class StorageCommands:
    """
    A class for interacting with browser storage using
    Chrome DevTools Protocol.

    This class provides methods to create commands for managing cookies
    in the browser, including retrieving, setting, and clearing cookies
    through CDP commands.

    Attributes:
        CLEAR_COOKIES (dict): Template for the Storage.clearCookies command.
        SET_COOKIES (dict): Template for the Storage.setCookies command.
        GET_COOKIES (dict): Template for the Storage.getCookies command.
    """

    CLEAR_COOKIES = {'method': 'Storage.clearCookies', 'params': {}}
    SET_COOKIES = {'method': 'Storage.setCookies', 'params': {}}
    GET_COOKIES = {'method': 'Storage.getCookies', 'params': {}}

    @classmethod
    def clear_cookies(cls) -> dict:
        """
        Generates a command to clear all browser cookies.

        Returns:
            dict: The CDP command to clear all cookies.
        """
        return cls.CLEAR_COOKIES

    @classmethod
    def set_cookies(cls, cookies: list) -> dict:
        """
        Generates a command to set browser cookies.

        Args:
            cookies (list): A list of cookie objects to be set in the browser.
                Each cookie object should follow the CDP cookie format.

        Returns:
            dict: The CDP command to set the specified cookies.
        """
        set_cookies = cls.SET_COOKIES.copy()
        set_cookies['params']['cookies'] = cookies
        return set_cookies

    @classmethod
    def get_cookies(cls) -> dict:
        """
        Generates a command to retrieve all browser cookies.

        Returns:
            dict: The CDP command to get all cookies.
        """
        return cls.GET_COOKIES
