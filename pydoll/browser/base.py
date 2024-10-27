import asyncio
import os
import subprocess
from typing import Callable

from pydoll.browser.options import Options
from pydoll.connection import ConnectionHandler


class Browser:
    def __init__(self, options: Options | None = None):
        self.options = self._initialize_options(options)
        self.process = self._start_browser()
        self.connection_handler = ConnectionHandler()

    def start(self) -> subprocess.Popen:
        args_str = ' '.join(self.options.arguments)
        binary_location = (
            self.options.binary_location or self._get_default_binary_location()
        )
        return subprocess.Popen(
            f'{binary_location} --remote-debugging-port=9222 {args_str}',
            shell=True,
        )

    def stop(self):
        if self._is_browser_running():
            self.process.terminate()
            self._execute_sync_command({'method': 'Browser.close'})
        else:
            raise ValueError('Browser is not running')

    def get_screenshot(self, path: str):
        command = {
            'method': 'Page.captureScreenshot',
            'params': {'format': 'png'},
        }
        response = self._execute_sync_command(command)
        image_bytes = response['result']['data'].encode('utf-8')
        with open(path, 'wb') as file:
            file.write(image_bytes)

    def on(self, event_name: str, callback: Callable):
        asyncio.run(
            self.connection_handler.register_callback(event_name, callback)
        )

    def _start_browser(self) -> subprocess.Popen:
        process = self.start()
        if not self._is_browser_running():
            raise ValueError('Failed to start browser')
        return process

    def _get_default_binary_location(self) -> str:
        raise NotImplementedError('Method must be implemented')

    def _is_browser_running(self):
        return self.process.poll() is None
    
    def _execute_sync_command(self, command: str):
        return asyncio.run(self.connection_handler.execute_command(command))

    @staticmethod
    def _validate_browser_path(path: str):
        if not os.path.exists(path):
            raise ValueError(f'Browser not found: {path}')
        return path

    @staticmethod
    def _initialize_options(options: Options | None) -> Options:
        if options is None:
            return Options()
        if not isinstance(options, Options):
            raise ValueError('Invalid options')
        return options
