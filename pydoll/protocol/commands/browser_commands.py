from copy import deepcopy
from typing import List, Optional

from pydoll.protocol.types.commands_types import (
    CancelDownloadParams,
    Command,
    DownloadBehavior,
    GetWindowForTargetParams,
    GrantPermissionsParams,
    PermissionType,
    ResetPermissionsParams,
    SetDownloadBehaviorParams,
    SetWindowBoundsParams,
    WindowBoundsDict,
    WindowState,
)
from pydoll.protocol.types.responses_types import (
    GetVersionResponse,
    GetWindowForTargetResponse,
    Response,
)


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

    GET_VERSION = Command(method='Browser.getVersion')
    RESET_PERMISSIONS = Command(method='Browser.resetPermissions')
    CANCEL_DOWNLOAD = Command(method='Browser.cancelDownload')
    CRASH = Command(method='Browser.crash')
    CRASH_GPU_PROCESS = Command(method='Browser.crashGpuProcess')
    CLOSE = Command(method='Browser.close')
    GET_WINDOW_ID_BY_TARGET = Command(method='Browser.getWindowForTarget')
    SET_WINDOW_BOUNDS_TEMPLATE = Command(method='Browser.setWindowBounds')
    SET_DOWNLOAD_BEHAVIOR = Command(method='Browser.setDownloadBehavior')
    GRANT_PERMISSIONS = Command(method='Browser.grantPermissions')

    @classmethod
    def get_version(cls) -> Command[GetVersionResponse]:
        """
        Generates a command to get browser version information.

        Returns:
            Command[GetVersionResponse]: The CDP command that returns browser version details
                including protocol version, product name, revision, and user agent.
        """
        return cls.GET_VERSION

    @classmethod
    def reset_permissions(
        cls, browser_context_id: Optional[str] = None
    ) -> Command[Response]:
        """
        Generates a command to reset all permissions.

        Args:
            browser_context_id (Optional[str]): The browser context to reset permissions for.
                If not specified, resets permissions for the default context.

        Returns:
            Command[Response]: The CDP command that returns a basic success response.
        """
        command = deepcopy(cls.RESET_PERMISSIONS)
        if browser_context_id:
            params = ResetPermissionsParams(
                browserContextId=browser_context_id
            )
            command['params'] = params
        return command

    @classmethod
    def cancel_download(
        cls, guid: str, browser_context_id: Optional[str] = None
    ) -> Command[Response]:
        """
        Generates a command to cancel a download.

        Args:
            guid (str): Global unique identifier of the download.
            browser_context_id (Optional[str]): The browser context the download belongs to.
                If not specified, uses the default context.

        Returns:
            Command[Response]: The CDP command that returns a basic success response.
        """
        command = deepcopy(cls.CANCEL_DOWNLOAD)
        params = CancelDownloadParams(guid=guid)
        if browser_context_id:
            params['browserContextId'] = browser_context_id
        command['params'] = params
        return command

    @classmethod
    def crash(cls) -> Command[Response]:
        """
        Generates a command to crash the browser main process.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                before crashing the browser.
        """
        return cls.CRASH

    @classmethod
    def crash_gpu_process(cls) -> Command[Response]:
        """
        Generates a command to crash the browser GPU process.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                before crashing the GPU process.
        """
        return cls.CRASH_GPU_PROCESS

    @classmethod
    def set_download_path(cls, path: str) -> Command[Response]:
        """
        Generates a command to set the download path for the browser.

        Args:
            path (str): The path to set for downloads.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                after setting the download path.
        """
        command = deepcopy(cls.SET_DOWNLOAD_BEHAVIOR)
        params = SetDownloadBehaviorParams(
            behavior=DownloadBehavior.ALLOW, downloadPath=path
        )
        command['params'] = params
        return command

    @classmethod
    def close(cls) -> Command[Response]:
        """
        Generates a command to close the browser.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                before closing the browser.
        """
        return cls.CLOSE

    @classmethod
    def get_window_id_by_target(
        cls, target_id: str
    ) -> Command[GetWindowForTargetResponse]:
        """
        Generates a command to get the ID of the current window.

        Args:
            target_id (str): The target_id to set for the window.

        Returns:
            Command[GetWindowForTargetResponse]: The CDP command that returns window
                information including windowId and bounds.
        """
        command = deepcopy(cls.GET_WINDOW_ID_BY_TARGET)
        params = GetWindowForTargetParams(targetId=target_id)
        command['params'] = params
        return command

    @classmethod
    def set_window_bounds(
        cls, window_id: int, bounds: WindowBoundsDict
    ) -> Command[Response]:
        """
        Generates a command to set the bounds of a window.

        Args:
            window_id (int): The ID of the window to set the bounds for.
            bounds (WindowBoundsDict): The bounds to set for the window,
                which should include windowState and optionally width, height,
                x, and y coordinates.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                after setting the window bounds.
        """
        command = deepcopy(cls.SET_WINDOW_BOUNDS_TEMPLATE)
        params = SetWindowBoundsParams(windowId=window_id, bounds=bounds)
        command['params'] = params
        return command

    @classmethod
    def set_window_maximized(cls, window_id: int) -> Command[Response]:
        """
        Generates a command to maximize a window.

        Args:
            window_id (int): The ID of the window to maximize.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                after maximizing the window.
        """
        bounds = WindowBoundsDict(windowState=WindowState.MAXIMIZED)
        return cls.set_window_bounds(window_id, bounds)

    @classmethod
    def set_window_minimized(cls, window_id: int) -> Command[Response]:
        """
        Generates a command to minimize a window.

        Args:
            window_id (int): The ID of the window to minimize.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                after minimizing the window.
        """
        bounds = WindowBoundsDict(windowState=WindowState.MINIMIZED)
        return cls.set_window_bounds(window_id, bounds)

    @classmethod
    def grant_permissions(
        cls,
        permissions: List[PermissionType],
        origin: Optional[str] = None,
        browser_context_id: Optional[str] = None,
    ) -> Command[Response]:
        """
        Generates a command to grant specific permissions to the given origin.

        Args:
            permissions (List[PermissionType]): List of permissions to grant.
                See PermissionType enum for available permissions.
            origin (Optional[str]): The origin to grant permissions to.
                If not specified, grants for all origins.
            browser_context_id (Optional[str]): The browser context to grant permissions in.
                If not specified, uses the default context.

        Returns:
            Command[Response]: The CDP command that returns a basic success response
                after granting the specified permissions.
        """
        command = deepcopy(cls.GRANT_PERMISSIONS)
        params = GrantPermissionsParams(permissions=permissions)
        if origin:
            params['origin'] = origin

        if browser_context_id:
            params['browserContextId'] = browser_context_id

        command['params'] = params
        return command
