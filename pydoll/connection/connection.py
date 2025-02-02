import asyncio
import json
import logging
from typing import Callable

import websockets

from pydoll import exceptions
from pydoll.utils import get_browser_ws_address
from pydoll.connection.managers import CommandManager, EventsHandler

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
        self._connection = None
        self._event_callbacks = {}
        self._callback_id = 0
        self._command_manager = CommandManager()
        self._events_handler = EventsHandler()
        logger.info('ConnectionHandler initialized.')

    @property
    def network_logs(self):
        return self._events_handler.network_logs
    
    @property
    async def connection(self) -> websockets.WebSocketClientProtocol:
        """
        Returns the WebSocket connection to the browser.

        If the connection is not established, it is created first.

        Returns:
            websockets.WebSocketClientProtocol: The WebSocket connection.

        Raises:
            ValueError: If the connection cannot be established.
        """
        if self._connection is None or self._connection.closed:
            await self.connect_to_page()
        return self._connection

    async def ping(self) -> bool:
        """
        Sends a ping message to the browser.

        Returns:
            bool: True if the ping was successful, False otherwise.
        """
        try:
            await (await self.connection).ping()
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

        future = self._command_manager.create_command_future(command)
        command_str = json.dumps(command)

        connection = await self.connection
        await connection.send(command_str)
        logger.info(f'Sent command with ID {command["id"]}: {command}')

        try:
            response: str = await asyncio.wait_for(future, timeout)
            logger.info(
                f'Received response for command ID {command["id"]}: {response}'
            )
            return json.loads(response)
        except asyncio.TimeoutError:
            self._command_manager.remove_pending_command(command['id'])
            logger.warning(
                f'Command execution timed out for ID {command["id"]}'
            )
            raise TimeoutError('Command execution timed out')

    async def connect_to_page(self) -> websockets.WebSocketClientProtocol:
        """
        Establishes a WebSocket connection to the browser page.

        Returns:
            websockets.WebSocketClientProtocol: The WebSocket connection.

        Initiates a task to listen for events from the page WebSocket.
        """
        if 'browser' in self._page_id:
            ws_address = await self._ws_address_resolver(self._connection_port)
        else:
            ws_address = (
                f'ws://localhost:{self._connection_port}/devtools/page/'
                + self._page_id
            )

        connection = await websockets.connect(ws_address)
        logger.info(f'Connected to page WebSocket at {ws_address}')
        asyncio.create_task(self._receive_events())
        self._connection = connection

    async def _receive_events(self):
        """
        Main loop for receiving and processing incoming WebSocket messages.
        Delegates processing to specialized handlers based on message type.
        """
        try:
            async for raw_message in self._incoming_messages():
                await self._process_single_message(raw_message)
        except websockets.ConnectionClosed as e:
            logger.warning(f"Connection closed gracefully: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in event loop: {e}")
            raise
    
    async def _incoming_messages(self):
        """Generator that yields raw messages while connection is open"""
        while not self._connection.closed:
            yield await self._connection.recv()
    
    async def _process_single_message(self, raw_message: str):
        """Orchestrates processing of a single raw WebSocket message"""
        message = self._parse_message(raw_message)
        if not message:
            return

        if self._is_command_response(message):
            await self._handle_command_message(message)
        else:
            await self._handle_event_message(message)

    def _parse_message(self, raw_message: str) -> dict | None:
        """
        Attempts to parse raw message string into JSON.
        Returns parsed dict or None if parsing fails.
        """
        try:
            return json.loads(raw_message)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse message: {raw_message[:200]}...")
            return None

    def _is_command_response(self, message: dict) -> bool:
        """Determines if message is a response to a command"""
        return "id" in message and isinstance(message["id"], int)

    async def _handle_command_message(self, message: dict):
        """Processes messages that are command responses"""
        logger.debug(f"Processing command response: {message.get('id')}")
        self._command_manager.resolve_command(message["id"], json.dumps(message))

    async def _handle_event_message(self, message: dict):
        """Processes messages that are spontaneous events"""
        event_type = message.get("method", "unknown-event")
        logger.debug(f"Processing {event_type} event")
        await self._events_handler.process_event(message)

    async def register_callback(self, event_name: str, callback: Callable, temporary: bool = False):
        return await self._events_handler.register_callback(event_name, callback, temporary)
    
    async def remove_callback(self, callback_id: int):
        return await self._events_handler.remove_callback(callback_id)
    
    async def clear_callbacks(self):
        return self._events_handler.clear_callbacks()
    
    async def close(self):
        """
        Closes the WebSocket connection.

        Closes the WebSocket connection and clears all event callbacks.
        """
        await self.clear_callbacks()
        await self._connection.close()
        logger.info('WebSocket connection closed.')

    def __repr__(self):
        return f'ConnectionHandler(port={self._connection_port})'

    def __str__(self):
        return f'ConnectionHandler(port={self._connection_port})'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
