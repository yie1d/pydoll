from enum import Enum
from typing import TypedDict, NotRequired


class WindowState(str, Enum):
    """Possible states for a browser window."""
    MAXIMIZED = 'maximized'
    MINIMIZED = 'minimized'
    NORMAL = 'normal'


class DownloadBehavior(str, Enum):
    """Possible behaviors for download handling."""
    ALLOW = 'allow'
    DENY = 'deny'


class CommandParams(TypedDict, total=False):
    """Base structure for command parameters. All fields are optional."""
    pass


class Command(TypedDict):
    """Base structure for all commands.
    
    Attributes:
        method: The command method name
        params: Optional dictionary of parameters for the command
    """
    method: str
    params: NotRequired[CommandParams]


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


class SetWindowBoundsParams(CommandParams):
    """Parameters for setting window bounds."""
    windowId: int
    bounds: WindowBoundsDict

