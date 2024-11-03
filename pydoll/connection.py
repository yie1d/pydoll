import asyncio
import json
import logging
from typing import Callable

import aiohttp
import websockets

from pydoll import exceptions
from pydoll.utils import get_browser_ws_address

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConnectionHandler:
    """
    A class to handle WebSocket connections for browser automation.

    This class manages the connection to the browser and the associated page,
    providing methods to execute commands and register event callbacks.
    """

    def __init__(self, connection_port: int, page_id: str = 'browser'):
        """
        Initializes the ConnectionHandler instance.

        Args:
            connection_port (int): The port to connect to the browser.

        Sets up the internal state including WebSocket addresses,
        connection instance, event callbacks, and command ID.
        """
        self._connection_port = connection_port
        self._page_id = page_id
        self._connection = None
        self._event_callbacks = {}
        self._id = 1
        self._callback_id = 1
        self._pending_commands: dict[int, asyncio.Future] = {}
        logger.info('ConnectionHandler initialized.')

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

    async def execute_command(self, command: dict, timeout: int = 10) -> dict:
        """
        Sends a command to the browser and awaits its response.

        Args:
            command (dict): The command to send, structured as a dictionary.
            timeout (int, optional): Time in seconds to wait for a response. Defaults to 10.

        Returns:
            dict: The response from the browser.

        Raises:
            ValueError: If the command is not a dictionary.
            TimeoutError: If the command execution exceeds the timeout.
        """
        if not isinstance(command, dict):
            logger.error('Command must be a dictionary.')
            raise exceptions.InvalidCommand('Command must be a dictionary')

        command['id'] = self._id
        command_str = json.dumps(command)
        future = asyncio.Future()
        self._pending_commands[self._id] = future
        self._id += 1

        connection = await self.connection
        await connection.send(command_str)
        logger.info(f'Sent command with ID {command["id"]}: {command}')

        try:
            response: str = await asyncio.wait_for(future, timeout)
            logger.info(
                f'Received response for command ID {command["id"]}: {response}'
            )
            del self._pending_commands[command['id']]
            return json.loads(response)
        except asyncio.TimeoutError:
            del self._pending_commands[command['id']]
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
            ws_address = await get_browser_ws_address(self._connection_port)
        else:
            ws_address = (
                f'ws://localhost:{self._connection_port}/devtools/page/'
                + self._page_id
            )

        connection = await websockets.connect(ws_address)
        logger.info(f'Connected to page WebSocket at {ws_address}')
        asyncio.create_task(self._receive_events())
        self._connection = connection

    async def register_callback(
        self, event_name: str, callback: Callable, temporary: bool = False
    ) -> None:
        """
        Registers a callback function for a specific event.

        Args:
            event_name (str): The name of the event to register.
            callback (Callable): The function to call when the event is received.
            temporary (bool, optional): If True, the callback will be removed after one use. Defaults to False.

        Raises:
            ValueError: If the callback is not callable.
        """
        if not callable(callback):
            logger.error('Callback must be a callable function.')
            raise exceptions.InvalidCallback(
                'Callback must be a callable function'
            )

        self._event_callbacks[self._callback_id] = {
            'event': event_name,
            'callback': callback,
            'temporary': temporary,
        }
        logger.info(
            f"Registered callback for event '{event_name}' with ID {self._callback_id}"
        )
        self._callback_id += 1

    async def _receive_events(self):
        """
        Listens for incoming events from the WebSocket connection and processes them.

        Matches responses to pending commands and handles events based on registered callbacks.
        """
        try:
            while True:
                connection = await self.connection
                event = await connection.recv()
                try:
                    event_json = json.loads(event)
                except json.JSONDecodeError:
                    logger.warning(f'Received malformed JSON message: {event}')
                    continue

                if (
                    'id' in event_json
                    and event_json['id'] in self._pending_commands
                ):
                    logger.info(
                        f'Received response for pending command ID {event_json["id"]}'
                    )
                    self._pending_commands[event_json['id']].set_result(event)
                    continue

                logger.info(f'Received event: {event_json["method"]}')
                await self._handle_event(event_json)
        except websockets.ConnectionClosed:
            logger.warning('WebSocket connection closed.')
        except Exception as exc:
            logger.error(f'Error while receiving event: {exc}', exc_info=True)

    async def _handle_event(self, event: dict):
        """
        Processes a received event and triggers the appropriate callback(s).

        Args:
            event (dict): The event data in dictionary form.
        """
        event_name = event.get('method')

        if event_name:
            logger.info(f'Handling event {event}')
        else:
            logger.warning('Event without a method received.')

        event_callbacks = self._event_callbacks.copy()
        for callback_id, callback_data in event_callbacks.items():
            if callback_data['event'] == event_name:
                callback_func = callback_data['callback']

                if asyncio.iscoroutinefunction(callback_func):
                    await callback_func(event)
                else:
                    callback_func(event)

                if callback_data['temporary']:
                    del self._event_callbacks[callback_id]
                    logger.info(
                        f'Removed temporary callback with ID {callback_id}'
                    )

    def clear_callbacks(self):
        """
        Clears all registered event callbacks.

        Removes all event callbacks from the internal dictionary.
        """
        self._event_callbacks = {}
        logger.info('All event callbacks cleared.')

    async def close(self):
        """
        Closes the WebSocket connection.

        Closes the WebSocket connection and clears all event callbacks.
        """
        self.clear_callbacks()
        await self._connection.close()
        logger.info('WebSocket connection closed.')

    def __repr__(self):
        return f'ConnectionHandler(port={self._connection_port})'

    def __str__(self):
        return f'ConnectionHandler(port={self._connection_port})'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
