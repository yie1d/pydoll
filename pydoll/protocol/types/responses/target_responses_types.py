from typing import List, NotRequired, TypedDict

from pydoll.protocol.types.responses.base_responses_types import (
    Response,
    ResponseResult,
)


class TargetInfo(TypedDict):
    targetId: str
    type: str
    title: str
    url: str
    attached: bool
    openerId: NotRequired[str]
    canAccessOpener: bool
    openerFrameId: NotRequired[str]
    browserContextId: NotRequired[str]
    subtype: NotRequired[str]


class AttachToTargetResultDict(ResponseResult):
    sessionId: str


class CreateBrowserContextResultDict(ResponseResult):
    browserContextId: str


class CreateTargetResultDict(ResponseResult):
    targetId: str


class GetBrowserContextsResultDict(ResponseResult):
    browserContextIds: List[str]


class GetTargetsResultDict(ResponseResult):
    targetInfos: List[TargetInfo]


class AttachToBrowserTargetResultDict(ResponseResult):
    sessionId: str


class GetTargetInfoResultDict(ResponseResult):
    targetInfo: TargetInfo


class AttachToTargetResponse(Response):
    result: AttachToTargetResultDict


class CreateBrowserContextResponse(Response):
    result: CreateBrowserContextResultDict


class CreateTargetResponse(Response):
    result: CreateTargetResultDict


class GetBrowserContextsResponse(Response):
    result: GetBrowserContextsResultDict


class GetTargetsResponse(Response):
    result: GetTargetsResultDict


class AttachToBrowserTargetResponse(Response):
    result: AttachToBrowserTargetResultDict


class GetTargetInfoResponse(Response):
    result: GetTargetInfoResultDict
