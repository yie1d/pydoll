class BrowserCommands:
    """
    A class to define the available commands to use in the
    Browser main class.
    """

    CLOSE = {'method': 'Browser.close'}
    GET_WINDOW_ID = {'method': 'Browser.WindowID'}
    SET_WINDOW_BOUNDS_TEMPLATE = {
        'method': 'Browser.setWindowBounds',
        'params': {},
    }

    @classmethod
    def close(cls) -> dict:
        """
        Generates the command to close the browser.

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.CLOSE

    @classmethod
    def get_window_id(cls) -> dict:
        """
        Generates the command to get the ID of the current window.

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.GET_WINDOW_ID

    @classmethod
    def set_window_bounds(cls, window_id: int, bounds: dict) -> dict:
        """
        Generates the command to set the bounds of a window.

        Args:
            window_id (int): The ID of the window to set the bounds for.
            bounds (dict): The bounds to set for the window.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.SET_WINDOW_BOUNDS_TEMPLATE.copy()
        command['params']['windowId'] = window_id
        command['params']['bounds'] = bounds
        return command

    @classmethod
    def set_window_maximized(cls, window_id: int) -> dict:
        """
        Generates the command to maximize a window.

        Args:
            window_id (int): The ID of the window to maximize.

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.set_window_bounds(window_id, {'windowState': 'maximized'})

    @classmethod
    def set_window_minimized(cls, window_id: int) -> dict:
        """
        Generates the command to minimize a window.

        Args:
            window_id (int): The ID of the window to minimize.

        Returns:
            dict: The command to be sent to the browser.
        """
        return cls.set_window_bounds(window_id, {'windowState': 'minimized'})
