import asyncio
from typing import Callable

import aiohttp
import websockets


class ConnectionHandler:
    def __init__(self):
        self._page_ws_address = None
        self._browser_ws_address = None
        self._connection = None
        self._event_callbacks = {}
        self._id = 1

    @property
    async def page_ws_address(self) -> str:
        if not self._page_ws_address:
            self._page_ws_address = await self._get_page_ws_address()
        return self._page_ws_address

    @property
    async def browser_ws_address(self) -> str:
        if not self._browser_ws_address:
            self._browser_ws_address = await self._get_browser_ws_address()
        return self._browser_ws_address

    @property
    async def connection(self):
        if not self._connection:
            self._connection = self._connect_to_page()
        return self._connection

    async def execute_command(self, command):
        command['id'] = self._id
        command_str = str(command).replace("'", '"')
        self._id += 1
        await self.connection.send(command_str)

    async def _connect_to_page(self):
        ws_address = await self.page_ws_address
        connection = await websockets.connect(ws_address)
        asyncio.create_task(self._receive_events())
        return connection

    async def register_callback(self, event_name: str, callback: Callable):
        if not callable(callback):
            raise ValueError('Invalid callback')
        self._event_callbacks[event_name] = callback

    async def _receive_events(self):
        try:
            while True:
                message = await self.connection.recv()
                event = message.encode('utf-8').decode('unicode_escape')
                self._handle_event(event)
        except websockets.ConnectionClosed:
            print('Connection closed')
        except Exception as e:
            print(f'Error while receiving event: {e}')

    async def _handle_event(self, event):
        event_name = event['method']
        if event_name in self._event_callbacks:
            callback = self._event_callbacks[event_name]
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)

    @staticmethod
    async def _get_page_ws_address():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'http://localhost:9222/json'
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
    async def _get_browser_ws_address():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'http://localhost:9222/json/version'
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data['webSocketDebuggerUrl']
        except aiohttp.ClientError as e:
            raise ValueError(f'Failed to get browser ws address: {e}')
        except KeyError as e:
            raise ValueError(f'Failed to get browser ws address: {e}')
