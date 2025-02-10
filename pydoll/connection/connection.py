import asyncio
import json
import logging
from typing import Callable

import websockets

from pydoll import exceptions
from pydoll.connection.managers import CommandManager, EventsHandler
from pydoll.utils import get_browser_ws_address

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConnectionHandler:
    """
    A class to handle WebSocket connections for browser automation.

    This class manages the connection to the browser and the associated page,
    providing methods to execute commands and register event callbacks.
    """

    def __init__(
        self,
        connection_port: int,
        page_id: str = 'browser',
        ws_address_resolver: Callable[[int], str] = get_browser_ws_address,
        ws_connector: Callable = websockets.connect,
    ):
        """
        Initializes the ConnectionHandler instance.

        Args:
            connection_port (int): The port to connect to the browser.

        Sets up the internal state including WebSocket addresses,
        connection instance, event callbacks, and command ID.
        """
        self._connection_port = connection_port
        self._page_id = page_id
        self._ws_address_resolver = ws_address_resolver
        self._ws_connector = ws_connector
        self._ws_connection = None
        self._command_manager = CommandManager()
        self._events_handler = EventsHandler()
        logger.info('ConnectionHandler initialized.')

    @property
    def network_logs(self):
        return self._events_handler.network_logs

    @property
    def dialog(self):
        return self._events_handler.dialog

    async def ping(self) -> bool:
        """
        Sends a ping message to the browser.

        Returns:
            bool: True if the ping was successful, False otherwise.
        """
        try:
            await self._ensure_active_connection()
            await self._ws_connection.ping()
            return True
        except Exception:
            return False

    async def execute_command(self, command: dict, timeout: int = 10) -> dict:
        """
        Sends a command to the browser and awaits its response.

        Args:
            command (dict): The command to send, structured as a dictionary.
            timeout (int, optional): Time in seconds to wait for a response.
                Defaults to 10.

        Returns:
            dict: The response from the browser.

        Raises:
            InvalidCommand: If the command is not a dictionary.
            TimeoutError: If the command execution exceeds the timeout.
        """
        if not isinstance(command, dict):
            logger.error('Command must be a dictionary.')
            raise exceptions.InvalidCommand('Command must be a dictionary')

        await self._ensure_active_connection()
        future = self._command_manager.create_command_future(command)
        command_str = json.dumps(command)

        try:
            await self._ws_connection.send(command_str)
            response: str = await asyncio.wait_for(future, timeout)
            return json.loads(response)
        except asyncio.TimeoutError as exc:
            self._command_manager.remove_pending_command(command['id'])
            raise exc
        except websockets.ConnectionClosed as exc:
            await self._handle_connection_loss()
            raise exc

    async def register_callback(
        self, event_name: str, callback: Callable, temporary: bool = False
    ):
        return self._events_handler.register_callback(
            event_name, callback, temporary
        )

    async def remove_callback(self, callback_id: int):
        return self._events_handler.remove_callback(callback_id)

    async def clear_callbacks(self):
        return self._events_handler.clear_callbacks()

    async def close(self):
        """
        Closes the WebSocket connection.

        Closes the WebSocket connection and clears all event callbacks.
        """
        await self.clear_callbacks()
        await self._ws_connection.close()
        logger.info('WebSocket connection closed.')

    async def _ensure_active_connection(self):
        """Guarantee an active connection exists."""
        if self._ws_connection is None or self._ws_connection.closed:
            await self._establish_new_connection()

    async def _establish_new_connection(self):
        """Create fresh connection and start listening."""
        ws_address = await self._resolve_ws_address()
        logger.info(f'Connecting to {ws_address}')
        self._ws_connection = await self._ws_connector(ws_address)
        self._receive_task = asyncio.create_task(self._receive_events())
        logger.debug('WebSocket connection established')

    async def _resolve_ws_address(self):
        """Determine correct WebSocket address."""
        if 'browser' in self._page_id:
            return await self._ws_address_resolver(self._connection_port)
        return (
            f'ws://localhost:{self._connection_port}/devtools/page/'
            f'{self._page_id}'
        )

    async def _handle_connection_loss(self):
        """Clean up after connection loss."""
        if self._ws_connection and not self._ws_connection.closed:
            await self._ws_connection.close()
        self._ws_connection = None

        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()

        logger.info('Connection resources cleaned up')

    async def _receive_events(self):
        """
        Main loop for receiving and processing incoming WebSocket messages.
        Delegates processing to specialized handlers based on message type.
        """
        try:
            async for raw_message in self._incoming_messages():
                await self._process_single_message(raw_message)
        except websockets.ConnectionClosed as e:
            logger.info(f'Connection closed gracefully: {e}')
        except Exception as e:
            logger.error(f'Unexpected error in event loop: {e}')
            raise

    async def _incoming_messages(self):
        """Generator that yields raw messages while connection is open"""
        while not self._ws_connection.closed:
            yield await self._ws_connection.recv()

    async def _process_single_message(self, raw_message: str):
        """Orchestrates processing of a single raw WebSocket message"""
        message = self._parse_message(raw_message)
        if not message:
            return

        if self._is_command_response(message):
            await self._handle_command_message(message)
        else:
            await self._handle_event_message(message)

    @staticmethod
    def _parse_message(raw_message: str) -> dict | None:
        """
        Attempts to parse raw message string into JSON.
        Returns parsed dict or None if parsing fails.
        """
        try:
            return json.loads(raw_message)
        except json.JSONDecodeError:
            logger.warning(f'Failed to parse message: {raw_message[:200]}...')
            return None

    @staticmethod
    def _is_command_response(message: dict) -> bool:
        """Determines if message is a response to a command"""
        return 'id' in message and isinstance(message['id'], int)

    async def _handle_command_message(self, message: dict):
        """Processes messages that are command responses"""
        logger.debug(f'Processing command response: {message.get("id")}')
        self._command_manager.resolve_command(
            message['id'], json.dumps(message)
        )

    async def _handle_event_message(self, message: dict):
        """Processes messages that are spontaneous events"""
        event_type = message.get('method', 'unknown-event')
        logger.debug(f'Processing {event_type} event')
        await self._events_handler.process_event(message)

    def __repr__(self):
        return f'ConnectionHandler(port={self._connection_port})'

    def __str__(self):
        return f'ConnectionHandler(port={self._connection_port})'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
