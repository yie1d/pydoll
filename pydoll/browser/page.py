import asyncio

import aiofiles

from pydoll.commands.dom import DomCommands
from pydoll.commands.fetch import FetchCommands
from pydoll.commands.input import InputCommands
from pydoll.commands.network import NetworkCommands
from pydoll.commands.page import PageCommands
from pydoll.connection import ConnectionHandler
from pydoll.element import WebElement
from pydoll.events.page import PageEvents
from pydoll.utils import decode_image_to_bytes
from pydoll.constants import By
from pydoll import exceptions


class Page:
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

    async def go_to(self, url: str):
        """
        Navigates to a URL in the page.

        Args:
            url (str): The URL to navigate to.
        """
        await self._execute_command(PageCommands.go_to(url))

        try:
            await self._wait_page_load()
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

    async def wait_element(self, by: DomCommands.SelectorType, value: str, timeout: int = 30):
        """
        Waits for an element to appear on the page.

        Args:
            by (str): The type of selector to use (e.g., 'css', 'xpath').
            value (str): The value of the selector to use.
        """
        start_time = asyncio.get_event_loop().time()
        while True:
            node_description = await self._get_node_description(by, value)
            if node_description:
                break

            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError('Element not found')
            await asyncio.sleep(0.5)
        
        return WebElement(node_description, self._connection_handler, by)

    async def find_element(self, by: DomCommands.SelectorType, value: str, raise_exc: bool = True):
        """
        Finds an element on the current page using the specified selector.

        Args:
            by (str): The type of selector to use (e.g., 'css', 'xpath').
            value (str): The value of the selector to use.

        Returns:
            dict: The response from the browser.
        """
        node_description = await self._get_node_description(by, value)
        
        if not node_description:
            if raise_exc:
                raise exceptions.ElementNotFound('Element not found')
            return None
        
        return WebElement(node_description, self._connection_handler, by)

    async def _get_node_description(self, by: str, value: str):
        """
        Executes a command to find an element on the page.

        Args:
            by (str): The type of selector to use.
            value (str): The value of the selector to use.

        Returns:
            dict: The response from the browser.
        """
        root_node_id = await self._get_root_node_id()
        response = await self._execute_command(
            DomCommands.find_element(root_node_id, by, value)
        )
        if not response.get('result', {}):
            return None
        
        if by == By.XPATH:
            
            if not response.get('result', {}).get('result', {}).get('objectId'):
                return None
            
            target_node_id = response['result']['result']['objectId']
        else:
            target_node_id = response['result']['nodeId']
            if target_node_id == 0:
                return None
        
        node_description = await self._describe_node(target_node_id)
        node_description['objectId'] = target_node_id
        return node_description
    
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

    async def _execute_command(self, command: dict) -> dict:
        """
        Executes a command on the page.

        Args:
            command (dict): The command to execute.

        Returns:
            dict: The result of the command execution.
        """
        return await self._connection_handler.execute_command(
            command, timeout=60
        )

    async def _wait_page_load(self):
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
        await asyncio.wait_for(page_loaded.wait(), timeout=300)
        
        if page_events_auto_enabled:
            await self.disable_page_events()

    async def _get_root_node_id(self):
        """
        Retrieves the root node ID of the current page's Document Object Model (DOM).
        This ID serves as a fundamental reference point for various DOM operations,
        such as locating specific elements or manipulating the document structure.

        The root node is typically the <html> element in an HTML document, and its ID
        is essential for subsequent DOM interactions.

        Returns:
            int: The unique ID of the root node in the current DOM.

        Raises:
            Exception: If the command to retrieve the DOM document fails or
            does not return a valid root node ID.
        """
        response = await self._execute_command(DomCommands.dom_document())
        return response['result']['root']['nodeId']

    async def _describe_node(self, id: int | str) -> dict:
        """
        Provides a detailed description of a specific node within the current page's DOM.
        Each node represents an element in the document, and this method retrieves
        comprehensive information about the node, including its ID, tag name, attributes,
        and any child nodes that it may contain.

        This method is useful for understanding the structure of the DOM and for
        performing operations on specific elements based on their properties.

        Args:
            node_id (int): The unique ID of the node to describe.

        Returns:
            dict: A dictionary containing the detailed description of the node,
            including its ID, tag name, attributes, and child nodes.

        Raises:
            ValueError: If the provided node ID is invalid or does not correspond
            to a valid node in the DOM.
        """
        if isinstance(id, str):
            response = await self._execute_command(
                DomCommands.describe_node_by_object_id(id)
            )
            return response['result']['node']
        
        response = await self._execute_command(
            DomCommands.describe_node(id)
        )
        return response['result']['node']
