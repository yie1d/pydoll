from typing import List, NotRequired, TypedDict

from pydoll.constants import (
    OriginTrialStatus,
    OriginTrialTokenStatus,
    OriginTrialUsageRestriction,
    PermissionsPolicyBlockReason,
    PermissionsPolicyFeature,
    ResourceType,
    TransitionType,
)
from pydoll.protocol.types.commands.page_commands_types import (
    InstallabilityError,
)
from pydoll.protocol.types.responses.base_responses_types import (
    Response,
    ResponseResult,
)
from pydoll.protocol.types.responses.network_responses_types import SearchMatch


class Rect(TypedDict):
    """Rectangle for capturing screenshot or clip rectangle."""

    x: float
    y: float
    width: float
    height: float


class AppManifestError(TypedDict):
    """App manifest error structure."""

    message: str
    critical: NotRequired[int]
    line: NotRequired[int]
    column: NotRequired[int]


class ImageResource(TypedDict):
    url: str
    sizes: NotRequired[str]
    type: NotRequired[str]


class FileFilter(TypedDict):
    name: NotRequired[str]
    accepts: NotRequired[List[str]]


class FileHandler(TypedDict):
    action: str
    name: str
    icons: NotRequired[List[ImageResource]]
    accepts: NotRequired[List[FileFilter]]
    launchType: NotRequired[str]


class LaunchHandler(TypedDict):
    clientMode: str


class ProtocolHandler(TypedDict):
    protocol: str
    url: str


class RelatedApplication(TypedDict):
    id: str
    url: str


class ScopeExtension(TypedDict):
    origin: str
    hasOriginWildcard: bool


class Screenshot(TypedDict):
    image: ImageResource
    formFactor: str
    label: NotRequired[str]


class ShareTarget(TypedDict):
    action: str
    method: str
    enctype: str
    title: NotRequired[str]
    text: NotRequired[str]
    url: NotRequired[str]
    files: NotRequired[List[FileFilter]]


class Shortcut(TypedDict):
    name: str
    url: str


class WebAppManifest(TypedDict):
    backgroundColor: NotRequired[str]
    description: NotRequired[str]
    dir: NotRequired[str]
    display: NotRequired[str]
    displayOverrides: NotRequired[List[str]]
    fileHandlers: NotRequired[List[FileHandler]]
    icons: NotRequired[List[ImageResource]]
    id: NotRequired[str]
    lang: NotRequired[str]
    launchHandler: NotRequired[LaunchHandler]
    name: NotRequired[str]
    orientation: NotRequired[str]
    preferRelatedApplications: NotRequired[bool]
    protocolHandlers: NotRequired[List[ProtocolHandler]]
    relatedApplications: NotRequired[List[RelatedApplication]]
    scope: NotRequired[str]
    scopeExtensions: NotRequired[List[ScopeExtension]]
    screenshots: NotRequired[List[Screenshot]]
    shareTarget: NotRequired[ShareTarget]
    shortName: NotRequired[str]
    shortcuts: NotRequired[List[Shortcut]]
    startUrl: NotRequired[str]
    themeColor: NotRequired[str]


class Frame(TypedDict):
    """Information about a frame."""

    id: str
    loaderId: NotRequired[str]
    url: str
    securityOrigin: NotRequired[str]
    mimeType: NotRequired[str]
    unreachableUrl: NotRequired[str]


class FrameResource(TypedDict):
    url: str
    type: ResourceType
    mimeType: str
    lastModified: NotRequired[str]
    contentSize: NotRequired[float]
    failed: NotRequired[bool]
    canceled: NotRequired[bool]


class FrameResourceTree(TypedDict):
    """Information about frame hierarchy."""

    frame: Frame
    childFrames: NotRequired[List['FrameResourceTree']]
    resources: NotRequired[List[FrameResource]]


class FrameTree(TypedDict):
    frame: Frame
    childFrames: NotRequired[List['FrameTree']]


class LayoutViewport(TypedDict):
    """Layout viewport position and dimensions."""

    pageX: int
    pageY: int
    clientWidth: int
    clientHeight: int


class VisualViewport(TypedDict):
    """Visual viewport position, dimensions, and scale."""

    offsetX: float
    offsetY: float
    pageX: float
    pageY: float
    clientWidth: float
    clientHeight: float
    scale: float
    zoom: NotRequired[float]


class NavigationEntry(TypedDict):
    """Navigation history entry."""

    id: int
    url: str
    userTypedURL: str
    title: str
    transitionType: TransitionType


class AdScriptId(TypedDict):
    scriptId: str
    debuggerId: str


class OriginTrialToken(TypedDict):
    origin: str
    matchSubDomains: bool
    trialName: str
    expiryTime: str
    isThirdParty: bool
    usageRestriction: NotRequired[OriginTrialUsageRestriction]


class OriginTrialTokenWithStatus(TypedDict):
    rawTokenText: str
    parsedTokenText: NotRequired[OriginTrialToken]
    status: OriginTrialTokenStatus


class OriginTrial(TypedDict):
    trialName: str
    status: OriginTrialStatus
    tokenWithStatus: List[OriginTrialTokenWithStatus]


class PermissionsPolicyBlockLocator(TypedDict):
    frameId: str
    blockReason: PermissionsPolicyBlockReason


class PermissionsPolicyFeatureState(TypedDict):
    feature: PermissionsPolicyFeature
    allowed: bool
    locator: NotRequired[PermissionsPolicyBlockLocator]


