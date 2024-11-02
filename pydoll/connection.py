import asyncio
import json
import logging
from typing import Callable

import aiohttp
import websockets

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConnectionHandler:
    """
    A class to handle WebSocket connections for browser automation.

    This class manages the connection to the browser and the associated page,
    providing methods to execute commands and register event callbacks.
    """

    BROWSER_JSON_URL = 'http://localhost:port/json'
    BROWSER_VERSION_URL = 'http://localhost:port/json/version'
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_port: int):
        """
        Initializes the ConnectionHandler instance.

        Args:
            connection_port (int): The port to connect to the browser.

        Sets up the internal state including WebSocket addresses,
        connection instance, event callbacks, and command ID.
        """
        if not hasattr(self, '_initialized'):  # Ensure init is called only once
            self._initialized = True
            self._connection_port = connection_port
            self._page_ws_address = None
            self._browser_ws_address = None
            self._connection = None
            self._event_callbacks = {}
            self._id = 1
            self._callback_id = 1
            self._reconnect_delay = 5
            self._reconnect_max_attempts = 5
            self._pending_commands: dict[int, asyncio.Future] = {}
            asyncio.create_task(self._monitor_connection())
            logger.info('ConnectionHandler initialized.')

    @property
    async def page_ws_address(self) -> str:
        """
        Retrieves the WebSocket address of the browser page.

        Returns:
            str: The WebSocket address of the browser page.
        """
        if not self._page_ws_address:
            logger.info('Fetching WebSocket address for the page.')
            self._page_ws_address = await self._get_page_ws_address()
            logger.info(
                f'Page WebSocket address obtained: {self._page_ws_address}'
            )
        return self._page_ws_address

    @property
    async def browser_ws_address(self) -> str:
        """
        Retrieves the WebSocket address of the browser.

        Returns:
            str: The WebSocket address of the browser.
        """
        if not self._browser_ws_address:
            logger.info('Fetching WebSocket address for the browser.')
            self._browser_ws_address = await self._get_browser_ws_address()
            logger.info(
                f'Browser WebSocket address obtained: {self._browser_ws_address}'
            )
        return self._browser_ws_address

    @property
    async def connection(self) -> websockets.WebSocketClientProtocol:
        """
        Establishes and returns the WebSocket connection to the page.

        Returns:
            websockets.WebSocketClientProtocol: The active WebSocket connection.
        
        Raises:
            Exception: If the connection fails.
        """
        if not self._connection or self._connection.closed:
            try:
                logger.info('Establishing WebSocket connection to the page.')
                self._connection = await self._connect_to_page()
                logger.info('WebSocket connection established.')
            except Exception as exc:
                logger.error(f'Failed to connect to page: {exc}')
                raise Exception(f'Failed to connect to page: {exc}')
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
            raise ValueError('Command must be a dictionary')

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
            del self._pending_commands[command['id']]
            logger.info(f'Received response for command ID {command["id"]}')
            return json.loads(response)
        except asyncio.TimeoutError:
            del self._pending_commands[command['id']]
            logger.warning(
                f'Command execution timed out for ID {command["id"]}'
            )
            raise TimeoutError('Command execution timed out')

    async def _connect_to_page(self) -> websockets.WebSocketClientProtocol:
        """
        Establishes a WebSocket connection to the browser page.

        Returns:
            websockets.WebSocketClientProtocol: The WebSocket connection.

        Initiates a task to listen for events from the page WebSocket.
        """
        ws_address = await self.page_ws_address
        connection = await websockets.connect(ws_address)
        logger.info(f'Connected to page WebSocket at {ws_address}')
        asyncio.create_task(self._receive_events())
        return connection

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
            raise ValueError('Callback must be a callable function')

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
                    logger.warning('Received malformed JSON message.')
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
            logger.info(f"Handling event '{event_name}'")
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

    async def _get_page_ws_address(self) -> str:
        """
        Fetches the WebSocket address for the browser page.

        Returns:
            str: The WebSocket address for the page.

        Raises:
            ValueError: If the address cannot be fetched due to network errors or missing data.
        """
        try:
            async with aiohttp.ClientSession() as session:
                
                async with session.get(
                    ConnectionHandler.BROWSER_JSON_URL.replace('port', str(self._connection_port))
                ) as response:
                    
                    response.raise_for_status()
                    data = await response.json()
                    ws_address = [
                        current_data['webSocketDebuggerUrl']
                        for current_data in data
                        if current_data['url'] == 'chrome://newtab/'
                    ][0]
                    logger.info(
                        'Page WebSocket address fetched successfully.'
                    )
                    return ws_address
        
        except aiohttp.ClientError as e:
            logger.error(
                'Failed to fetch page WebSocket address due to network error.'
            )
            raise ValueError(f'Failed to get page ws address: {e}')
        
        except (KeyError, IndexError) as e:
            logger.error(
                'Failed to get page WebSocket address due to missing data.'
            )
            raise ValueError(f'Failed to get page ws address: {e}')

    async def _get_browser_ws_address(self) -> str:
        """
        Fetches the WebSocket address for the browser instance.

        Returns:
            str: The WebSocket address for the browser.

        Raises:
            ValueError: If the address cannot be fetched due to network errors or missing data.
        """
        try:
            async with aiohttp.ClientSession() as session:
                
                async with session.get(
                    ConnectionHandler.BROWSER_VERSION_URL.replace('port', str(self._connection_port))
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info(
                        'Browser WebSocket address fetched successfully.'
                    )
                    return data['webSocketDebuggerUrl']
        
        except aiohttp.ClientError as e:
            logger.error(
                'Failed to fetch browser WebSocket address due to network error.'
            )
            raise ValueError(f'Failed to get browser ws address: {e}')
        
        except KeyError as e:
            logger.error(
                'Failed to get browser WebSocket address due to missing data.'
            )
            raise ValueError(f'Failed to get browser ws address: {e}')

    async def _monitor_connection(self):
        """
        Monitors the WebSocket connection and attempts to reconnect if it is lost.

        Retries the connection up to a maximum number of attempts and resends pending commands upon reconnection.
        """
        attempts = 0
        
        while attempts < self._reconnect_max_attempts:
            if self._connection is None or self._connection.closed:
                try:
                    logger.info('Attempting to reconnect to WebSocket...')
                    self._connection = await self._connect_to_page()
                    logger.info('Reconnected successfully.')
                    await self._resend_pending_commands()
                except Exception as e:
                    logger.warning(
                        f'Reconnection attempt {attempts + 1} failed: {e}'
                    )
                    await asyncio.sleep(self._reconnect_delay)
                    attempts += 1
            
            await asyncio.sleep(1)

        logger.error(
            'Failed to reconnect to WebSocket after maximum attempts.'
        )
        raise Exception(
            'Failed to reconnect to WebSocket after multiple attempts.'
        )

    async def _resend_pending_commands(self):
        """
        Resends commands that were pending when the connection was lost.

        Ensures that commands waiting for a response are re-sent upon reconnection.
        """
        for command_id, future in self._pending_commands.items():
            if not future.done():
                try:
                    command = {
                        'id': command_id,
                        **self._pending_commands[command_id],
                    }
                    command_str = json.dumps(command)
                    await self._connection.send(command_str)
                    logger.info(
                        f'Resent pending command with ID {command_id}'
                    )
                except Exception as exc:
                    logger.error(
                        f'Failed to resend command {command_id}: {exc}'
                    )
                    raise exc
