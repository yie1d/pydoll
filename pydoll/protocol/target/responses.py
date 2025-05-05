from typing import List

from pydoll.protocol.base import Response, ResponseResult
from pydoll.protocol.target.types import TargetInfo


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
