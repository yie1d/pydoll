from enum import Enum

from typing_extensions import NotRequired, TypedDict

from pydoll.protocol.base import Command, EmptyParams, EmptyResponse, Response
from pydoll.protocol.debugger.types import SearchMatch
from pydoll.protocol.dom.types import Rect
from pydoll.protocol.io.types import StreamHandle
from pydoll.protocol.network.types import LoaderId
from pydoll.protocol.page.types import (
    AdScriptAncestry,
    AppManifestError,
    AppManifestParsedProperties,
    FrameId,
    FrameResourceTree,
    FrameTree,
    InstallabilityError,
    LayoutViewport,
    NavigationEntry,
    OriginTrial,
    PermissionsPolicyFeatureState,
    ReferrerPolicy,
    ScriptIdentifier,
    TransitionType,
    Viewport,
    VisualViewport,
    WebAppManifest,
)
from pydoll.protocol.runtime.types import ExecutionContextId


class PageMethod(str, Enum):
    ADD_SCRIPT_TO_EVALUATE_ON_NEW_DOCUMENT = 'Page.addScriptToEvaluateOnNewDocument'
    BRING_TO_FRONT = 'Page.bringToFront'
    CAPTURE_SCREENSHOT = 'Page.captureScreenshot'
    CLOSE = 'Page.close'
    CREATE_ISOLATED_WORLD = 'Page.createIsolatedWorld'
    DISABLE = 'Page.disable'
    ENABLE = 'Page.enable'
    GET_APP_MANIFEST = 'Page.getAppManifest'
    GET_FRAME_TREE = 'Page.getFrameTree'
    GET_LAYOUT_METRICS = 'Page.getLayoutMetrics'
    GET_NAVIGATION_HISTORY = 'Page.getNavigationHistory'
    HANDLE_JAVASCRIPT_DIALOG = 'Page.handleJavaScriptDialog'
    NAVIGATE = 'Page.navigate'
    NAVIGATE_TO_HISTORY_ENTRY = 'Page.navigateToHistoryEntry'
    PRINT_TO_PDF = 'Page.printToPDF'
    RELOAD = 'Page.reload'
    REMOVE_SCRIPT_TO_EVALUATE_ON_NEW_DOCUMENT = 'Page.removeScriptToEvaluateOnNewDocument'
    RESET_NAVIGATION_HISTORY = 'Page.resetNavigationHistory'
    SET_BYPASS_CSP = 'Page.setBypassCSP'
    SET_DOCUMENT_CONTENT = 'Page.setDocumentContent'
    SET_INTERCEPT_FILE_CHOOSER_DIALOG = 'Page.setInterceptFileChooserDialog'
    SET_LIFECYCLE_EVENTS_ENABLED = 'Page.setLifecycleEventsEnabled'
    STOP_LOADING = 'Page.stopLoading'
    ADD_COMPILATION_CACHE = 'Page.addCompilationCache'
    CAPTURE_SNAPSHOT = 'Page.captureSnapshot'
    CLEAR_COMPILATION_CACHE = 'Page.clearCompilationCache'
    CRASH = 'Page.crash'
    GENERATE_TEST_REPORT = 'Page.generateTestReport'
    GET_AD_SCRIPT_ANCESTRY_IDS = 'Page.getAdScriptAncestryIds'
    GET_APP_ID = 'Page.getAppId'
    GET_INSTALLABILITY_ERRORS = 'Page.getInstallabilityErrors'
    GET_ORIGIN_TRIALS = 'Page.getOriginTrials'
    GET_PERMISSIONS_POLICY_STATE = 'Page.getPermissionsPolicyState'
    GET_RESOURCE_CONTENT = 'Page.getResourceContent'
    GET_RESOURCE_TREE = 'Page.getResourceTree'
    PRODUCE_COMPILATION_CACHE = 'Page.produceCompilationCache'
    SCREENCAST_FRAME_ACK = 'Page.screencastFrameAck'
    SEARCH_IN_RESOURCE = 'Page.searchInResource'
    SET_AD_BLOCKING_ENABLED = 'Page.setAdBlockingEnabled'
    SET_FONT_FAMILIES = 'Page.setFontFamilies'
    SET_FONT_SIZES = 'Page.setFontSizes'
    SET_PRERENDERING_ALLOWED = 'Page.setPrerenderingAllowed'
    SET_RPH_REGISTRATION_MODE = 'Page.setRPHRegistrationMode'
    SET_SPC_TRANSACTION_MODE = 'Page.setSPCTransactionMode'
    SET_WEB_LIFECYCLE_STATE = 'Page.setWebLifecycleState'
    START_SCREENCAST = 'Page.startScreencast'
    STOP_SCREENCAST = 'Page.stopScreencast'
    WAIT_FOR_DEBUGGER = 'Page.waitForDebugger'


