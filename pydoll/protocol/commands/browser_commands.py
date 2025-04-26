from copy import deepcopy

from pydoll.protocol.types.commands.browser import (
    GetWindowForTargetParams,
    SetDownloadBehaviorParams,
    SetWindowBoundsParams,
    WindowBoundsDict,
    WindowState,
    DownloadBehavior
)
from pydoll.protocol.types.commands.common import Command
from pydoll.protocol.types.responses.common import Response
from pydoll.protocol.types.responses.browser import GetWindowForTargetResponse


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

    CLOSE = Command(method='Browser.close')
    GET_WINDOW_ID_BY_TARGET = Command(method='Browser.getWindowForTarget')
    SET_WINDOW_BOUNDS_TEMPLATE = Command(method='Browser.setWindowBounds')
    SET_DOWNLOAD_BEHAVIOR = Command(method='Browser.setDownloadBehavior')

    @classmethod
    def set_download_path(cls, path: str) -> Command[Response]:
        """
        Generates the command to set the download path for the browser.

        Args:
            path (str): The path to set for downloads.

        Returns:
            Command: The command to be sent to the browser.
        """
        command = deepcopy(cls.SET_DOWNLOAD_BEHAVIOR)
        params = SetDownloadBehaviorParams(
            behavior=DownloadBehavior.ALLOW,
            downloadPath=path
        )
        command['params'] = params
        return command

    @classmethod
    def close(cls) -> Command[Response]:
        """
        Generates the command to close the browser.

        Returns:
            Command: The command to be sent to the browser.
        """
        return cls.CLOSE

    @classmethod
    def get_window_id_by_target(cls, target_id: str) -> Command[GetWindowForTargetResponse]:
        """
        Generates the command to get the ID of the current window.

        Args:
            target_id (str): The target_id to set for the window.

        Returns:
            Command: The command to be sent to the browser.
        """
        command = deepcopy(cls.GET_WINDOW_ID_BY_TARGET)
        params = GetWindowForTargetParams(targetId=target_id)
        command['params'] = params
        return command

    @classmethod
    def set_window_bounds(cls, window_id: int, bounds: WindowBoundsDict) -> Command[Response]:
        """
        Generates the command to set the bounds of a window.

        Args:
            window_id (int): The ID of the window to set the bounds for.
            bounds (WindowBoundsDict): The bounds to set for the window,
                           which should include width, height,
                           and optionally x and y coordinates.

        Returns:
            Command: The command to be sent to the browser.
        """
        command = deepcopy(cls.SET_WINDOW_BOUNDS_TEMPLATE)
        params = SetWindowBoundsParams(
            windowId=window_id,
            bounds=bounds
        )
        command['params'] = params
        return command

    @classmethod
    def set_window_maximized(cls, window_id: int) -> Command[Response]:
        """
        Generates the command to maximize a window.

        Args:
            window_id (int): The ID of the window to maximize.

        Returns:
            Command: The command to be sent to the browser.
        """
        bounds = WindowBoundsDict(windowState=WindowState.MAXIMIZED)
        return cls.set_window_bounds(window_id, bounds)

    @classmethod
    def set_window_minimized(cls, window_id: int) -> Command[Response]:
        """
        Generates the command to minimize a window.

        Args:
            window_id (int): The ID of the window to minimize.

        Returns:
            Command: The command to be sent to the browser.
        """
        bounds = WindowBoundsDict(windowState=WindowState.MINIMIZED)
        return cls.set_window_bounds(window_id, bounds)
