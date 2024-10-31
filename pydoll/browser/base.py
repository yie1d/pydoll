import asyncio
import os
import subprocess
from abc import ABC, abstractmethod
from typing import Callable

from pydoll.browser.options import Options
from pydoll.commands.browser import BrowserCommands
from pydoll.commands.dom import DomCommands
from pydoll.commands.page import PageCommands
from pydoll.connection import ConnectionHandler
from pydoll.element import WebElement
from pydoll.utils import decode_image_to_bytes
from pydoll.events.page import PageEvents


class Browser(ABC):
    """
    A class to manage a browser instance for automated interactions.

    This class allows users to start and stop a browser, take screenshots,
    and register event callbacks.
    """

    def __init__(self, options: Options | None = None):
        """
        Initializes the Browser instance.

        Args:
            options (Options | None): An instance of the Options class to
            configure the browser. If None, default options will be used.
        """
        self.connection_handler = ConnectionHandler()
        self.options = self._initialize_options(options)
        self.process = None

    async def start(self) -> None:
        """
        Starts the browser process with the specified options.

        Returns:
            subprocess.Popen: The process object for the started browser.
        """
        binary_location = (
            self.options.binary_location or self._get_default_binary_location()
        )
        self.process = subprocess.Popen(
            [
                binary_location,
                '--remote-debugging-port=9222',
                *self.options.arguments,
            ],
            stdout=subprocess.PIPE,
        )
        if not await self._is_browser_running():
            raise ValueError('Failed to start browser')
        await self._enable_page_events()

    async def stop(self):
        """
        Stops the running browser process.

        Raises:
            ValueError: If the browser is not currently running.
        """
        if await self._is_browser_running():
            self.process.terminate()
            await self._execute_command(BrowserCommands.CLOSE)
        else:
            raise ValueError('Browser is not running')

    async def get_screenshot(self, path: str):
        """
        Captures a screenshot of the current page and saves
        it to the specified path.

        Args:
            path (str): The file path where the screenshot will be saved.
        """
        response = await self._execute_command(PageCommands.screenshot())
        image_b64 = response['result']['data'].encode('utf-8')
        image_bytes = decode_image_to_bytes(image_b64)
        with open(path, 'wb') as file:
            file.write(image_bytes)

    async def go_to(self, url: str):
        """
        Navigates the browser to the specified URL.

        Args:
            url (str): The URL to navigate to.
        """
        await self._execute_command(PageCommands.go_to(url))
        try:
            await self._wait_page_loaded()
        except asyncio.TimeoutError:
            raise TimeoutError('Page load timed out')

    async def refresh(self):
        """
        Refreshes the current page in the browser.
        """
        await self._execute_command(PageCommands.refresh())
        try:
            await self._wait_page_loaded()
        except asyncio.TimeoutError:
            raise TimeoutError('Page refresh timed out')

    async def get_window_id(self):
        """
        Retrieves the ID of the current browser window.

        Returns:
            str: The ID of the current browser window.
        """
        response = await self._execute_command(BrowserCommands.get_window_id())
        return response['result']['windowId']

    async def set_window_bounds(self, bounds: dict):
        """
        Sets the bounds of the specified window.

        Args:
            bounds (dict): The bounds to set for the window.
        """
        window_id = await self.get_window_id()
        await self._execute_command(
            BrowserCommands.set_window_bounds(window_id, bounds)
        )

    async def set_window_maximized(self):
        """
        Maximizes the specified window.
        """
        window_id = await self.get_window_id()
        await self._execute_command(
            BrowserCommands.set_window_maximized(window_id)
        )

    async def set_window_minimized(self):
        """
        Minimizes the specified window.
        """
        window_id = await self.get_window_id()
        await self._execute_command(
            BrowserCommands.set_window_minimized(window_id)
        )

    async def print_to_pdf(self, path: str):
        """
        Prints the current page to a PDF file and saves it to the specified path.

        Args:
            path (str): The file path where the PDF will be saved.
        """
        response = await self._execute_command(PageCommands.print_to_pdf())
        pdf_b64 = response['result']['data'].encode('utf-8')
        pdf_bytes = decode_image_to_bytes(pdf_b64)
        with open(path, 'wb') as file:
            file.write(pdf_bytes)

    async def find_element(self, by: DomCommands.SelectorType, value: str):
        """
        Finds an element on the current page using the specified selector.

        Args:
            by (str): The type of selector to use (e.g., 'css', 'xpath').
            value (str): The value of the selector to use.

        Returns:
            dict: The response from the browser.
        """
        root_node_id = await self._get_root_node_id()
        response = await self._execute_command(
            DomCommands.find_element(root_node_id, by, value)
        )
        target_node_id = response['result']['nodeId']
        node_description = await self._describe_node(target_node_id)
        return WebElement(node_description, self.connection_handler)

    async def on(self, event_name: str, callback: Callable, temporary: bool = False):
        """
        Registers an event callback for a specific event.

        Args:
            event_name (str): Name of the event to listen for.
            callback (Callable): function to be called when the event occurs.
        """
        await self.connection_handler.register_callback(event_name, callback, temporary)

    async def _is_browser_running(self):
        """
        Checks if the browser process is currently running.
        Attempts to connect to the browser to verify its status.

        Returns:
            bool: True if the browser is running, False otherwise.
        """
        for _ in range(10):
            if await self._check_browser_connection():
                return True
            await asyncio.sleep(1)
        return False

    async def _check_browser_connection(self):
        """
        Checks if the browser process is currently running.

        Returns:
            bool: True if the browser is running, False otherwise.
        """
        try:
            await self.connection_handler.browser_ws_address
            return True
        except Exception as exc:
            print(f'Browser is not running: {exc}')
            return False

    async def _execute_command(self, command: str):
        """
        Executes a command through the connection handler.

        Args:
            command (str): The command to be executed.

        Returns:
            The response from executing the command.
        """
        return await self.connection_handler.execute_command(command)
    
    async def _get_root_node_id(self):
        """
        Retrieves the root node ID of the current page.

        Returns:
            int: The ID of the root node.
        """
        response = await self._execute_command(DomCommands.dom_document())
        return response['result']['root']['nodeId']

    async def _describe_node(self, node_id: int):
        """
        Describes a node on the current page.

        Args:
            node_id (int): The ID of the node to describe.
        
        Returns:
            dict: The description of the node.
        """
        response = await self._execute_command(
            DomCommands.describe_node(node_id)
        )
        return response['result']['node']
    
    async def _wait_page_loaded(self):
        """
        Waits for the page to finish loading.

        Raises:
            asyncio.TimeoutError: If the page load times
            out after 300 seconds.
        """
        page_loaded = asyncio.Event()
        await self.on(PageEvents.PAGE_LOADED, lambda _: page_loaded.set(), temporary=True)
        await asyncio.wait_for(page_loaded.wait(), timeout=300)
    
    async def _enable_page_events(self):
        await self.connection_handler.execute_command(
            PageCommands.enable_page()
        )
    
    @staticmethod
    def _validate_browser_path(path: str):
        """
        Validates the provided browser path.

        Args:
            path (str): The file path to the browser executable.

        Raises:
            ValueError: If the browser path does not exist.

        Returns:
            str: The validated browser path.
        """
        if not os.path.exists(path):
            raise ValueError(f'Browser not found: {path}')
        return path

    @staticmethod
    def _initialize_options(options: Options | None) -> Options:
        """
        Initializes the options for the browser.

        Args:
            options (Options | None): An instance of the Options class or None.

        Raises:
            ValueError: If the provided options are invalid.

        Returns:
            Options: The initialized options instance.
        """
        if options is None:
            return Options()
        if not isinstance(options, Options):
            raise ValueError('Invalid options')
        return options

    @abstractmethod
    def _get_default_binary_location(self) -> str:
        """
        Retrieves the default location of the browser binary.

        This method must be implemented by subclasses.
        """
        pass
