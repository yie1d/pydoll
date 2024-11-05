import asyncio
import json

import aiofiles

from pydoll.commands.dom import DomCommands
from pydoll.commands.fetch import FetchCommands
from pydoll.commands.network import NetworkCommands
from pydoll.commands.page import PageCommands
from pydoll.connection import ConnectionHandler
from pydoll.events.page import PageEvents
from pydoll.mixins.find_elements import FindElementsMixin
from pydoll.utils import decode_image_to_bytes


class Page(FindElementsMixin):
    def __init__(self, connection_port: int, page_id: str):
        """
        Initializes the Page instance.

        Args:
            connection_handler (ConnectionHandler): The connection handler instance.
            page_id (str): The ID of the page, obtained via the DevTools Protocol.
        """
        self._connection_handler = ConnectionHandler(connection_port, page_id)
        self._page_events_enabled = False
        self._network_events_enabled = False
        self._fetch_events_enabled = False
        self._dom_events_enabled = False

    @property
    def page_events_enabled(self) -> bool:
        """
        Returns whether page events are enabled or not.

        Returns:
            bool: True if page events are enabled, False otherwise.
        """
        return self._page_events_enabled

    @property
    def network_events_enabled(self) -> bool:
        """
        Returns whether network events are enabled or not.

        Returns:
            bool: True if network events are enabled, False otherwise.
        """
        return self._network_events_enabled

    @property
    def fetch_events_enabled(self) -> bool:
        """
        Returns whether fetch events are enabled or not.

        Returns:
            bool: True if fetch events are enabled, False otherwise.
        """
        return self._fetch_events_enabled

    @property
    def dom_events_enabled(self) -> bool:
        """
        Returns whether DOM events are enabled or not.

        Returns:
            bool: True if DOM events are enabled, False otherwise.
        """
        return self._dom_events_enabled

    @property
    async def current_url(self) -> str:
        """
        Retrieves the current URL of the page.

        Returns:
            str: The current URL of the page.
        """
        response = await self._execute_command(DomCommands.get_current_url())
        return response['result']['result']['value']

    @property
    async def page_source(self) -> str:
        """
        Retrieves the source code of the page.

        Returns:
            str: The source code of the page.
        """
        root_node_id = await self._get_root_node_id()
        response = await self._execute_command(
            DomCommands.get_outer_html(root_node_id)
        )
        return response['result']['outerHTML']

    async def go_to(self, url: str, timeout=300):
        """
        Navigates to a URL in the page.

        Args:
            url (str): The URL to navigate to.
        """
        await self._execute_command(PageCommands.go_to(url))

        try:
            await self._wait_page_load(timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError('Page load timed out')

    async def refresh(self):
        """
        Refreshes the page.
        """
        await self._execute_command(PageCommands.refresh())
        try:
            await self._wait_page_load()
        except asyncio.TimeoutError:
            raise TimeoutError('Page load timed out')

    async def get_screenshot(self, path: str):
        """
        Captures a screenshot of the page.

        Args:
            path (str): The file path to save the screenshot to.
        """
        response = await self._execute_command(PageCommands.screenshot())
        screenshot_b64 = response['result']['data'].encode('utf-8')
        screenshot_bytes = decode_image_to_bytes(screenshot_b64)
        async with aiofiles.open(path, 'wb') as file:
            await file.write(screenshot_bytes)

    async def get_pdf_base64(self):
        """
        Retrieves the PDF data of the page.

        Returns:
            str: The PDF data of the page.
        """
        response = await self._execute_command(PageCommands.print_to_pdf())
        return response['result']['data'].encode('utf-8')
    
    async def print_to_pdf(self, path: str):
        """
        Prints the page to a PDF file.

        Args:
            path (str): The file path to save the PDF file to.
        """
        response = await self._execute_command(PageCommands.print_to_pdf(path))
        pdf_b64 = response['result']['data'].encode('utf-8')
        pdf_bytes = decode_image_to_bytes(pdf_b64)
        async with aiofiles.open(path, 'wb') as file:
            await file.write(pdf_bytes)

    async def get_network_logs(self, matches: list[str] = []):
        """
        Retrieves network logs from the page.

        Args:
            matches (str): The URL pattern to match network logs against.

        Returns:
            list: A list of network logs that match the specified pattern.
        """
        network_logs = self._connection_handler.network_logs
        logs_matched = []
        for log in network_logs:
            if not log.get('params', {}).get('request', {}).get('url'):
                continue
            for match in matches:
                if match in log['params']['request']['url']:
                    logs_matched.append(log)
                    break

        if not logs_matched:
            raise LookupError('No network logs matched the specified pattern')

        return logs_matched

    async def get_network_response_bodies(self, matches: list[str] = []):
        """
        Retrieves the response bodies of network requests that match the specified pattern.

        Args:
            matches (list): The URL patterns to match network requests against.

        Returns:
            list: A list of response bodies from network requests that match the specified patterns.
        """
        logs_matched = await self.get_network_logs(matches)
        responses = []
        for log in logs_matched:
            response = await self.get_network_response_body(
                log['params']['requestId']
            )
            responses.append(json.loads(response))
        return responses

    async def get_network_response_body(self, request_id: str):
        """
        Retrieves the response body of a network request.

        Args:
            request_id (str): The ID of the network request.

        Returns:
            str: The response body of the network request.
        """
        response = await self._execute_command(
            NetworkCommands.get_response_body(request_id)
        )
        return response['result']['body']

    async def enable_page_events(self):
        """
        Enables page events for the page.
        """
        await self._execute_command(PageCommands.enable_page())
        self._page_events_enabled = True

    async def enable_network_events(self):
        """
        Enables network events for the page.
        """
        await self._execute_command(NetworkCommands.enable_network_events())
        self._network_events_enabled = True

    async def enable_fetch_events(
        self, handle_auth: bool = False, resource_type: str = 'Document'
    ):
        """
        Enables fetch events for the page.
        """
        await self._execute_command(
            FetchCommands.enable_fetch_events(handle_auth, resource_type)
        )
        self._fetch_events_enabled = True

    async def enable_dom_events(self):
        """
        Enables DOM events for the page.
        """
        await self._execute_command(DomCommands.enable_dom_events())
        self._dom_events_enabled = True

    async def disable_fetch_events(self):
        """
        Disables fetch events for the page.
        """
        await self._execute_command(FetchCommands.disable_fetch_events())
        self._fetch_events_enabled = False

    async def disable_page_events(self):
        """
        Disables page events for the page.
        """
        await self._execute_command(PageCommands.disable_page())
        self._page_events_enabled = False

    async def on(
        self, event_name: str, callback: callable, temporary: bool = False
    ):
        """
        Registers an event listener for the page.

        Args:
            event (str): The event to listen for.
            callback (callable): The callback function to execute when the event is triggered.
            temporary (bool): Whether the event listener is temporary or not.
        """

        async def callback_wrapper(event):
            asyncio.create_task(callback(event))

        if asyncio.iscoroutinefunction(callback):
            function_to_register = callback_wrapper
        else:
            function_to_register = callback

        await self._connection_handler.register_callback(
            event_name, function_to_register, temporary
        )

    async def execute_js_script(self, script: str) -> dict:
        """
        Executes a JavaScript script in the page.

        Args:
            script (str): The JavaScript script to execute.

        Returns:
            dict: The result of the JavaScript script execution.
        """
        command = {
            'method': 'Runtime.evaluate',
            'params': {'expression': script, 'returnByValue': True},
        }
        return await self._execute_command(command)

    async def _wait_page_load(self, timeout: int = 300):
        """
        Waits for the page to finish loading.
        """
        page_events_auto_enabled = False

        if not self._page_events_enabled:
            page_events_auto_enabled = True
            await self.enable_page_events()

        page_loaded = asyncio.Event()
        await self.on(
            PageEvents.PAGE_LOADED, lambda _: page_loaded.set(), temporary=True
        )  
        try:
            await asyncio.wait_for(page_loaded.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            print('TimeoutError')
        
        if page_events_auto_enabled:
            await self.disable_page_events()
