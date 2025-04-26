from enum import Enum, auto


class By(str, Enum):
    CSS_SELECTOR = 'css'
    XPATH = 'xpath'
    CLASS_NAME = 'class_name'
    ID = 'id'
    TAG_NAME = 'tag_name'


class Scripts:
    ELEMENT_VISIBLE = """
    function() {
        const rect = this.getBoundingClientRect();
        return (
            rect.width > 0 && rect.height > 0
            && getComputedStyle(this).visibility !== 'hidden'
            && getComputedStyle(this).display !== 'none'
        )
    }
    """

    ELEMENT_ON_TOP = """
    function() {
        const rect = this.getBoundingClientRect();
        const elementFromPoint = document.elementFromPoint(
            rect.x + rect.width / 2,
            rect.y + rect.height / 2
        );
        return elementFromPoint === this;
    }
    """

    CLICK = """
    function(){
        clicked = false;
        this.addEventListener('click', function(){
            clicked = true;
        });
        this.click();
        return clicked;
    }
    """

    CLICK_OPTION_TAG = """
    document.querySelector('option[value="{self.value}"]').selected = true;
    var selectParentXpath = (
        '//option[@value="{self.value}"]//ancestor::select'
    );
    var select = document.evaluate(
        selectParentXpath,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;
    var event = new Event('change', { bubbles: true });
    select.dispatchEvent(event);
    """

    BOUNDS = """
    function() {
        return JSON.stringify(this.getBoundingClientRect());
    }
    """

    FIND_RELATIVE_XPATH_ELEMENT = """
        function() {
            return document.evaluate(
                "{escaped_value}", this, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null
            ).singleNodeValue;
        }
    """

    FIND_XPATH_ELEMENT = """
        var element = document.evaluate(
            "{escaped_value}", document, null,
            XPathResult.FIRST_ORDERED_NODE_TYPE, null
        ).singleNodeValue;
        element;
    """

    FIND_RELATIVE_XPATH_ELEMENTS = """
        function() {
            var elements = document.evaluate(
                "{escaped_value}", this, null,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
            );
            var results = [];
            for (var i = 0; i < elements.snapshotLength; i++) {
                results.push(elements.snapshotItem(i));
            }
            return results;
        }
    """

    FIND_XPATH_ELEMENTS = """
        var elements = document.evaluate(
            "{escaped_value}", document, null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null
        );
        var results = [];
        for (var i = 0; i < elements.snapshotLength; i++) {
            results.push(elements.snapshotItem(i));
        }
        results;
    """

    QUERY_SELECTOR = 'document.querySelector("{selector}");'

    RELATIVE_QUERY_SELECTOR = """
        function() {
            return this.querySelector("{selector}");
        }
    """

    QUERY_SELECTOR_ALL = 'document.querySelectorAll("{selector}");'

    RELATIVE_QUERY_SELECTOR_ALL = """
        function() {
            return this.querySelectorAll("{selector}");
        }
    """


class Keys:
    BACKSPACE = ('Backspace', 8)
    TAB = ('Tab', 9)
    ENTER = ('Enter', 13)
    SHIFT = ('Shift', 16)
    CONTROL = ('Control', 17)
    ALT = ('Alt', 18)
    PAUSE = ('Pause', 19)
    CAPSLOCK = ('CapsLock', 20)
    ESCAPE = ('Escape', 27)
    SPACE = ('Space', 32)
    PAGEUP = ('PageUp', 33)
    PAGEDOWN = ('PageDown', 34)
    END = ('End', 35)
    HOME = ('Home', 36)
    ARROWLEFT = ('ArrowLeft', 37)
    ARROWUP = ('ArrowUp', 38)
    ARROWRIGHT = ('ArrowRight', 39)
    ARROWDOWN = ('ArrowDown', 40)
    PRINTSCREEN = ('PrintScreen', 44)
    INSERT = ('Insert', 45)
    DELETE = ('Delete', 46)
    META = ('Meta', 91)
    METARIGHT = ('MetaRight', 92)
    CONTEXTMENU = ('ContextMenu', 93)
    NUMLOCK = ('NumLock', 144)
    SCROLLLOCK = ('ScrollLock', 145)

    F1 = ('F1', 112)
    F2 = ('F2', 113)
    F3 = ('F3', 114)
    F4 = ('F4', 115)
    F5 = ('F5', 116)
    F6 = ('F6', 117)
    F7 = ('F7', 118)
    F8 = ('F8', 119)
    F9 = ('F9', 120)
    F10 = ('F10', 121)
    F11 = ('F11', 122)
    F12 = ('F12', 123)

    SEMICOLON = ('Semicolon', 186)
    EQUALSIGN = ('EqualSign', 187)
    COMMA = ('Comma', 188)
    MINUS = ('Minus', 189)
    PERIOD = ('Period', 190)
    SLASH = ('Slash', 191)
    GRAVEACCENT = ('GraveAccent', 192)
    BRACKETLEFT = ('BracketLeft', 219)
    BACKSLASH = ('Backslash', 220)
    BRACKETRIGHT = ('BracketRight', 221)
    QUOTE = ('Quote', 222)


class BrowserType(Enum):
    CHROME = auto()
    EDGE = auto()


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


class RequestMethod(str, Enum):
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


class NetworkErrorReason(str, Enum):
    """Network level fetch failure reason."""

    FAILED = 'Failed'
    ABORTED = 'Aborted'
    TIMED_OUT = 'TimedOut'
    ACCESS_DENIED = 'AccessDenied'
    CONNECTION_CLOSED = 'ConnectionClosed'
    CONNECTION_RESET = 'ConnectionReset'
    CONNECTION_REFUSED = 'ConnectionRefused'
    CONNECTION_ABORTED = 'ConnectionAborted'
    CONNECTION_FAILED = 'ConnectionFailed'
    NAME_NOT_RESOLVED = 'NameNotResolved'
    INTERNET_DISCONNECTED = 'InternetDisconnected'
    ADDRESS_UNREACHABLE = 'AddressUnreachable'
    BLOCKED_BY_CLIENT = 'BlockedByClient'
    BLOCKED_BY_RESPONSE = 'BlockedByResponse'
