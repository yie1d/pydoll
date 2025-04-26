from typing import List, NotRequired

from pydoll.protocol.types.commands.base_types import CommandParams
from pydoll.protocol.types.enums import (
    DownloadBehavior,
    PermissionType,
    WindowState
)


class WindowBoundsDict(TypedDict):
    """Structure for window bounds parameters."""

    windowState: WindowState
    width: NotRequired[int]
    height: NotRequired[int]
    x: NotRequired[int]
    y: NotRequired[int]


class GetWindowForTargetParams(CommandParams):
    """Parameters for getting window by target ID."""

    targetId: str


class SetDownloadBehaviorParams(CommandParams):
    """Parameters for setting download behavior."""

    behavior: DownloadBehavior
    downloadPath: str
    browserContextId: NotRequired[str]
    eventsEnabled: NotRequired[bool]


class SetWindowBoundsParams(CommandParams):
    """Parameters for setting window bounds."""

    windowId: int
    bounds: WindowBoundsDict


class ResetPermissionsParams(CommandParams):
    """Parameters for resetting permissions."""

    browserContextId: str


class CancelDownloadParams(CommandParams):
    """Parameters for cancelling downloads."""

    guid: str
    browserContextId: NotRequired[str]


class GrantPermissionsParams(CommandParams):
    """Parameters for granting permissions."""

    permissions: List[PermissionType]
    origin: NotRequired[str]
    browserContextId: NotRequired[str] 