import asyncio
import os
import subprocess
from abc import ABC, abstractmethod
from functools import partial
from random import randint
from tempfile import TemporaryDirectory
from typing import Callable

import aiofiles

from pydoll import exceptions
from pydoll.browser.options import Options
from pydoll.commands.browser import BrowserCommands
from pydoll.commands.dom import DomCommands
from pydoll.commands.fetch import FetchCommands
from pydoll.commands.network import NetworkCommands
from pydoll.commands.page import PageCommands
from pydoll.connection import ConnectionHandler
from pydoll.element import WebElement
from pydoll.events.fetch import FetchEvents
from pydoll.events.page import PageEvents
from pydoll.utils import decode_image_to_bytes


class Browser(ABC):
    """
    A class to manage a browser instance for automated interactions.

    This class allows users to start and stop a browser, take screenshots,
    and register event callbacks.
    """

    def __init__(
        self, options: Options | None = None, connection_port: int = None
    ):
        """
        Initializes the Browser instance.

        Args:
            options (Options | None): An instance of the Options class to
            configure the browser. If None, default options will be used.
        """
        self._connection_port = (
            connection_port if connection_port else randint(9223, 9322)
        )
        self.connection_handler = ConnectionHandler(self._connection_port)
        self.options = self._initialize_options(options)
        self.process = None
        self.temp_dirs = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        for temp_dir in self.temp_dirs:
            temp_dir.cleanup()
        self.connection_handler.close()

    async def start(self) -> None:
        """
        Starts the browser process with the specified options, including any proxy configurations.

        This method initializes and launches the browser, setting up the necessary command-line
        arguments and options. It checks for a specified user data directory, creates a temporary
        directory if none is provided, and configures the browser to run in a controlled environment.

        If a private proxy is specified in the options, this method sets up the necessary
        event listeners to handle network requests and authentication. The browser will pause
        network requests that require authentication and will allow for continuing those requests
        using the provided proxy credentials.

        The proxy configuration process is as follows:
        1. The `_configure_proxy()` method is called to check if any proxy server has been defined in the
        command-line arguments. If a proxy is detected, it extracts the server address and, if necessary,
        the authentication credentials (username and password).
        2. When the browser is started, if the private proxy is enabled:
        - The `enable_fetch_events` method is called with the argument `handle_auth_requests=True`.
            This allows the browser to intercept network requests and pause them if authentication is needed.
        - An event listener is set up for the `FetchEvents.REQUEST_PAUSED` event. This listener
            calls the `_continue_request()` method, which is responsible for resuming requests that have been paused.
        - Another event listener is set up for the `FetchEvents.AUTH_REQUIRED` event. This listener calls the
            `_continue_request_auth_required()` method, passing the extracted proxy credentials to handle
            authentication when required.

        Returns:
            subprocess.Popen: The process object for the started browser.
        """
        binary_location = (
            self.options.binary_location or self._get_default_binary_location()
        )

        temp_dir = self._get_temp_dir()

        if '--user-data-dir' not in self.options.arguments:
            self.options.arguments.append(f'--user-data-dir={temp_dir.name}')
            self.options.arguments.append('--no-first-run')
            self.options.arguments.append('--no-default-browser-check')

        private_proxy, proxy_credentials = self._configure_proxy()

        self.process = subprocess.Popen(
            [
                binary_location,
                f'--remote-debugging-port={self._connection_port}',
                *self.options.arguments,
            ],
            stdout=subprocess.PIPE,
        )
        if not await self._is_browser_running():
            raise exceptions.BrowserNotRunning('Failed to start browser')

        await self.enable_page_events()

        if private_proxy:
            await self.enable_fetch_events(
                handle_auth_requests=True, resource_type='Document'
            )
            await self.on(
                FetchEvents.REQUEST_PAUSED,
                self._continue_request,
                temporary=True,
            )
            # need to use partial to pass the proxy credentials to the callback as a coroutine argument
            await self.on(
                FetchEvents.AUTH_REQUIRED,
                partial(
                    self._continue_request_auth_required,
                    proxy_username=proxy_credentials[0],
                    proxy_password=proxy_credentials[1],
                ),
                temporary=True,
            )

    async def execute_js_script(self, script: str):
        """
        Executes a JavaScript script in the browser.

        Args:
            script (str): The JavaScript script to execute.

        Returns:
            The response from executing the script.
        """
        command = {
            'method': 'Runtime.evaluate',
            'params': {'expression': script, 'returnByValue': True},
        }
        return await self._execute_command(command)

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
            raise exceptions.BrowserNotRunning('Browser is not running')

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
        async with aiofiles.open(path, 'wb') as file:
            await file.write(image_bytes)

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
        async with aiofiles.open(path, 'wb') as file:
            await file.write(pdf_bytes)

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

    async def on(
        self, event_name: str, callback: Callable, temporary: bool = False
    ):
        """
        Registers an event callback for a specific event. If the callback is
        a coroutine, it will be wrapped in a task to avoid blocking the event loop.
        Otherwise, the callback will be used directly.

        Args:
            event_name (str): Name of the event to listen for.
            callback (Callable): function to be called when the event occurs.
        """

        async def callback_wrapper(event):
            asyncio.create_task(callback(event))

        if asyncio.iscoroutinefunction(callback):
            function_to_register = callback_wrapper
        else:
            function_to_register = callback

        await self.connection_handler.register_callback(
            event_name, function_to_register, temporary
        )

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
        return await self.connection_handler.execute_command(
            command, timeout=60
        )

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

    async def _describe_node(self, node_id: int):
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
        await self.on(
            PageEvents.PAGE_LOADED, lambda _: page_loaded.set(), temporary=True
        )
        await asyncio.wait_for(page_loaded.wait(), timeout=300)

    def _configure_proxy(self) -> tuple[bool, tuple[str, str]]:
        """
        Configures the proxy settings for the browser. If the proxy
        is private, the credentials will be extracted from the proxy
        string and returned.

        Returns:
            tuple[bool, tuple[str, str]]: A tuple containing a boolean
            indicating if the proxy is private and a tuple with the proxy
            username and password
        """
        private_proxy = False
        proxy_username, proxy_password = None, None

        if any('--proxy-server' in arg for arg in self.options.arguments):
            proxy_index = next(
                index
                for index, arg in enumerate(self.options.arguments)
                if '--proxy-server' in arg
            )
            proxy = self.options.arguments[proxy_index].replace(
                '--proxy-server=', ''
            )

            if '@' in proxy:
                credentials, proxy_server = proxy.split('@')
                self.options.arguments[proxy_index] = (
                    f'--proxy-server={proxy_server}'
                )
                proxy_username, proxy_password = credentials.split(':')
                private_proxy = True

        return private_proxy, (proxy_username, proxy_password)

    async def _continue_request(self, event: dict):
        """
        Resumes a network request that was previously paused in the browser.
        When the Fetch domain is active, certain requests can be paused based
        on the specified resource type. This method takes the event data that
        contains the request ID and uses it to continue the paused request,
        allowing the browser to proceed with the network operation. This is
        particularly useful for handling requests that require conditional logic
        before they are sent to the server.

        Args:
            event (dict): A dictionary containing the event data, including
            the request ID, which identifies the paused request to be resumed.

        Returns:
            None
        """
        request_id = event['params']['requestId']
        await self._execute_command(FetchCommands.continue_request(request_id))

    async def _continue_request_auth_required(
        self, event: dict, proxy_username: str, proxy_password: str
    ):
        """
        Resumes a network request that was previously paused in the browser
        and requires proxy authentication. This method is triggered when an
        authentication challenge is encountered during the request handling.
        It uses the provided proxy credentials to continue the request, enabling
        successful communication through the proxy server. After handling the
        request, it disables fetch event monitoring.

        Args:
            event (dict): A dictionary containing the event data, which includes
            the request ID for the paused request that needs to be resumed.
            proxy_username (str): The username for the proxy server
            authentication.
            proxy_password (str): The password for the proxy server
            authentication.

        Raises:
            IndexError: If the event data does not contain a valid request ID.

        Returns:
            None
        """
        request_id = event['params']['requestId']
        await self._execute_command(
            FetchCommands.continue_request_with_auth(
                request_id, proxy_username, proxy_password
            )
        )
        await self.disable_fetch_events()

    async def enable_page_events(self):
        """
        Enables listening for page-related events over the websocket connection.
        Once this method is invoked, the connection will emit events pertaining
        to page activities, such as loading, navigation, and DOM updates, to any
        registered event callbacks. For a comprehensive list of available page
        events and their purposes, refer to the PageEvents class documentation.
        This functionality is crucial for monitoring and reacting to changes
        in the page state in real-time.

        Returns:
            None
        """
        await self.connection_handler.execute_command(
            PageCommands.enable_page()
        )

    async def enable_network_events(self):
        """
        Activates listening for network events through the websocket connection.
        After calling this method, the connection will emit events related
        to network activities, such as resource loading and response status,
        to any registered event callbacks. This is essential for debugging
        network interactions and analyzing resource requests. For details
        on available network events, consult the NetworkEvents class documentation.

        Returns:
            None
        """
        await self.connection_handler.execute_command(
            NetworkCommands.enable_network_events()
        )

    async def enable_fetch_events(
        self, handle_auth_requests: bool = False, resource_type: str = ''
    ):
        """
        Enables the Fetch domain for intercepting network requests before they
        are sent. This method allows you to modify, pause, or continue requests
        as needed. If handle_auth_requests is set to True, the connection will
        emit an event when an authentication is required during a request.
        The resource_type parameter specifies which type of requests to intercept;
        if omitted, all requests will be intercepted. Use the _continue_request
        method to resume any paused requests. This is especially useful for
        monitoring and controlling network interactions.

        Args:
            handle_auth_requests (bool): Whether to handle authentication
            requests that require user credentials.
            resource_type (str): The type of resource to intercept (e.g.,
            'XHR', 'Script'). If not specified, all requests will be intercepted.

        Returns:
            None
        """
        await self.connection_handler.execute_command(
            FetchCommands.enable_fetch_events(
                handle_auth_requests, resource_type
            )
        )

    async def enable_dom_events(self):
        """
        Enables DOM-related events for the websocket connection. When invoked,
        this method allows the connection to listen for changes in the DOM,
        including node additions, removals, and attribute changes. This feature
        is vital for applications that need to react to dynamic changes in
        the page structure. For a full list of available DOM events, refer to
        the DomCommands class documentation.

        Returns:
            None
        """
        await self.connection_handler.execute_command(
            DomCommands.enable_dom_events()
        )

    async def disable_fetch_events(self):
        """
        Deactivates the Fetch domain, stopping the interception of network
        requests for the websocket connection. Once this method is called,
        the connection will no longer monitor or pause any network requests,
        allowing normal network operations to resume. This can be useful when
        you want to halt the monitoring of network activity.

        Returns:
            None
        """
        await self.connection_handler.execute_command(
            FetchCommands.disable_fetch_events()
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

    def _get_temp_dir(self):
        """
        Retrieves a temporary directory for the browser instance.

        Returns:
            TemporaryDirectory: The temporary directory.
        """
        temp_dir = TemporaryDirectory()
        self.temp_dirs.append(temp_dir)
        return temp_dir

    @abstractmethod
    def _get_default_binary_location(self) -> str:
        """
        Retrieves the default location of the browser binary.

        This method must be implemented by subclasses.
        """
        pass
