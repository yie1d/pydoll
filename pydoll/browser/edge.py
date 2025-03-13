import os
import platform
from typing import Optional

from pydoll.browser.base import Browser
from pydoll.browser.managers import BrowserOptionsManager
from pydoll.browser.options import EdgeOptions, Options


class Edge(Browser):
    def __init__(
        self, options: Options | None = None, connection_port: int = 9222
    ):
        if options is None:
            options = EdgeOptions()
        # Initialize base class with options and port
        super().__init__(options, connection_port)
        

    @staticmethod
    def _get_default_binary_location():
        """
        Get the default Edge browser binary location based on the operating system.
        
        Returns:
            str: Path to the Edge browser executable
            
        Raises:
            ValueError: If the operating system is not supported
        """
        os_name = platform.system()
        browser_paths = {
            'Windows':
                r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'Linux':
                '/usr/bin/microsoft-edge',
            'Darwin':
                '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
        }

        browser_path = browser_paths.get(os_name)

        if not browser_path:
            raise ValueError('Unsupported operating system')

        return BrowserOptionsManager.validate_browser_path(
            browser_path
        )