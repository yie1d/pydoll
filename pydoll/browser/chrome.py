import platform
from typing import Optional

from pydoll.browser.base import Browser
from pydoll.browser.managers import BrowserOptionsManager
from pydoll.browser.options import Options


class Chrome(Browser):
    def __init__(
        self,
        options: Optional[Options] = None,
        connection_port: Optional[int] = None,
    ):
        super().__init__(options, connection_port)

    @staticmethod
    def _get_default_binary_location():
        os_name = platform.system()
        browser_paths = {
            'Windows':
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'Linux':
                '/usr/bin/google-chrome',
            'Darwin':
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        }

        browser_path = browser_paths.get(os_name)

        if not browser_path:
            raise ValueError('Unsupported OS')

        return BrowserOptionsManager.validate_browser_path(
            browser_path
        )
