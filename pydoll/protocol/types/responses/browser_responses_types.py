from pydoll.protocol.types.commands.browser_commands_types import WindowBoundsDict
from pydoll.protocol.types.responses.base_types import Response, ResponseResult


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