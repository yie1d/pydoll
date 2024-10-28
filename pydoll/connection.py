import asyncio
import json
from typing import Callable

import aiohttp
import websockets


class ConnectionHandler:
    """
    A class to handle WebSocket connections for browser automation.

    This class manages the connection to the browser and the associated page,
    providing methods to execute commands and register event callbacks.
    """

    BROWSER_JSON_URL = 'http://localhost:9222/json'
    BROWSER_VERSION_URL = 'http://localhost:9222/json/version'

    def __init__(self):
        """
        Initializes the ConnectionHandler instance.

        Sets up the internal state including WebSocket addresses,
        connection instance, event callbacks, and command ID.
        """
        self._page_ws_address = None
        self._browser_ws_address = None
        self._connection = None
        self._event_callbacks = {}
        self._id = 1
        self._pending_commands: dict[int, asyncio.Future] = {}

    @property
    async def page_ws_address(self) -> str:
        """
        Asynchronously retrieves the WebSocket address for the current page.

        If the address has not been fetched yet,
        it will call the internal method to obtain it.

        Returns:
            str: The WebSocket address of the page.
        """
        if not self._page_ws_address:
            self._page_ws_address = await self._get_page_ws_address()
        return self._page_ws_address

    @property
    async def browser_ws_address(self) -> str:
        """
        Asynchronously retrieves the WebSocket address for the browser.

        If the address has not been fetched yet, it will call
        the internal method to obtain it.

        Returns:
            str: The WebSocket address of the browser.
        """
        if not self._browser_ws_address:
            self._browser_ws_address = await self._get_browser_ws_address()
        return self._browser_ws_address

    @property
    async def connection(self) -> websockets.WebSocketClientProtocol:
        """
        Asynchronously establishes a connection to the page WebSocket.

        If the connection has not been established yet, it will call the method
        to connect to the page.

        Returns:
            Connection: The active WebSocket connection to the page.

        Raises:
            Exception: If the connection fails to establish.
        """
        if not self._connection or self._connection.closed:
            try:
                self._connection = await self._connect_to_page()
            except Exception as exc:
                raise Exception(f'Failed to connect to page: {exc}')

        return self._connection

    async def execute_command(self, command: dict) -> dict:
        """
        Sends a command to the connected WebSocket.

        Args:
            command (dict): The command to send, which should be a dictionary
                            with the necessary parameters.

        Returns:
            dict: The response received from the WebSocket.

        Raises:
            ValueError: If the command is invalid.
        """
        if not isinstance(command, dict):
            raise ValueError('Command must be a dictionary')

        command['id'] = self._id
        command_str = str(command).replace("'", '"')

        future = asyncio.Future()
        self._pending_commands[self._id] = future
        self._id += 1

        connection = await self.connection
        await connection.send(command_str)

        response: str = await future
        del self._pending_commands[command['id']]
        parsed_response = response.encode('utf-8').decode('unicode_escape')
        return json.loads(parsed_response)

    async def _connect_to_page(self) -> websockets.WebSocketClientProtocol:
        """
        Establishes a WebSocket connection to the current page.

        Initiates the connection using the page's WebSocket address
        and starts listening for incoming events.

        Returns:
            Connection: The active WebSocket connection to the page.
        """
        ws_address = await self.page_ws_address
        connection = await websockets.connect(ws_address)
        asyncio.create_task(self._receive_events())
        return connection

    async def register_callback(
        self, event_name: str, callback: Callable
    ) -> None:
        """
        Registers a callback function for a specific event.

        Args:
            event_name (str): Name of the event to register the callback for.
            callback (Callable): Function to execute when the event occurs.

        Raises:
            ValueError: If the callback is not callable.
        """
        if not callable(callback):
            raise ValueError('Callback must be a callable function')
        self._event_callbacks[event_name] = callback

    async def _receive_events(self):
        """
        Continuously listens for messages from the WebSocket connection.

        This method processes incoming messages in an infinite loop.
        If a message corresponds to a pending command (identified by its 'id'),
        it completes the associated `Future`.
        Otherwise, it treats the message as an event and
        calls `_handle_event` for processing.

        Raises:
            websockets.ConnectionClosed: If the WebSocket connection is closed.
            Exception: For other unforeseen errors.
        """
        try:
            while True:
                connection = await self.connection
                message = await connection.recv()
                event = message.encode('utf-8').decode('unicode_escape')
                try:
                    event_json = json.loads(event)
                except json.JSONDecodeError:
                    continue

                # Handle pending command response
                if (
                    'id' in event_json
                    and event_json['id'] in self._pending_commands
                ):
                    print(f'Received response: {event}')
                    self._pending_commands[event_json['id']].set_result(event)
                    continue

                await self._handle_event(event_json)
        except websockets.ConnectionClosed:
            print('Connection closed')
        except Exception as exc:
            import traceback

            print(traceback.format_exc())
            print(f'Error while receiving event: {exc}')

    async def _handle_event(self, event: dict):
        """
        Handles an incoming event by executing the corresponding callback.

        Args:
            event (dict): The event data received from the WebSocket.
        """
        event_name = event['method']
        if event_name in self._event_callbacks:
            callback = self._event_callbacks[event_name]
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)

    @staticmethod
    async def _get_page_ws_address() -> str:
        """
        Asynchronously retrieves the WebSocket address for the current page.

        Returns:
            str: The WebSocket address of the page.

        Raises:
            ValueError: If unable to fetch the address due to network errors
                         or missing data.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    ConnectionHandler.BROWSER_JSON_URL
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return [
                        current_data['webSocketDebuggerUrl']
                        for current_data in data
                        if current_data['url'] == 'chrome://newtab/'
                    ][0]
        except aiohttp.ClientError as e:
            raise ValueError(f'Failed to get page ws address: {e}')
        except (KeyError, IndexError) as e:
            raise ValueError(f'Failed to get page ws address: {e}')

    @staticmethod
    async def _get_browser_ws_address() -> str:
        """
        Asynchronously retrieves the WebSocket address for the browser.

        Returns:
            str: The WebSocket address of the browser.

        Raises:
            ValueError: If unable to fetch the address due to network errors
                         or missing data.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    ConnectionHandler.BROWSER_VERSION_URL
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data['webSocketDebuggerUrl']
        except aiohttp.ClientError as e:
            raise ValueError(f'Failed to get browser ws address: {e}')
        except KeyError as e:
            raise ValueError(f'Failed to get browser ws address: {e}')
