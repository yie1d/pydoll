from typing import Annotated, Any, List, NotRequired, TypedDict

from pydoll.constants import CompatibilityMode, PseudoType, ShadowRootType
from pydoll.protocol.types.responses.base_responses_types import (
    Response,
    ResponseResult,
)
from pydoll.protocol.types.responses.runtime_responses_types import RemoteObject, StackTrace

Quad = Annotated[List[float], 'Format: [x1, y1, x2, y2, x3, y3, x4, y4]']


class BackendNode(TypedDict):
    nodeType: int
    nodeName: str
    backendNodeId: int


class Node(TypedDict):
    nodeId: int
    parentId: NotRequired[int]
    backendNodeId: int
    nodeType: int
    nodeName: str
    localName: str
    nodeValue: str
    childNodeCount: NotRequired[int]
    children: NotRequired[List['Node']]
    attributes: NotRequired[List[str]]
    documentURL: NotRequired[str]
    baseURL: NotRequired[str]
    publicId: NotRequired[str]
    systemId: NotRequired[str]
    internalSubset: NotRequired[str]
    xmlVersion: NotRequired[str]
    name: NotRequired[str]
    value: NotRequired[str]
    pseudoType: NotRequired[PseudoType]
    pseudoIdentifier: NotRequired[str]
    shadowRootType: NotRequired[ShadowRootType]
    frameId: NotRequired[str]
    contentDocument: NotRequired['Node']
    shadowRoots: NotRequired[List['Node']]
    templateContent: NotRequired['Node']
    pseudoElements: NotRequired[List['Node']]
    importedDocument: NotRequired['Node']
    distributedNodes: NotRequired[List[BackendNode]]
    isSVG: NotRequired[bool]
    compatibilityMode: NotRequired[CompatibilityMode]
    assignedSlot: NotRequired[BackendNode]
    isScrollable: NotRequired[bool]


class DetachedElementInfo(TypedDict):
    treeNode: Node
    retainedNodeIds: List[int]


class ShapeOutsideInfo(TypedDict):
    bounds: Quad
    shape: List[Any]
    marginShape: List[Any]


class BoxModel(TypedDict):
    content: Quad
    padding: Quad
    border: Quad
    margin: Quad
    width: int
    height: int
    shapeOutside: NotRequired[ShapeOutsideInfo]


class DescribeNodeResultDict(ResponseResult):
    node: Node


class GetAttributesResultDict(ResponseResult):
    attributes: List[str]


class GetBoxModelResultDict(ResponseResult):
    model: BoxModel


class GetDocumentResultDict(ResponseResult):
    root: Node


class GetNodeForLocationResultDict(ResponseResult):
    backendNodeId: int
    frameId: str
    nodeId: NotRequired[int]


class GetOuterHTMLResultDict(ResponseResult):
    outerHTML: str


class MoveToResultDict(ResponseResult):
    nodeId: int


class QuerySelectorResultDict(ResponseResult):
    nodeId: int


class QuerySelectorAllResultDict(ResponseResult):
    nodeIds: List[int]


class RequestNodeResultDict(ResponseResult):
    nodeId: int


class ResolveNodeResultDict(ResponseResult):
    object: RemoteObject


class SetNodeNameResultDict(ResponseResult):
    nodeId: int


class CollectClassNamesFromSubtreeResultDict(ResponseResult):
    classNames: List[str]


class CopyToResultDict(ResponseResult):
    nodeId: int


class GetAnchorElementResultDict(ResponseResult):
    nodeId: int


class GetContainerForNodeResultDict(ResponseResult):
    nodeId: int


class GetContentQuadsResultDict(ResponseResult):
    quads: List[Quad]


class GetDetachedDomNodesResultDict(ResponseResult):
    detachedNodes: List[DetachedElementInfo]


class GetElementByRelationResultDict(ResponseResult):
    nodeId: int


class GetFileInfoResultDict(ResponseResult):
    path: str


class GetFrameOwnerResultDict(ResponseResult):
    backendNodeId: int
    nodeId: NotRequired[int]


class GetNodesForSubtreeByStyleResultDict(ResponseResult):
    nodeIds: List[int]


class GetNodeStackTracesResultDict(ResponseResult):
    creation: StackTrace


class GetQueryingDescendantForContainerResultDict(ResponseResult):
    nodeIds: List[int]


class GetRelayoutBoundaryResultDict(ResponseResult):
    nodeId: int


class GetSearchResultsResultDict(ResponseResult):
    nodeIds: List[int]


class GetTopLayerElementsResultDict(ResponseResult):
    nodeIds: List[int]


class PerformSearchResultDict(ResponseResult):
    searchId: str
    resultCount: int


class PushNodeByPathToFrontendResultDict(ResponseResult):
    nodeId: int


class PushNodesByBackendIdsToFrontendResultDict(ResponseResult):
    nodeIds: List[int]


class DescribeNodeResponse(Response):
    result: DescribeNodeResultDict


class GetAttributesResponse(Response):
    result: GetAttributesResultDict


class GetBoxModelResponse(Response):
    result: GetBoxModelResultDict


class GetDocumentResponse(Response):
    result: GetDocumentResultDict


class GetNodeForLocationResponse(Response):
    result: GetNodeForLocationResultDict


class GetOuterHTMLResponse(Response):
    result: GetOuterHTMLResultDict


class MoveToResponse(Response):
    result: MoveToResultDict


class QuerySelectorResponse(Response):
    result: QuerySelectorResultDict


class QuerySelectorAllResponse(Response):
    result: QuerySelectorAllResultDict


class RequestNodeResponse(Response):
    result: RequestNodeResultDict


class ResolveNodeResponse(Response):
    result: ResolveNodeResultDict


class SetNodeNameResponse(Response):
    result: SetNodeNameResultDict


class CollectClassNamesFromSubtreeResponse(Response):
    result: CollectClassNamesFromSubtreeResultDict


class CopyToResponse(Response):
    result: CopyToResultDict


class GetAnchorElementResponse(Response):
    result: GetAnchorElementResultDict


class GetContainerForNodeResponse(Response):
    result: GetContainerForNodeResultDict


class GetContentQuadsResponse(Response):
    result: GetContentQuadsResultDict


class GetDetachedDomNodesResponse(Response):
    result: GetDetachedDomNodesResultDict


class GetElementByRelationResponse(Response):
    result: GetElementByRelationResultDict


class GetFileInfoResponse(Response):
    result: GetFileInfoResultDict


class GetFrameOwnerResponse(Response):
    result: GetFrameOwnerResultDict


class GetNodesForSubtreeByStyleResponse(Response):
    result: GetNodesForSubtreeByStyleResultDict


class GetNodeStackTracesResponse(Response):
    result: GetNodeStackTracesResultDict


class GetQueryingDescendantForContainerResponse(Response):
    result: GetQueryingDescendantForContainerResultDict


class GetRelayoutBoundaryResponse(Response):
    result: GetRelayoutBoundaryResultDict


class GetSearchResultsResponse(Response):
    result: GetSearchResultsResultDict


class GetTopLayerElementsResponse(Response):
    result: GetTopLayerElementsResultDict


class PerformSearchResponse(Response):
    result: PerformSearchResultDict


class PushNodeByPathToFrontendResponse(Response):
    result: PushNodeByPathToFrontendResultDict


class PushNodesByBackendIdsToFrontendResponse(Response):
    result: PushNodesByBackendIdsToFrontendResultDict
