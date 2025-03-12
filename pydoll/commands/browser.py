class BrowserCommands:
    """
    BrowserCommands class provides a set of commands to interact with the
    browser's main functionality based on CDP. These commands allow for
    managing browser windows, such as closing windows, retrieving window IDs,
    and adjusting window bounds (size and state).

    The following operations can be performed:
    - Close the browser.
    - Get the ID of the current window.
    - Set the size and position of a specific window.
    - Maximize or minimize a specific window.

    Each method generates a command that can be sent to the browser
    as part of the communication with the browser's underlying API.
    """

    CLOSE = {'method': 'Browser.close'}
    GET_WINDOW_ID = {'method': 'Browser.WindowID'}
    GET_WINDOW_ID_BY_TARGET = {
        'method': 'Browser.getWindowForTarget',
        'params': {},
    }
    SET_WINDOW_BOUNDS_TEMPLATE = {
        'method': 'Browser.setWindowBounds',
        'params': {},
    }
    SET_DOWNLOAD_BEHAVIOR = {
        'method': 'Browser.setDownloadBehavior',
        'params': {},
    }

    @classmethod
    def set_download_path(cls, path: str) -> dict:
        """
        Generates the command to set the download path for the browser.

        Args:
            path (str): The path to set for downloads.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.SET_DOWNLOAD_BEHAVIOR.copy()
        command['params']['behavior'] = 'allow'
        command['params']['downloadPath'] = path
        return command

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
    def get_window_id_by_target(cls, target_id: str) -> dict:
        """
        Generates the command to get the ID of the current window.

        Args:
            target_id (str): The target_id to set for the window.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.GET_WINDOW_ID_BY_TARGET.copy()
        command['params']['targetId'] = target_id
        return command

    @classmethod
    def set_window_bounds(cls, window_id: int, bounds: dict) -> dict:
        """
        Generates the command to set the bounds of a window.

        Args:
            window_id (int): The ID of the window to set the bounds for.
            bounds (dict): The bounds to set for the window,
                           which should include width, height,
                           and optionally x and y coordinates.

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
