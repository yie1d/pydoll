from pydoll.protocol.base import Response, ResponseResult
from pydoll.protocol.browser.types import WindowBoundsDict


class GetWindowForTargetResultDict(ResponseResult):
    """Result structure for GetWindowForTarget command."""

    windowId: int
    bounds: WindowBoundsDict


class GetVersionResultDict(ResponseResult):
    """Result structure for GetVersion command."""

    protocolVersion: str
    product: str
    revision: str
    userAgent: str
    jsVersion: str


class GetWindowForTargetResponse(Response):
    """Response structure for GetWindowForTarget command."""

    result: GetWindowForTargetResultDict


class GetVersionResponse(Response):
    """Response structure for GetVersion command."""

    result: GetVersionResultDict
