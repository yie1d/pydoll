from enum import Enum
from typing import List


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


class RequestMethods(str, Enum):
    """HTTP request methods."""

    GET = 'GET'
    POST = 'POST'
    OPTIONS = 'OPTIONS'
    PUT = 'PUT'
    DELETE = 'DELETE'


class AuthChallengeResponseValues(str, Enum):
    DEFAULT = 'Default'
    CANCEL_AUTH = 'CancelAuth'
    PROVIDE_CREDENTIALS = 'ProvideCredentials'


class ResourceType(str, Enum):
    DOCUMENT = 'Document'
    STYLESHEET = 'Stylesheet'
    IMAGE = 'Image'
    MEDIA = 'Media'
    FONT = 'Font'
    SCRIPT = 'Script'
    TEXT_TRACK = 'TextTrack'
    XHR = 'XHR'
    FETCH = 'Fetch'
    PREFETCH = 'Prefetch'
    EVENT_SOURCE = 'EventSource'
    WEBSOCKET = 'WebSocket'
    MANIFEST = 'Manifest'
    SIGNED_EXCHANGE = 'SignedExchange'
    PING = 'Ping'
    CSP_VIOLATION_REPORT = 'CSPViolationReport'
    PREFLIGHT = 'Preflight'
    OTHER = 'OTHER'


class RequestStage(str, Enum):
    REQUEST = 'Request'
    RESPONSE = 'Response' 