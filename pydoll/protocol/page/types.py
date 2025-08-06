from enum import Enum

from typing_extensions import NotRequired, TypedDict

from pydoll.protocol.network.types import LoaderId, ResourceType, TimeSinceEpoch
from pydoll.protocol.runtime.types import ScriptId, UniqueDebuggerId

FrameId = str
ScriptIdentifier = str


class AdFrameType(Enum):
    """Ad frame types."""

    NONE = 'none'
    CHILD = 'child'
    ROOT = 'root'


class AdFrameExplanation(Enum):
    """Ad frame explanation types."""

    PARENT_IS_AD = 'ParentIsAd'
    CREATED_BY_AD_SCRIPT = 'CreatedByAdScript'
    MATCHED_BLOCKING_RULE = 'MatchedBlockingRule'


class SecureContextType(Enum):
    """Secure context types."""

    SECURE = 'Secure'
    SECURE_LOCALHOST = 'SecureLocalhost'
    INSECURE_SCHEME = 'InsecureScheme'
    INSECURE_ANCESTOR = 'InsecureAncestor'


class CrossOriginIsolatedContextType(Enum):
    """Cross-origin isolated context types."""

    ISOLATED = 'Isolated'
    NOT_ISOLATED = 'NotIsolated'
    NOT_ISOLATED_FEATURE_DISABLED = 'NotIsolatedFeatureDisabled'


class GatedAPIFeatures(Enum):
    """Gated API features."""

    SHARED_ARRAY_BUFFERS = 'SharedArrayBuffers'
    SHARED_ARRAY_BUFFERS_TRANSFER_ALLOWED = 'SharedArrayBuffersTransferAllowed'
    PERFORMANCE_MEASURE_MEMORY = 'PerformanceMeasureMemory'
    PERFORMANCE_PROFILE = 'PerformanceProfile'


class PermissionsPolicyFeature(Enum):
    """Permissions policy features."""

    ACCELEROMETER = 'accelerometer'
    ALL_SCREENS_CAPTURE = 'all-screens-capture'
    AMBIENT_LIGHT_SENSOR = 'ambient-light-sensor'
    ARIA_NOTIFY = 'aria-notify'
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
    LANGUAGE_MODEL = 'language-model'
    LOCAL_FONTS = 'local-fonts'
    LOCAL_NETWORK_ACCESS = 'local-network-access'
    MAGNETOMETER = 'magnetometer'
    MEDIA_PLAYBACK_WHILE_NOT_VISIBLE = 'media-playback-while-not-visible'
    MICROPHONE = 'microphone'
    MIDI = 'midi'
    ON_DEVICE_SPEECH_RECOGNITION = 'on-device-speech-recognition'
    OTP_CREDENTIALS = 'otp-credentials'
    PAYMENT = 'payment'
    PICTURE_IN_PICTURE = 'picture-in-picture'
    POPINS = 'popins'
    PRIVATE_AGGREGATION = 'private-aggregation'
    PRIVATE_STATE_TOKEN_ISSUANCE = 'private-state-token-issuance'
    PRIVATE_STATE_TOKEN_REDEMPTION = 'private-state-token-redemption'
    PUBLICKEY_CREDENTIALS_CREATE = 'publickey-credentials-create'
    PUBLICKEY_CREDENTIALS_GET = 'publickey-credentials-get'
    RECORD_AD_AUCTION_EVENTS = 'record-ad-auction-events'
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


class PermissionsPolicyBlockReason(Enum):
    """Permissions policy block reasons."""

    HEADER = 'Header'
    IFRAME_ATTRIBUTE = 'IframeAttribute'
    IN_FENCED_FRAME_TREE = 'InFencedFrameTree'
    IN_ISOLATED_APP = 'InIsolatedApp'


class OriginTrialTokenStatus(Enum):
    """Origin trial token status."""

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


class OriginTrialStatus(Enum):
    """Origin trial status."""

    ENABLED = 'Enabled'
    VALID_TOKEN_NOT_PROVIDED = 'ValidTokenNotProvided'
    OS_NOT_SUPPORTED = 'OSNotSupported'
    TRIAL_NOT_ALLOWED = 'TrialNotAllowed'


class OriginTrialUsageRestriction(Enum):
    """Origin trial usage restriction."""

    NONE = 'None'
    SUBSET = 'Subset'


class TransitionType(Enum):
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


