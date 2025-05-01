import os

from pydoll.browser.options import ChromeOptions, EdgeOptions, Options
from pydoll.constants import BrowserType


class BrowserOptionsManager:
    @staticmethod
    def initialize_options(options: Options | None, browser_type: BrowserType = None) -> Options:
        """
        Initialize browser options based on browser type.

        Creates a new options instance based on browser type if none
        is provided, or validates and returns the provided
        options instance.

        Args:
            options (Options | None): Browser options instance.
            If None, a new instance
                will be created based on browser_type
            browser_type (BrowserType): Type of browser, used to create
            appropriate options instance

        Returns:
            Options: The initialized browser options instance

        Raises:
            ValueError: If provided options is not an instance
            of Options class
        """
        if options is None:
            if browser_type == BrowserType.CHROME:
                return ChromeOptions()
            elif browser_type == BrowserType.EDGE:
                return EdgeOptions()
            else:
                return Options()

        if not isinstance(options, Options):
            raise ValueError('Invalid options')

        return options

    @staticmethod
    def add_default_arguments(options: Options):
        """Adds default arguments to the provided options"""
        options.arguments.append('--no-first-run')
        options.arguments.append('--no-default-browser-check')

        # Add browser-specific arguments based on options type
        if isinstance(options, EdgeOptions):
            BrowserOptionsManager._add_edge_arguments(options)
        elif isinstance(options, ChromeOptions):
            BrowserOptionsManager._add_chrome_arguments(options)

    @staticmethod
    def _add_edge_arguments(options: Options):
        """Adds Edge-specific arguments to the options"""
        options.add_argument('--disable-crash-reporter')
        options.add_argument('--disable-features=TranslateUI')
        options.add_argument('--disable-component-update')
        options.add_argument('--disable-background-networking')
        options.add_argument('--remote-allow-origins=*')

    @staticmethod
    def _add_chrome_arguments(options: Options):
        """Adds Chrome-specific arguments to the options"""
        options.add_argument('--remote-allow-origins=*')
        # Add other Chrome-specific arguments here

    @staticmethod
    def validate_browser_paths(paths: list[str]) -> str:
        """
        Validates the provided browser executable path.

        This method checks if the browser executable file exists at
        the specified path.

        Args:
            paths (list[str]): Lista de caminhos possíveis do navegador.


        Returns:
            str: The validated browser path if it exists.

        Raises:
            ValueError: If the browser executable is not found at the path.
        """
        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        raise ValueError(f'No valid browser path found in: {paths}')
