from typing import Any, List, NotRequired, TypedDict, Union

from pydoll.constants import (
    DeepSerializedValueType,
    ObjectPreviewSubtype,
    ObjectPreviewType,
    PropertyPreviewSubtype,
    PropertyPreviewType,
    RemoteObjectSubtype,
    RemoteObjectType,
    UnserializableEnum,
)
from pydoll.protocol.types.responses.base_responses_types import (
    Response,
    ResponseResult,
)


class PropertyPreview(TypedDict):
    name: str
    type: PropertyPreviewType
    value: NotRequired[str]
    valuePreview: NotRequired['ObjectPreview']
    subtype: NotRequired[PropertyPreviewSubtype]


class EntryPreview(TypedDict):
    key: 'ObjectPreview'
    value: 'ObjectPreview'


class DeepSerializedValue(TypedDict):
    type: DeepSerializedValueType
    value: NotRequired[Any]
    objectId: NotRequired[str]
    weakLocalObjectReference: NotRequired[int]


class ObjectPreview(TypedDict):
    type: ObjectPreviewType
    subtype: NotRequired[ObjectPreviewSubtype]
    description: NotRequired[str]
    overflow: bool
    properties: List[PropertyPreview]
    entries: NotRequired[List[EntryPreview]]


class CustomPreview(TypedDict):
    header: str
    bodyGetterId: NotRequired[str]


class RemoteObject(TypedDict):
    type: RemoteObjectType
    subtype: NotRequired[RemoteObjectSubtype]
    className: NotRequired[str]
    value: NotRequired[Any]
    unserializableValue: NotRequired[Union[UnserializableEnum, str]]
    description: NotRequired[str]
    deepSerializedValue: NotRequired[DeepSerializedValue]
    objectId: NotRequired[str]
    preview: NotRequired[ObjectPreview]
    customPreview: NotRequired[CustomPreview]


class CallFrame(TypedDict):
    functionName: str
    scriptId: str
    url: str
    lineNumber: int
    columnNumber: int


class StackTraceId(TypedDict):
    id: str
    debuggerId: str


class StackTrace(TypedDict):
    description: NotRequired[str]
    callFrames: List[CallFrame]
    parent: NotRequired['StackTrace']
    parentId: NotRequired[StackTraceId]


class ExceptionDetails(TypedDict):
    exceptionId: int
    text: str
    lineNumber: int
    columnNumber: int
    scriptId: NotRequired[str]
    url: NotRequired[str]
    stackTrace: NotRequired[StackTrace]
    exception: NotRequired[RemoteObject]
    executionContextId: NotRequired[int]
    exceptionMetaData: NotRequired[dict]


class PropertyDescriptor(TypedDict):
    name: str
    value: NotRequired[RemoteObject]
    writable: bool
    get: NotRequired[RemoteObject]
    set: NotRequired[RemoteObject]
    configurable: bool
    enumerable: bool
    wasThrown: NotRequired[bool]
    isOwn: NotRequired[bool]
    symbol: NotRequired[RemoteObject]


class InternalPropertyDescriptor(TypedDict):
    name: str
    value: NotRequired[RemoteObject]


class PrivatePropertyDescriptor(TypedDict):
    name: str
    value: NotRequired[RemoteObject]
    get: NotRequired[RemoteObject]
    set: NotRequired[RemoteObject]


class AwaitPromiseResultDict(ResponseResult):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class CallFunctionOnResultDict(ResponseResult):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class CompileScriptResultDict(ResponseResult):
    scriptId: NotRequired[str]
    exceptionDetails: NotRequired[ExceptionDetails]


class EvaluateResultDict(ResponseResult):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class GetPropertiesResultDict(ResponseResult):
    result: List[PropertyDescriptor]
    internalProperties: NotRequired[List[InternalPropertyDescriptor]]
    privateProperties: NotRequired[List[PrivatePropertyDescriptor]]
    exceptionDetails: NotRequired[ExceptionDetails]


class GlobalLexicalScopeNamesResultDict(ResponseResult):
    names: List[str]


class QueryObjectsResultDict(ResponseResult):
    objects: List[RemoteObject]


class RunScriptResultDict(ResponseResult):
    result: RemoteObject
    exceptionDetails: NotRequired[ExceptionDetails]


class GetExceptionDetailsResultDict(ResponseResult):
    exceptionDetails: ExceptionDetails


class GetHeapUsageResultDict(ResponseResult):
    usedSize: float
    totalSize: float
    embedderHeapUsedSize: float
    backingStorageSize: float


class GetIsolateIdResultDict(ResponseResult):
    id: str


class AwaitPromiseResponse(Response):
    result: AwaitPromiseResultDict


class CallFunctionOnResponse(Response):
    result: CallFunctionOnResultDict


class CompileScriptResponse(Response):
    result: CompileScriptResultDict


class EvaluateResponse(Response):
    result: EvaluateResultDict


class GetPropertiesResponse(Response):
    result: GetPropertiesResultDict


class GlobalLexicalScopeNamesResponse(Response):
    result: GlobalLexicalScopeNamesResultDict


class QueryObjectsResponse(Response):
    result: QueryObjectsResultDict


class RunScriptResponse(Response):
    result: RunScriptResultDict


class GetHeapUsageResponse(Response):
    result: GetHeapUsageResultDict


class GetIsolateIdResponse(Response):
    result: GetIsolateIdResultDict


class GetHeapUsageResponse(Response):
    result: GetHeapUsageResultDict


class GetIsolateIdResponse(Response):
    result: GetIsolateIdResultDict
