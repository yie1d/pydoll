import os
import platform

from pydoll.browser.base import Browser
from pydoll.browser.managers import BrowserOptionsManager
from pydoll.browser.options import Options


class Edge(Browser):
    def __init__(
        self, options: Options | None = None, connection_port: int = 9222
    ):
        if options is None:
            options = Options()
            
        # Add Edge-specific startup arguments
        options.add_argument('--no-first-run')  # Disable first run experience
        options.add_argument('--no-default-browser-check')  # Disable default browser check
        options.add_argument('--disable-crash-reporter')  # Disable crash reporting
        options.add_argument('--disable-features=TranslateUI')  # Disable translation UI
        options.add_argument('--disable-component-update')  # Disable component updates
        options.add_argument('--disable-background-networking')  # Disable background networking
        
        # Add debugging parameters
        options.add_argument(f'--remote-debugging-port={connection_port}')
        options.add_argument('--remote-allow-origins=*')

        # Set default user data directory if not already set
        if not any('--user-data-dir=' in arg for arg in options.arguments):
            user_data_dir = os.path.join(os.path.expanduser('~'), '.edge_automation')
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f'--user-data-dir={user_data_dir}')

        # Initialize base class first so we can use its methods
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