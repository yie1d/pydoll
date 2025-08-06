from enum import Enum

from typing_extensions import NotRequired, TypedDict

from pydoll.protocol.browser.types import BrowserContextID
from pydoll.protocol.page.types import FrameId

TargetID = str
SessionID = str
"""Unique identifier of attached debugging session."""


class TargetInfo(TypedDict):
    targetId: TargetID
    type: str
    title: str
    url: str
    attached: bool
    openerId: NotRequired[TargetID]
    canAccessOpener: NotRequired[bool]
    openerFrameId: NotRequired[FrameId]
    browserContextId: NotRequired[BrowserContextID]
    subtype: NotRequired[str]


class FilterEntry(TypedDict, total=False):
    """A filter used by target query/discovery/auto-attach operations."""

    exclude: bool
    type: str


TargetFilter = list[FilterEntry]


class RemoteLocation(TypedDict):
    host: str
    port: int


class WindowState(str, Enum):
    """The state of the target window."""

    NORMAL = 'normal'
    MINIMIZED = 'minimized'
    MAXIMIZED = 'maximized'
    FULLSCREEN = 'fullscreen'
