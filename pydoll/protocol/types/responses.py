from typing import TypedDict

from pydoll.protocol.types.commands import WindowBoundsDict


class ResponseResult(TypedDict, total=False):
    """Base structure for all response results."""

    pass


class Response(TypedDict):
    """Base structure for all responses.

    Attributes:
        id: The ID that matches the command ID
        result: The result data for the command
    """

    id: int
    result: ResponseResult


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
