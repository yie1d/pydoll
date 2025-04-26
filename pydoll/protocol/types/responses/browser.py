from pydoll.protocol.types.responses.common import Response, ResponseResult
from pydoll.protocol.types.commands.browser import WindowBoundsDict


class GetWindowForTargetResultDict(ResponseResult):
    windowId: int
    bounds: WindowBoundsDict


class GetWindowForTargetResponse(Response):
    result: GetWindowForTargetResultDict