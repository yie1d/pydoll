import asyncio
from typing import Callable

import aiohttp
import websockets


class ConnectionHandler:
    """
    A class to handle WebSocket connections for browser automation.

    This class manages the connection to the browser and the associated page,
    providing methods to execute commands and register event callbacks.
    """

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

    @property
    async def page_ws_address(self) -> str:
        """
        Asynchronously retrieves the WebSocket address for the current page.

        If the address has not been fetched yet, it will call the internal method
        to obtain it. 

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

        If the address has not been fetched yet, it will call the internal method
        to obtain it.

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
        """
        if not self._connection:
            self._connection = await self._connect_to_page()
        return self._connection

    async def execute_command(self, command):
        """
        Sends a command to the connected WebSocket.

        Args:
            command (dict): The command to send, which should be a dictionary
                            with the necessary parameters.

        Raises:
            ValueError: If the command is invalid.
        """
        command['id'] = self._id
        command_str = str(command).replace("'", '"')
        self._id += 1
        await self.connection.send(command_str)

    async def _connect_to_page(self):
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

    async def register_callback(self, event_name: str, callback: Callable):
        """
        Registers a callback function for a specific event.

        Args:
            event_name (str): The name of the event to register the callback for.
            callback (Callable): The callback function to execute when the event occurs.

        Raises:
            ValueError: If the callback is not callable.
        """
        if not callable(callback):
            raise ValueError('Invalid callback')
        self._event_callbacks[event_name] = callback

    async def _receive_events(self):
        """
        Continuously listens for incoming events from the WebSocket connection.

        Processes incoming messages and triggers registered callbacks based on the event type.
        """
        try:
            while True:
                message = await self.connection.recv()
                event = message.encode('utf-8').decode('unicode_escape')
                await self._handle_event(event)
        except websockets.ConnectionClosed:
            print('Connection closed')
        except Exception as e:
            print(f'Error while receiving event: {e}')

    async def _handle_event(self, event):
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
    async def _get_page_ws_address():
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
                async with session.get('http://localhost:9222/json') as response:
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
    async def _get_browser_ws_address():
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
                async with session.get('http://localhost:9222/json/version') as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data['webSocketDebuggerUrl']
        except aiohttp.ClientError as e:
            raise ValueError(f'Failed to get browser ws address: {e}')
        except KeyError as e:
            raise ValueError(f'Failed to get browser ws address: {e}')
