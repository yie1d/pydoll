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


class CookiePriority(str, Enum):
    """Cookie priority levels."""

    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


class CookieSourceScheme(str, Enum):
    """Cookie source schemes."""

    UNSET = 'Unset'
    NON_SECURE = 'NonSecure'
    SECURE = 'Secure'


class CookieSameSite(str, Enum):
    """Cookie same site values."""

    STRICT = 'Strict'
    LAX = 'Lax'
    NONE = 'None'


class ConnectionType(str, Enum):
    """Network connection types."""

    NONE = 'none'
    CELLULAR2G = 'cellular2g'
    CELLULAR3G = 'cellular3g'
    CELLULAR4G = 'cellular4g'
    WIFI = 'wifi'
    ETHERNET = 'ethernet'
    BLUETOOTH = 'bluetooth'
    WIMAX = 'wimax'
    OTHER = 'other'


class ContentEncoding(str, Enum):
    """Content encoding types."""

    GZIP = 'gzip'
    DEFLATE = 'deflate'
    BR = 'br'
    ZSTD = 'zstd'


class ScreenshotFormat(str, Enum):
    """Screenshot formats."""

    JPEG = 'jpeg'
    PNG = 'png'
    WEBP = 'webp'


class TransitionType(str, Enum):
    """Transition types."""

    LINK = 'link'
    TYPED = 'typed'
    ADDRESS_BAR = 'address_bar'
    AUTO_BOOKMARK = 'auto_bookmark'
    AUTO_SUBFRAME = 'auto_subframe'
    MANUAL_SUBFRAME = 'manual_subframe'
    GENERATED = 'generated'
    AUTO_TOPLEVEL = 'auto_toplevel'
    FORM_SUBMIT = 'form_submit'
    RELOAD = 'reload'
    KEYWORD = 'keyword'
    KEYWORD_GENERATED = 'keyword_generated'
    OTHER = 'other'


class ReferrerPolicy(str, Enum):
    """Referrer policies."""

    NO_REFERRER = 'noReferrer'
    NO_REFERRER_WHEN_DOWNGRADE = 'noReferrerWhenDowngrade'
    ORIGIN = 'origin'
    ORIGIN_WHEN_CROSS_ORIGIN = 'originWhenCrossOrigin'
    SAME_ORIGIN = 'sameOrigin'
    STRICT_ORIGIN = 'strictOrigin'
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN = 'strictOriginWhenCrossOrigin'
    UNSAFE_URL = 'unsafeUrl'


class TransferMode(str, Enum):
    """Transfer modes."""

    RETURN_AS_STREAM = 'returnAsStream'
    RETURN_AS_BASE64 = 'returnAsBase64'


class AutoResponseMode(str, Enum):
    NONE = 'none'
    AUTO_ACCEPT = 'autoAccept'
    AUTO_REJECT = 'autoReject'
    AUTO_OPTOUT = 'autoOptout'


class WebLifecycleState(str, Enum):
    """Web lifecycle states."""

    FROZEN = 'frozen'
    ACTIVE = 'active'


class ScreencastFormat(str, Enum):
    """Screencast formats."""

    JPEG = 'jpeg'
    PNG = 'png'


class OriginTrialStatus(str, Enum):
    ENABLED = 'Enabled'
    VALID_TOKEN_NOT_PROVIDED = 'ValidTokenNotProvided'
    OS_NOT_SUPPORTED = 'OsNotSupported'
    TRIAL_NOT_ALLOWED = 'TrialNotAllowed'


class OriginTrialUsageRestriction(str, Enum):
    NONE = 'None'
    SUBSET = 'Subset'


class OriginTrialTokenStatus(str, Enum):
    SUCCESS = 'Success'
    NOT_SUPPORTED = 'NotSupported'
    INSECURE = 'Insecure'
    EXPIRED = 'Expired'
    WRONG_ORIGIN = 'WrongOrigin'
    INVALID_SIGNATURE = 'InvalidSignature'
    MALFORMED = 'Malformed'
    WRONG_VERSION = 'WrongVersion'
    FEATURE_DISABLED = 'FeatureDisabled'
    TOKEN_DISABLED = 'TokenDisabled'
    FEATURE_DISABLED_FOR_USER = 'FeatureDisabledForUser'
    UNKNOWN_TRIAL = 'UnknownTrial'


