from typing import Optional

from pydoll.browser.interfaces import BrowserOptionsManager, Options
from pydoll.browser.options import ChromiumOptions
from pydoll.exceptions import InvalidOptionsObject


class ChromiumOptionsManager(BrowserOptionsManager):
    """
    Manages browser options configuration for CDP-based browser automation.

    This utility class provides static methods for handling browser options across
    different browser types (Chrome, Edge) while ensuring proper defaults and
    compatibility settings are applied. It centralizes options management to:

    1. Create appropriate browser-specific options objects
    2. Apply default arguments needed for CDP integration
    3. Validate browser binary locations
    4. Handle browser-specific configuration needs

    The class works closely with the Options hierarchy (Options base class and
    browser-specific subclasses like ChromeOptions and EdgeOptions) to ensure
    proper configuration for each browser type.
    """

    def __init__(self, options: Optional[Options] = None):
        self.options = options

    def initialize_options(
        self,
    ) -> ChromiumOptions:
        """
        Initializes browser options.

        Creates a new appropriate options instance if none is provided, or validates
        and returns the existing options instance. This ensures that proper
        browser-specific options are available for browser initialization.

        Args:
            options: Existing Options instance to use. If None, a new instance
                will be created.

        Returns:
            ChromiumOptions: A properly initialized browser options instance.

        Raises:
            InvalidOptionsObject: If provided options is not an instance
                of ChromiumOptions class
        """
        if self.options is None:
            self.options = ChromiumOptions()

        if not isinstance(self.options, ChromiumOptions):
            raise InvalidOptionsObject(f'Expected ChromiumOptions, got {type(self.options)}')

        self.add_default_arguments()
        return self.options

    def add_default_arguments(self):
        """
        Adds default arguments required for proper CDP integration.

        Applies universal and browser-specific arguments to ensure proper
        functionality of the CDP connection and browser behavior. These arguments
        minimize prompts, disable unnecessary features, and configure security
        settings for automation.

        Args:
            options: The Options instance to modify with default arguments.

        Note:
            This method modifies the options object in-place by appending
            to its arguments list. It detects the specific browser type
            by examining the options class type.
        """
        self.options.arguments.append('--no-first-run')
        self.options.arguments.append('--no-default-browser-check')