class DialogType(Enum):
    """Dialog types."""

    ALERT = 'alert'
    CONFIRM = 'confirm'
    PROMPT = 'prompt'
    BEFOREUNLOAD = 'beforeunload'


class ClientNavigationReason(Enum):
    """Client navigation reasons."""

    ANCHOR_CLICK = 'anchorClick'
    FORM_SUBMISSION_GET = 'formSubmissionGet'
    FORM_SUBMISSION_POST = 'formSubmissionPost'
    HTTP_HEADER_REFRESH = 'httpHeaderRefresh'
    INITIAL_FRAME_NAVIGATION = 'initialFrameNavigation'
    META_TAG_REFRESH = 'metaTagRefresh'
    OTHER = 'other'
    PAGE_BLOCK_INTERSTITIAL = 'pageBlockInterstitial'
    RELOAD = 'reload'
    SCRIPT_INITIATED = 'scriptInitiated'


class ClientNavigationDisposition(Enum):
    """Client navigation dispositions."""

    CURRENT_TAB = 'currentTab'
    NEW_TAB = 'newTab'
    NEW_WINDOW = 'newWindow'
    DOWNLOAD = 'download'


class ReferrerPolicy(Enum):
    """Referrer policy types."""

    NO_REFERRER = 'noReferrer'
    NO_REFERRER_WHEN_DOWNGRADE = 'noReferrerWhenDowngrade'
    ORIGIN = 'origin'
    ORIGIN_WHEN_CROSS_ORIGIN = 'originWhenCrossOrigin'
    SAME_ORIGIN = 'sameOrigin'
    STRICT_ORIGIN = 'strictOrigin'
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN = 'strictOriginWhenCrossOrigin'
    UNSAFE_URL = 'unsafeUrl'


class NavigationType(Enum):
    """Navigation types."""

    NAVIGATION = 'Navigation'
    BACK_FORWARD_CACHE_RESTORE = 'BackForwardCacheRestore'


class AdFrameStatus(TypedDict):
    """Ad frame status."""

    adFrameType: AdFrameType
    explanations: NotRequired[list[AdFrameExplanation]]


class AdScriptId(TypedDict):
    """Ad script identifier."""

    scriptId: ScriptId
    debuggerId: UniqueDebuggerId


class AdScriptAncestry(TypedDict):
    """Ad script ancestry."""

    ancestryChain: list[AdScriptId]
    rootScriptFilterlistRule: NotRequired[str]


class PermissionsPolicyBlockLocator(TypedDict):
    """Permissions policy block locator."""

    frameId: FrameId
    blockReason: PermissionsPolicyBlockReason


class PermissionsPolicyFeatureState(TypedDict):
    """Permissions policy feature state."""

    feature: PermissionsPolicyFeature
    allowed: bool
    locator: NotRequired[PermissionsPolicyBlockLocator]


class OriginTrialToken(TypedDict):
    """Origin trial token."""

    origin: str
    matchSubDomains: bool
    trialName: str
    expiryTime: TimeSinceEpoch
    isThirdParty: bool
    usageRestriction: OriginTrialUsageRestriction


class OriginTrialTokenWithStatus(TypedDict):
    """Origin trial token with status."""

    rawTokenText: str
    status: OriginTrialTokenStatus
    parsedToken: NotRequired[OriginTrialToken]


class OriginTrial(TypedDict):
    """Origin trial."""

    trialName: str
    status: OriginTrialStatus
    tokensWithStatus: list[OriginTrialTokenWithStatus]


class SecurityOriginDetails(TypedDict):
    """Security origin details."""

    isLocalhost: bool


class Frame(TypedDict):
    """Frame information."""

    id: FrameId
    loaderId: LoaderId
    url: str
    domainAndRegistry: str
    securityOrigin: str
    mimeType: str
    secureContextType: SecureContextType
    crossOriginIsolatedContextType: CrossOriginIsolatedContextType
    gatedAPIFeatures: list[GatedAPIFeatures]
    parentId: NotRequired[FrameId]
    name: NotRequired[str]
    urlFragment: NotRequired[str]
    securityOriginDetails: NotRequired[SecurityOriginDetails]
    unreachableUrl: NotRequired[str]
    adFrameStatus: NotRequired[AdFrameStatus]


class FrameResource(TypedDict):
    """Frame resource information."""

    url: str
    type: ResourceType
    mimeType: str
    lastModified: NotRequired[TimeSinceEpoch]
    contentSize: NotRequired[float]
    failed: NotRequired[bool]
    canceled: NotRequired[bool]


