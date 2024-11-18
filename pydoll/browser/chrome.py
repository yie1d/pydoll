import os

from pydoll.browser.base import Browser
from pydoll.browser.options import Options


class Chrome(Browser):
    def __init__(
        self, options: Options | None = None, connection_port: int = 9222
    ):
        super().__init__(options, connection_port)

    def _get_default_binary_location(self):
        os_name = os.name
        match os_name:
            case 'nt':
                browser_path = (
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe'
                )
                return self._validate_browser_path(browser_path)
            case 'posix':
                browser_path = '/usr/bin/google-chrome'
                return self._validate_browser_path(browser_path)
            case _:
                raise ValueError('Unsupported OS')