class AddScriptToEvaluateOnNewDocumentParams(TypedDict):
    """Parameters for addScriptToEvaluateOnNewDocument."""

    source: str
    worldName: NotRequired[str]
    includeCommandLineAPI: NotRequired[bool]
    runImmediately: NotRequired[bool]


class CaptureScreenshotParams(TypedDict, total=False):
    """Parameters for captureScreenshot."""

    format: str
    quality: int
    clip: Viewport
    fromSurface: bool
    captureBeyondViewport: bool
    optimizeForSpeed: bool


class CaptureSnapshotParams(TypedDict, total=False):
    """Parameters for captureSnapshot."""

    format: str


class CreateIsolatedWorldParams(TypedDict):
    """Parameters for createIsolatedWorld."""

    frameId: FrameId
    worldName: NotRequired[str]
    grantUniveralAccess: NotRequired[bool]


class GetAppManifestParams(TypedDict, total=False):
    """Parameters for getAppManifest."""

    manifestId: str


class GetAdScriptAncestryParams(TypedDict):
    """Parameters for getAdScriptAncestry."""

    frameId: FrameId


class GetPermissionsPolicyStateParams(TypedDict):
    """Parameters for getPermissionsPolicyState."""

    frameId: FrameId


class GetOriginTrialsParams(TypedDict):
    """Parameters for getOriginTrials."""

    frameId: FrameId


class GetResourceContentParams(TypedDict):
    """Parameters for getResourceContent."""

    frameId: FrameId
    url: str


class HandleJavaScriptDialogParams(TypedDict):
    """Parameters for handleJavaScriptDialog."""

    accept: bool
    promptText: NotRequired[str]


class NavigateParams(TypedDict):
    """Parameters for navigate."""

    url: str
    referrer: NotRequired[str]
    transitionType: NotRequired[TransitionType]
    frameId: NotRequired[FrameId]
    referrerPolicy: NotRequired[ReferrerPolicy]


class NavigateToHistoryEntryParams(TypedDict):
    """Parameters for navigateToHistoryEntry."""

    entryId: int


class PrintToPDFParams(TypedDict, total=False):
    """Parameters for printToPDF."""

    landscape: bool
    displayHeaderFooter: bool
    printBackground: bool
    scale: float
    paperWidth: float
    paperHeight: float
    marginTop: float
    marginBottom: float
    marginLeft: float
    marginRight: float
    pageRanges: str
    headerTemplate: str
    footerTemplate: str
    preferCSSPageSize: bool
    transferMode: str
    generateTaggedPDF: bool
    generateDocumentOutline: bool


class ReloadParams(TypedDict, total=False):
    """Parameters for reload."""

    ignoreCache: bool
    scriptToEvaluateOnLoad: str
    loaderId: LoaderId


class RemoveScriptToEvaluateOnNewDocumentParams(TypedDict):
    """Parameters for removeScriptToEvaluateOnNewDocument."""

    identifier: ScriptIdentifier


class ScreencastFrameAckParams(TypedDict):
    """Parameters for screencastFrameAck."""

    sessionId: int


class SearchInResourceParams(TypedDict):
    """Parameters for searchInResource."""

    frameId: FrameId
    url: str
    query: str
    caseSensitive: NotRequired[bool]
    isRegex: NotRequired[bool]


class SetAdBlockingEnabledParams(TypedDict):
    """Parameters for setAdBlockingEnabled."""

    enabled: bool


class SetBypassCSPParams(TypedDict):
    """Parameters for setBypassCSP."""

    enabled: bool


class AddScriptToEvaluateOnNewDocumentResult(TypedDict):
    identifier: ScriptIdentifier


class CaptureScreenshotResult(TypedDict):
    data: str


class CaptureSnapshotResult(TypedDict):
    data: str


class CreateIsolatedWorldResult(TypedDict):
    executionContextId: ExecutionContextId


class GetAppManifestResult(TypedDict):
    url: str
    errors: list[AppManifestError]
    data: NotRequired[str]
    parsed: NotRequired[AppManifestParsedProperties]
    manifest: NotRequired[WebAppManifest]


