import asyncio
import os
import subprocess
from typing import Callable
from abc import ABC, abstractmethod

from pydoll.browser.options import Options
from pydoll.commands.browser import BrowserCommands
from pydoll.connection import ConnectionHandler


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
        self.options = self._initialize_options(options)
        self.process = self._start_browser()
        self.connection_handler = ConnectionHandler()

    def start(self) -> subprocess.Popen:
        """
        Starts the browser process with the specified options.

        Returns:
            subprocess.Popen: The process object for the started browser.
        """
        binary_location = (
            self.options.binary_location or self._get_default_binary_location()
        )
        return subprocess.Popen(
            [binary_location, '--remote-debugging-port=9222', *self.options.arguments],
            stdout=subprocess.PIPE,
        )

    def stop(self):
        """
        Stops the running browser process.

        Raises:
            ValueError: If the browser is not currently running.
        """
        if self._is_browser_running():
            self.process.terminate()
            self._execute_sync_command(BrowserCommands.CLOSE)
        else:
            raise ValueError('Browser is not running')

    def get_screenshot(self, path: str):
        """
        Captures a screenshot of the current page and saves
        it to the specified path.

        Args:
            path (str): The file path where the screenshot will be saved.
        """
        response = self._execute_sync_command(BrowserCommands.SCREENSHOT)
        image_bytes = response['result']['data'].encode('utf-8')
        with open(path, 'wb') as file:
            file.write(image_bytes)

    def on(self, event_name: str, callback: Callable):
        """
        Registers an event callback for a specific event.

        Args:
            event_name (str): Name of the event to listen for.
            callback (Callable): function to be called when the event occurs.
        """
        asyncio.run(
            self.connection_handler.register_callback(event_name, callback)
        )

    def _start_browser(self) -> subprocess.Popen:
        """
        Starts the browser and verifies if it is running.

        Raises:
            ValueError: If the browser fails to start.

        Returns:
            subprocess.Popen: The process object for the started browser.
        """
        process = self.start()
        if not self._is_browser_running():
            raise ValueError('Failed to start browser')
        return process

    @abstractmethod
    def _get_default_binary_location(self) -> str:
        """
        Retrieves the default location of the browser binary.

        This method must be implemented by subclasses.
        """
        pass

    def _is_browser_running(self):
        """
        Checks if the browser process is currently running.

        Returns:
            bool: True if the browser is running, False otherwise.
        """
        return self.process.poll() is None

    def _execute_sync_command(self, command: str):
        """
        Executes a command synchronously through the connection handler.

        Args:
            command (str): The command to be executed.

        Returns:
            The response from executing the command.
        """
        return asyncio.run(self.connection_handler.execute_command(command))

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
