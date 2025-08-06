from enum import Enum

from typing_extensions import NotRequired, TypedDict

TimeSinceEpoch = float


class GestureSourceType(Enum):
    """Gesture source types."""

    DEFAULT = 'default'
    TOUCH = 'touch'
    MOUSE = 'mouse'


class MouseButton(Enum):
    """Mouse button types."""

    NONE = 'none'
    LEFT = 'left'
    MIDDLE = 'middle'
    RIGHT = 'right'
    BACK = 'back'
    FORWARD = 'forward'


class DragEventType(Enum):
    """Drag event types."""

    DRAG_ENTER = 'dragEnter'
    DRAG_OVER = 'dragOver'
    DROP = 'drop'
    DRAG_CANCEL = 'dragCancel'


class KeyEventType(Enum):
    """Key event types."""

    KEY_DOWN = 'keyDown'
    KEY_UP = 'keyUp'
    RAW_KEY_DOWN = 'rawKeyDown'
    CHAR = 'char'


class MouseEventType(Enum):
    """Mouse event types."""

    MOUSE_PRESSED = 'mousePressed'
    MOUSE_RELEASED = 'mouseReleased'
    MOUSE_MOVED = 'mouseMoved'
    MOUSE_WHEEL = 'mouseWheel'


class TouchEventType(Enum):
    """Touch event types."""

    TOUCH_START = 'touchStart'
    TOUCH_END = 'touchEnd'
    TOUCH_MOVE = 'touchMove'
    TOUCH_CANCEL = 'touchCancel'


class PointerType(Enum):
    """Pointer types."""

    MOUSE = 'mouse'
    PEN = 'pen'


class TouchPoint(TypedDict):
    """Touch point data."""

    x: float
    y: float
    radiusX: NotRequired[float]
    radiusY: NotRequired[float]
    rotationAngle: NotRequired[float]
    force: NotRequired[float]
    tangentialPressure: NotRequired[float]
    tiltX: NotRequired[float]
    tiltY: NotRequired[float]
    twist: NotRequired[int]
    id: NotRequired[float]


class DragDataItem(TypedDict):
    """Drag data item."""

    mimeType: str
    data: str
    title: NotRequired[str]
    baseURL: NotRequired[str]


class DragData(TypedDict):
    """Drag data."""

    items: list[DragDataItem]
    dragOperationsMask: int
    files: NotRequired[list[str]]