class AddScriptToEvaluateOnNewDocumentResultDict(ResponseResult):
    """Response result for addScriptToEvaluateOnNewDocument command."""

    identifier: str


class CaptureScreenshotResultDict(ResponseResult):
    """Response result for captureScreenshot command."""

    data: str  # Base64-encoded image data


class CreateIsolatedWorldResultDict(ResponseResult):
    """Response result for createIsolatedWorld command."""

    executionContextId: int


class GetAppManifestResultDict(ResponseResult):
    """Response result for getAppManifest command."""

    url: str
    errors: List[AppManifestError]
    data: str  # Manifest content as string
    manifest: NotRequired[WebAppManifest]


class GetFrameTreeResultDict(ResponseResult):
    """Response result for getFrameTree command."""

    frameTree: FrameTree


class GetLayoutMetricsResultDict(ResponseResult):
    """Response result for getLayoutMetrics command."""

    cssLayoutViewport: LayoutViewport
    cssVisualViewport: VisualViewport
    cssContentSize: Rect


class GetNavigationHistoryResultDict(ResponseResult):
    """Response result for getNavigationHistory command."""

    currentIndex: int
    entries: List[NavigationEntry]


class NavigateResultDict(ResponseResult):
    """Response result for navigate command."""

    frameId: str
    loaderId: NotRequired[str]
    errorText: NotRequired[str]


class PrintToPDFResultDict(ResponseResult):
    """Response result for printToPDF command."""

    data: str  # Base64-encoded pdf data
    stream: NotRequired[str]  # A handle to the stream that holds the PDF data


class CaptureSnapshotResultDict(ResponseResult):
    """Response result for captureSnapshot command."""

    data: str  # Base64-encoded image data


class GetAdScriptAncestryIdsResultDict(ResponseResult):
    """Response result for getAdScriptAncestryIds command."""

    adScriptAncestryIds: List[AdScriptId]


class GetAppIdResultDict(ResponseResult):
    """Response result for getAppId command."""

    appId: NotRequired[str]
    recommendedId: NotRequired[str]


class GetInstallabilityErrorsResultDict(ResponseResult):
    """Response result for getInstallabilityErrors command."""

    installabilityErrors: List[InstallabilityError]


class GetOriginTrialsResultDict(ResponseResult):
    """Response result for getOriginTrials command."""

    originTrials: List[OriginTrial]


class GetPermissionsPolicyStateResultDict(ResponseResult):
    """Response result for getPermissionsPolicyState command."""

    states: List[PermissionsPolicyFeatureState]


class GetResourceContentResultDict(ResponseResult):
    """Response result for getResourceContent command."""

    content: str
    base64Encoded: bool


class GetResourceTreeResultDict(ResponseResult):
    """Response result for getResourceTree command."""

    frameTree: FrameResourceTree


class SearchInResourceResultDict(ResponseResult):
    """Response result for searchInResource command."""

    result: List[SearchMatch]


# Response classes that inherit from Response
class AddScriptToEvaluateOnNewDocumentResponse(Response):
    """Response for addScriptToEvaluateOnNewDocument command."""

    result: AddScriptToEvaluateOnNewDocumentResultDict


class CaptureScreenshotResponse(Response):
    """Response for captureScreenshot command."""

    result: CaptureScreenshotResultDict


class CreateIsolatedWorldResponse(Response):
    """Response for createIsolatedWorld command."""

    result: CreateIsolatedWorldResultDict


class GetAppManifestResponse(Response):
    """Response for getAppManifest command."""

    result: GetAppManifestResultDict


class GetFrameTreeResponse(Response):
    """Response for getFrameTree command."""

    result: GetFrameTreeResultDict


class GetLayoutMetricsResponse(Response):
    """Response for getLayoutMetrics command."""

    result: GetLayoutMetricsResultDict


class GetNavigationHistoryResponse(Response):
    """Response for getNavigationHistory command."""

    result: GetNavigationHistoryResultDict


class NavigateResponse(Response):
    """Response for navigate command."""

    result: NavigateResultDict


class PrintToPDFResponse(Response):
    """Response for printToPDF command."""

    result: PrintToPDFResultDict


class CaptureSnapshotResponse(Response):
    """Response for captureSnapshot command."""

    result: CaptureSnapshotResultDict


class GetAdScriptAncestryIdsResponse(Response):
    """Response for getAdScriptAncestryIds command."""

    result: GetAdScriptAncestryIdsResultDict


class GetAppIdResponse(Response):
    """Response for getAppId command."""

    result: GetAppIdResultDict


class GetInstallabilityErrorsResponse(Response):
    """Response for getInstallabilityErrors command."""

    result: GetInstallabilityErrorsResultDict


class GetOriginTrialsResponse(Response):
    """Response for getOriginTrials command."""

    result: GetOriginTrialsResultDict


class GetPermissionsPolicyStateResponse(Response):
    """Response for getPermissionsPolicyState command."""

    result: GetPermissionsPolicyStateResultDict


class GetResourceContentResponse(Response):
    """Response for getResourceContent command."""

    result: GetResourceContentResultDict


class GetResourceTreeResponse(Response):
    """Response for getResourceTree command."""

    result: GetResourceTreeResultDict


class SearchInResourceResponse(Response):
    """Response for searchInResource command."""

    result: SearchInResourceResultDict
