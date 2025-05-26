from typing import List, NotRequired

from pydoll.protocol.base import Response, ResponseResult
from pydoll.protocol.runtime.types import (
    ExceptionDetails,
    InternalPropertyDescriptor,
    PrivatePropertyDescriptor,
    PropertyDescriptor,
    RemoteObject,
)


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
