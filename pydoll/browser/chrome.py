import os
import platform

from pydoll.browser.base import Browser
from pydoll.browser.managers import BrowserOptionsManager
from pydoll.browser.options import Options


class Chrome(Browser):
    def __init__(
        self, options: Options | None = None, connection_port: int = 9222
    ):
        super().__init__(options, connection_port)

    @staticmethod
    def _get_default_binary_location():
        os_name = platform.system()

        if os_name == 'Windows':
            possible_paths = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return BrowserOptionsManager.validate_browser_path(path)
            raise ValueError("Chrome not found in default Windows locations.")
        elif os_name == 'Linux':
            browser_path = '/usr/bin/google-chrome'
        elif os_name == 'Darwin':
            browser_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        else:
            raise ValueError('Unsupported OS')

        return BrowserOptionsManager.validate_browser_path(browser_path)
