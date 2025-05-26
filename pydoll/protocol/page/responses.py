from typing import List, NotRequired, TypedDict

from pydoll.protocol.base import Response
from pydoll.protocol.dom.types import Rect
from pydoll.protocol.network.types import SearchMatch
from pydoll.protocol.page.types import (
    AdScriptId,
    AppManifestError,
    FrameResourceTree,
    FrameTree,
    InstallabilityError,
    LayoutViewport,
    NavigationEntry,
    OriginTrial,
    PermissionsPolicyFeatureState,
    VisualViewport,
    WebAppManifest,
)


class AddScriptToEvaluateOnNewDocumentResultDict(TypedDict):
    """Response result for addScriptToEvaluateOnNewDocument command."""

    identifier: str


class CaptureScreenshotResultDict(TypedDict):
    """Response result for captureScreenshot command."""

    data: str  # Base64-encoded image data


class CreateIsolatedWorldResultDict(TypedDict):
    """Response result for createIsolatedWorld command."""

    executionContextId: int


class GetAppManifestResultDict(TypedDict):
    """Response result for getAppManifest command."""

    url: str
    errors: List[AppManifestError]
    data: str  # Manifest content as string
    manifest: NotRequired[WebAppManifest]


class GetFrameTreeResultDict(TypedDict):
    """Response result for getFrameTree command."""

    frameTree: FrameTree


class GetLayoutMetricsResultDict(TypedDict):
    """Response result for getLayoutMetrics command."""

    cssLayoutViewport: LayoutViewport
    cssVisualViewport: VisualViewport
    cssContentSize: Rect


class GetNavigationHistoryResultDict(TypedDict):
    """Response result for getNavigationHistory command."""

    currentIndex: int
    entries: List[NavigationEntry]


class NavigateResultDict(TypedDict):
    """Response result for navigate command."""

    frameId: str
    loaderId: NotRequired[str]
    errorText: NotRequired[str]


class PrintToPDFResultDict(TypedDict):
    """Response result for printToPDF command."""

    data: str  # Base64-encoded pdf data
    stream: NotRequired[str]  # A handle to the stream that holds the PDF data


class CaptureSnapshotResultDict(TypedDict):
    """Response result for captureSnapshot command."""

    data: str  # Base64-encoded image data


class GetAdScriptAncestryIdsResultDict(TypedDict):
    """Response result for getAdScriptAncestryIds command."""

    adScriptAncestryIds: List[AdScriptId]


class GetAppIdResultDict(TypedDict):
    """Response result for getAppId command."""

    appId: NotRequired[str]
    recommendedId: NotRequired[str]


class GetInstallabilityErrorsResultDict(TypedDict):
    """Response result for getInstallabilityErrors command."""

    installabilityErrors: List[InstallabilityError]


class GetOriginTrialsResultDict(TypedDict):
    """Response result for getOriginTrials command."""

    originTrials: List[OriginTrial]


class GetPermissionsPolicyStateResultDict(TypedDict):
    """Response result for getPermissionsPolicyState command."""

    states: List[PermissionsPolicyFeatureState]


class GetResourceContentResultDict(TypedDict):
    """Response result for getResourceContent command."""

    content: str
    base64Encoded: bool


class GetResourceTreeResultDict(TypedDict):
    """Response result for getResourceTree command."""

    frameTree: FrameResourceTree


class SearchInResourceResultDict(TypedDict):
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
