from typing import TypedDict


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
