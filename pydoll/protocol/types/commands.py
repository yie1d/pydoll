from enum import Enum
from typing import Generic, List, NotRequired, TypedDict, TypeVar

T_CommandResponse = TypeVar('T_CommandResponse')


class CommandParams(TypedDict, total=False):
    """Base structure for command parameters. All fields are optional."""

    pass


class Command(TypedDict, Generic[T_CommandResponse]):
    """Base structure for all commands.

    Attributes:
        method: The command method name
        params: Optional dictionary of parameters for the command
    """

    method: str
    params: NotRequired[CommandParams]


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


class PermissionType(str, Enum):
    """Browser permission types as defined in the Chrome DevTools Protocol."""

    AR = 'ar'
    AUDIO_CAPTURE = 'audioCapture'
    AUTOMATIC_FULLSCREEN = 'automaticFullscreen'
    BACKGROUND_FETCH = 'backgroundFetch'
    BACKGROUND_SYNC = 'backgroundSync'
    CAMERA_PAN_TILT_ZOOM = 'cameraPanTiltZoom'
    CAPTURED_SURFACE_CONTROL = 'capturedSurfaceControl'
    CLIPBOARD_READ_WRITE = 'clipboardReadWrite'
    CLIPBOARD_SANITIZED_WRITE = 'clipboardSanitizedWrite'
    DISPLAY_CAPTURE = 'displayCapture'
    DURABLE_STORAGE = 'durableStorage'
    GEOLOCATION = 'geolocation'
    HAND_TRACKING = 'handTracking'
    IDLE_DETECTION = 'idleDetection'
    KEYBOARD_LOCK = 'keyboardLock'
    LOCAL_FONTS = 'localFonts'
    LOCAL_NETWORK_ACCESS = 'localNetworkAccess'
    MIDI = 'midi'
    MIDI_SYSEX = 'midiSysex'
    NFC = 'nfc'
    NOTIFICATIONS = 'notifications'
    PAYMENT_HANDLER = 'paymentHandler'
    PERIODIC_BACKGROUND_SYNC = 'periodicBackgroundSync'
    POINTER_LOCK = 'pointerLock'
    PROTECTED_MEDIA_IDENTIFIER = 'protectedMediaIdentifier'
    SENSORS = 'sensors'
    SMART_CARD = 'smartCard'
    SPEAKER_SELECTION = 'speakerSelection'
    STORAGE_ACCESS = 'storageAccess'
    TOP_LEVEL_STORAGE_ACCESS = 'topLevelStorageAccess'
    VIDEO_CAPTURE = 'videoCapture'
    VR = 'vr'
    WAKE_LOCK_SCREEN = 'wakeLockScreen'
    WAKE_LOCK_SYSTEM = 'wakeLockSystem'
    WEB_APP_INSTALLATION = 'webAppInstallation'
    WEB_PRINTING = 'webPrinting'
    WINDOW_MANAGEMENT = 'windowManagement'


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


class RequestMethods(str, Enum):
    """HTTP request methods."""

    GET = 'GET'
    POST = 'POST'
    OPTIONS = 'OPTIONS'
    PUT = 'PUT'
    DELETE = 'DELETE'


class HeaderEntry(TypedDict):
    """HTTP header entry structure."""

    name: str
    value: str


class ContinueRequestParams(CommandParams):
    """Parameters for continuing a request."""

    requestId: str
    url: NotRequired[str]
    method: NotRequired[RequestMethods]
    postData: NotRequired[dict]
    headers: NotRequired[List[HeaderEntry]]
    interceptResponse: NotRequired[bool]
