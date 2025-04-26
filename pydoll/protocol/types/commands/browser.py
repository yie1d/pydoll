from enum import Enum
from typing import TypedDict, NotRequired

from pydoll.protocol.types.commands.common import CommandParams


class WindowState(str, Enum):
    """Possible states for a browser window."""
    MAXIMIZED = 'maximized'
    MINIMIZED = 'minimized'
    NORMAL = 'normal'


class DownloadBehavior(str, Enum):
    """Possible behaviors for download handling."""
    ALLOW = 'allow'
    DENY = 'deny'
    ALLOW_AND_NAME = 'allowAndName'
    DEFAULT = 'default'


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

