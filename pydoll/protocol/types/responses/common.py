from typing import TypedDict


class ResponseResult(TypedDict, total=False):
    pass


class Response(TypedDict):
    id: int
    result: ResponseResult