class GetInstallabilityErrorsResult(TypedDict):
    installabilityErrors: list[InstallabilityError]


class GetAppIdResult(TypedDict, total=False):
    appId: str
    recommendedId: str


class GetAdScriptAncestryResult(TypedDict, total=False):
    adScriptAncestry: AdScriptAncestry


class GetFrameTreeResult(TypedDict):
    frameTree: FrameTree


class GetLayoutMetricsResult(TypedDict):
    layoutViewport: LayoutViewport
    visualViewport: VisualViewport
    contentSize: Rect
    cssLayoutViewport: LayoutViewport
    cssVisualViewport: VisualViewport
    cssContentSize: Rect


class GetNavigationHistoryResult(TypedDict):
    currentIndex: int
    entries: list[NavigationEntry]


class GetPermissionsPolicyStateResult(TypedDict):
    states: list[PermissionsPolicyFeatureState]


class GetOriginTrialsResult(TypedDict):
    originTrials: list[OriginTrial]


class GetResourceContentResult(TypedDict):
    content: str
    base64Encoded: bool


class GetResourceTreeResult(TypedDict):
    frameTree: FrameResourceTree


class PrintToPDFResult(TypedDict):
    data: str
    stream: NotRequired[StreamHandle]


class SearchInResourceResult(TypedDict):
    result: list[SearchMatch]


class NavigateResult(TypedDict):
    """Result for navigate."""

    frameId: FrameId
    loaderId: NotRequired[LoaderId]
    errorText: NotRequired[str]
    isDownload: NotRequired[bool]


AddScriptToEvaluateOnNewDocumentCommand = Command[
    AddScriptToEvaluateOnNewDocumentParams, Response[AddScriptToEvaluateOnNewDocumentResult]
]
CaptureScreenshotCommand = Command[CaptureScreenshotParams, Response[CaptureScreenshotResult]]
CaptureSnapshotCommand = Command[CaptureSnapshotParams, Response[CaptureSnapshotResult]]
CreateIsolatedWorldCommand = Command[CreateIsolatedWorldParams, Response[CreateIsolatedWorldResult]]
EnableCommand = Command[EmptyParams, EmptyResponse]
GetAppManifestCommand = Command[GetAppManifestParams, Response[GetAppManifestResult]]
GetInstallabilityErrorsCommand = Command[EmptyParams, Response[GetInstallabilityErrorsResult]]
GetAppIdCommand = Command[EmptyParams, Response[GetAppIdResult]]
GetAdScriptAncestryCommand = Command[GetAdScriptAncestryParams, Response[GetAdScriptAncestryResult]]
GetFrameTreeCommand = Command[EmptyParams, Response[GetFrameTreeResult]]
GetLayoutMetricsCommand = Command[EmptyParams, Response[GetLayoutMetricsResult]]
GetNavigationHistoryCommand = Command[EmptyParams, Response[GetNavigationHistoryResult]]
GetPermissionsPolicyStateCommand = Command[
    GetPermissionsPolicyStateParams, Response[GetPermissionsPolicyStateResult]
]
GetOriginTrialsCommand = Command[GetOriginTrialsParams, Response[GetOriginTrialsResult]]
GetResourceContentCommand = Command[GetResourceContentParams, Response[GetResourceContentResult]]
GetResourceTreeCommand = Command[EmptyParams, Response[GetResourceTreeResult]]
HandleJavaScriptDialogCommand = Command[HandleJavaScriptDialogParams, EmptyResponse]
NavigateCommand = Command[NavigateParams, Response[NavigateResult]]
NavigateToHistoryEntryCommand = Command[NavigateToHistoryEntryParams, EmptyResponse]
PrintToPDFCommand = Command[PrintToPDFParams, Response[PrintToPDFResult]]
ReloadCommand = Command[ReloadParams, EmptyResponse]
RemoveScriptToEvaluateOnNewDocumentCommand = Command[
    RemoveScriptToEvaluateOnNewDocumentParams, EmptyResponse
]
ScreencastFrameAckCommand = Command[ScreencastFrameAckParams, EmptyResponse]
SearchInResourceCommand = Command[SearchInResourceParams, Response[SearchInResourceResult]]
SetAdBlockingEnabledCommand = Command[SetAdBlockingEnabledParams, EmptyResponse]
SetBypassCSPCommand = Command[SetBypassCSPParams, EmptyResponse]