class PermissionsPolicyBlockReason(str, Enum):
    HEADER = 'Header'
    IFRAME_ATTRIBUTE = 'IframeAttribute'
    IN_FANCED_FRAME_TREE = 'InFancedFrameTree'
    IN_ISOLATED_APP = 'InIsolatedApp'


class PermissionsPolicyFeature(str, Enum):
    ACCELEROMETER = 'accelerometer'
    ALL_SCREENS_CAPTURE = 'all-screens-capture'
    AMBIENT_LIGHT_SENSOR = 'ambient-light-sensor'
    ATTRIBUTION_REPORTING = 'attribution-reporting'
    AUTOPLAY = 'autoplay'
    BLUETOOTH = 'bluetooth'
    BROWSING_TOPICS = 'browsing-topics'
    CAMERA = 'camera'
    CAPTURED_SURFACE_CONTROL = 'captured-surface-control'
    CH_DPR = 'ch-dpr'
    CH_DEVICE_MEMORY = 'ch-device-memory'
    CH_DOWNLINK = 'ch-downlink'
    CH_ECT = 'ch-ect'
    CH_PREFERS_COLOR_SCHEME = 'ch-prefers-color-scheme'
    CH_PREFERS_REDUCED_MOTION = 'ch-prefers-reduced-motion'
    CH_PREFERS_REDUCED_TRANSPARENCY = 'ch-prefers-reduced-transparency'
    CH_RTT = 'ch-rtt'
    CH_SAVE_DATA = 'ch-save-data'
    CH_UA = 'ch-ua'
    CH_UA_ARCH = 'ch-ua-arch'
    CH_UA_BITNESS = 'ch-ua-bitness'
    CH_UA_HIGH_ENTROPY_VALUES = 'ch-ua-high-entropy-values'
    CH_UA_PLATFORM = 'ch-ua-platform'
    CH_UA_MODEL = 'ch-ua-model'
    CH_UA_MOBILE = 'ch-ua-mobile'
    CH_UA_FORM_FACTORS = 'ch-ua-form-factors'
    CH_UA_FULL_VERSION = 'ch-ua-full-version'
    CH_UA_FULL_VERSION_LIST = 'ch-ua-full-version-list'
    CH_UA_PLATFORM_VERSION = 'ch-ua-platform-version'
    CH_UA_WOW64 = 'ch-ua-wow64'
    CH_VIEWPORT_HEIGHT = 'ch-viewport-height'
    CH_VIEWPORT_WIDTH = 'ch-viewport-width'
    CH_WIDTH = 'ch-width'
    CLIPBOARD_READ = 'clipboard-read'
    CLIPBOARD_WRITE = 'clipboard-write'
    COMPUTE_PRESSURE = 'compute-pressure'
    CONTROLLED_FRAME = 'controlled-frame'
    CROSS_ORIGIN_ISOLATED = 'cross-origin-isolated'
    DEFERRED_FETCH = 'deferred-fetch'
    DEFERRED_FETCH_MINIMAL = 'deferred-fetch-minimal'
    DEVICE_ATTRIBUTES = 'device-attributes'
    DIGITAL_CREDENTIALS_GET = 'digital-credentials-get'
    DIRECT_SOCKETS = 'direct-sockets'
    DIRECT_SOCKETS_PRIVATE = 'direct-sockets-private'
    DISPLAY_CAPTURE = 'display-capture'
    DOCUMENT_DOMAIN = 'document-domain'
    ENCRYPTED_MEDIA = 'encrypted-media'
    EXECUTION_WHILE_OUT_OF_VIEWPORT = 'execution-while-out-of-viewport'
    EXECUTION_WHILE_NOT_RENDERED = 'execution-while-not-rendered'
    FENCED_UNPARTITIONED_STORAGE_READ = 'fenced-unpartitioned-storage-read'
    FOCUS_WITHOUT_USER_ACTIVATION = 'focus-without-user-activation'
    FULLSCREEN = 'fullscreen'
    FROBULATE = 'frobulate'
    GAMEPAD = 'gamepad'
    GEOLOCATION = 'geolocation'
    GYROSCOPE = 'gyroscope'
    HID = 'hid'
    IDENTITY_CREDENTIALS_GET = 'identity-credentials-get'
    IDLE_DETECTION = 'idle-detection'
    INTEREST_COHORT = 'interest-cohort'
    JOIN_AD_INTEREST_GROUP = 'join-ad-interest-group'
    KEYBOARD_MAP = 'keyboard-map'
    LANGUAGE_DETECTOR = 'language-detector'
    LOCAL_FONTS = 'local-fonts'
    MAGNETOMETER = 'magnetometer'
    MEDIA_PLAYBACK_WHILE_NOT_VISIBLE = 'media-playback-while-not-visible'
    MICROPHONE = 'microphone'
    MIDI = 'midi'
    OTP_CREDENTIALS = 'otp-credentials'
    PAYMENT = 'payment'
    PICTURE_IN_PICTURE = 'picture-in-picture'
    POPINS = 'popins'
    PRIVATE_AGGREGATION = 'private-aggregation'
    PRIVATE_STATE_TOKEN_ISSUANCE = 'private-state-token-issuance'
    PRIVATE_STATE_TOKEN_REDEMPTION = 'private-state-token-redemption'
    PUBLICKEY_CREDENTIALS_CREATE = 'publickey-credentials-create'
    PUBLICKEY_CREDENTIALS_GET = 'publickey-credentials-get'
    REWRITER = 'rewriter'
    RUN_AD_AUCTION = 'run-ad-auction'
    SCREEN_WAKE_LOCK = 'screen-wake-lock'
    SERIAL = 'serial'
    SHARED_AUTOFILL = 'shared-autofill'
    SHARED_STORAGE = 'shared-storage'
    SHARED_STORAGE_SELECT_URL = 'shared-storage-select-url'
    SMART_CARD = 'smart-card'
    SPEAKER_SELECTION = 'speaker-selection'
    STORAGE_ACCESS = 'storage-access'
    SUB_APPS = 'sub-apps'
    SUMMARIZER = 'summarizer'
    SYNC_XHR = 'sync-xhr'
    TRANSLATOR = 'translator'
    UNLOAD = 'unload'
    USB = 'usb'
    USB_UNRESTRICTED = 'usb-unrestricted'
    VERTICAL_SCROLL = 'vertical-scroll'
    WEB_APP_INSTALLATION = 'web-app-installation'
    WEB_PRINTING = 'web-printing'
    WEB_SHARE = 'web-share'
    WINDOW_MANAGEMENT = 'window-management'
    WRITER = 'writer'
    XR_SPATIAL_TRACKING = 'xr-spatial-tracking'


class CrossOriginOpenerPolicyStatus(str, Enum):
    SAME_ORIGIN = 'SameOrigin'
    SAME_ORIGIN_ALLOW_POPUPS = 'SameOriginAllowPopups'
    RESTRICT_PROPERTIES = 'RestrictProperties'
    UNSAFE_NONE = 'UnsafeNone'
    SAME_ORIGIN_PLUS_COEP = 'SameOriginPlusCoep'
    RESTRICT_PROPERTIES_PLUS_COEP = 'RestrictPropertiesPlusCoep'
    NO_OPENER_ALLOW_POPUPS = 'NoopenerAllowPopups'


class CrossOriginEmbedderPolicyStatus(str, Enum):
    """Cross-origin embedder policy status values."""

    NONE = 'None'
    CREDENTIALLESS = 'Credentialless'
    REQUIRE_CORP = 'RequireCorp'


class ContentSecurityPolicySource(str, Enum):
    HTTP = 'HTTP'
    META = 'Meta'
