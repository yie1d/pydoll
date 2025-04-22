class ProxyManager:
    def __init__(self, options):
        """
        Initializes the ProxyManager with browser options.

        This manager handles proxy configuration for the browser,
        including extraction and management of proxy credentials.

        Args:
            options: The browser options instance containing arguments.
        """
        self.options = options

    def get_proxy_credentials(self) -> tuple[bool, tuple[str, str]]:
        """
        Configures proxy settings and extracts credentials if present.

        This method searches for proxy settings in the browser options,
        extracts any credentials, and updates the proxy arguments to use
        a clean proxy URL without embedded credentials.

        Returns:
            tuple[bool, tuple[str, str]]: A tuple containing:
                - bool: True if private proxy with credentials was found
                - tuple[str, str]: Username and password for proxy
                    authentication
        """
        private_proxy = False
        credentials = (None, None)

        proxy_arg = self._find_proxy_argument()

        if proxy_arg is not None:
            index, proxy_value = proxy_arg
            has_credentials, username, password, clean_proxy = (
                self._parse_proxy(proxy_value)
            )

            if has_credentials:
                self._update_proxy_argument(index, clean_proxy)
                private_proxy = True
                credentials = (username, password)

        return private_proxy, credentials

    def _find_proxy_argument(self) -> tuple[int, str] | None:
        """
        Finds the first valid --proxy-server argument in browser options.

        This method iterates through the browser arguments looking for
        a proxy server configuration.

        Returns:
            tuple[int, str] | None: A tuple containing the index of the
                argument and the proxy value if found, None otherwise.
        """
        for index, arg in enumerate(self.options.arguments):
            if arg.startswith('--proxy-server='):
                return index, arg.split('=', 1)[1]
        return None

    @staticmethod
    def _parse_proxy(proxy_value: str) -> tuple[bool, str, str, str]:
        """
        Extracts credentials from proxy value and cleans the proxy string.

        This method parses a proxy URL to extract embedded credentials
        (if present) in the format username:password@server.

        Args:
            proxy_value (str): The proxy URL potentially containing
                credentials.

        Returns:
            tuple[bool, str, str, str]: A tuple containing:
                - bool: True if credentials were found
                - str: Username (or None if no credentials)
                - str: Password (or None if no credentials)
                - str: Clean proxy URL without credentials
        """
        if '@' not in proxy_value:
            return False, None, None, proxy_value

        try:
            creds_part, server_part = proxy_value.split('@', 1)
            username, password = creds_part.split(':', 1)
            return True, username, password, server_part
        except ValueError:
            return False, None, None, proxy_value

    def _update_proxy_argument(self, index: int, clean_proxy: str) -> None:
        """
        Updates the options arguments list with the clean proxy URL.

        This method replaces the original proxy argument (which may have
        contained credentials) with a clean version that doesn't expose
        sensitive data.

        Args:
            index (int): The index of the proxy argument to update.
            clean_proxy (str): The proxy URL without credentials.

        Returns:
            None
        """
        self.options.arguments[index] = f'--proxy-server={clean_proxy}'