class FrameResourceTree(TypedDict):
    """Frame resource tree."""

    frame: Frame
    resources: list[FrameResource]
    childFrames: NotRequired[list['FrameResourceTree']]


class FrameTree(TypedDict):
    """Frame tree."""

    frame: Frame
    childFrames: NotRequired[list['FrameTree']]


class NavigationEntry(TypedDict):
    """Navigation entry."""

    id: int
    url: str
    userTypedURL: str
    title: str
    transitionType: TransitionType


class ScreencastFrameMetadata(TypedDict):
    """Screencast frame metadata."""

    offsetTop: float
    pageScaleFactor: float
    deviceWidth: float
    deviceHeight: float
    scrollOffsetX: float
    scrollOffsetY: float
    timestamp: NotRequired[TimeSinceEpoch]


class AppManifestError(TypedDict):
    """App manifest error."""

    message: str
    critical: int
    line: int
    column: int


class AppManifestParsedProperties(TypedDict):
    """App manifest parsed properties."""

    scope: str


class LayoutViewport(TypedDict):
    """Layout viewport."""

    pageX: int
    pageY: int
    clientWidth: int
    clientHeight: int


class VisualViewport(TypedDict):
    """Visual viewport."""

    offsetX: float
    offsetY: float
    pageX: float
    pageY: float
    clientWidth: float
    clientHeight: float
    scale: float
    zoom: NotRequired[float]


class Viewport(TypedDict):
    """Viewport for capturing screenshot."""

    x: float
    y: float
    width: float
    height: float
    scale: float


class FontFamilies(TypedDict, total=False):
    """Font families."""

    standard: str
    fixed: str
    serif: str
    sansSerif: str
    cursive: str
    fantasy: str
    math: str


class ScriptFontFamilies(TypedDict):
    """Script font families."""

    script: str
    fontFamilies: FontFamilies


class FontSizes(TypedDict, total=False):
    """Font sizes."""

    standard: int
    fixed: int


class CompilationCacheParams(TypedDict):
    """Compilation cache parameters."""

    url: str
    eager: NotRequired[bool]


class FileFilter(TypedDict, total=False):
    """File filter."""

    name: str
    accepts: list[str]


class ImageResource(TypedDict):
    """Image resource."""

    url: str
    sizes: NotRequired[str]
    type: NotRequired[str]


class FileHandler(TypedDict):
    """File handler."""

    action: str
    name: str
    launchType: str
    icons: NotRequired[list[ImageResource]]
    accepts: NotRequired[list[FileFilter]]


class LaunchHandler(TypedDict):
    """Launch handler."""

    clientMode: str


class ProtocolHandler(TypedDict):
    """Protocol handler."""

    protocol: str
    url: str


class RelatedApplication(TypedDict):
    """Related application."""

    url: str
    id: NotRequired[str]


class ScopeExtension(TypedDict):
    """Scope extension."""

    origin: str
    hasOriginWildcard: bool


class Screenshot(TypedDict):
    """Screenshot."""

    image: ImageResource
    formFactor: str
    label: NotRequired[str]


class ShareTarget(TypedDict):
    """Share target."""

    action: str
    method: str
    enctype: str
    title: NotRequired[str]
    text: NotRequired[str]
    url: NotRequired[str]
    files: NotRequired[list[FileFilter]]


class Shortcut(TypedDict):
    """Shortcut."""

    name: str
    url: str


class WebAppManifest(TypedDict, total=False):
    """Web app manifest."""

    backgroundColor: str
    description: str
    dir: str
    display: str
    displayOverrides: list[str]
    fileHandlers: list[FileHandler]
    icons: list[ImageResource]
    id: str
    lang: str
    launchHandler: LaunchHandler
    name: str
    orientation: str
    preferRelatedApplications: bool
    protocolHandlers: list[ProtocolHandler]
    relatedApplications: list[RelatedApplication]
    scope: str
    scopeExtensions: list[ScopeExtension]
    screenshots: list[Screenshot]
    shareTarget: ShareTarget
    shortName: str
    shortcuts: list[Shortcut]
    startUrl: str
    themeColor: str


class InstallabilityErrorArgument(TypedDict):
    """Installability error argument."""

    name: str
    value: str


class InstallabilityError(TypedDict):
    """Installability error."""

    errorId: str
    errorArguments: list[InstallabilityErrorArgument]
