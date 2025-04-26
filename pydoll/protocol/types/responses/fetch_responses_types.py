from pydoll.protocol.types.responses.base_types import Response, ResponseResult


class GetResponseBodyResultDict(ResponseResult):
    body: str
    base64encoded: bool


class TakeResponseBodyAsStreamResultDict(ResponseResult):
    stream: str


class GetResponseBodyResponse(Response):
    result: GetResponseBodyResultDict


class TakeResponseBodyAsStreamResponse(Response):
    result: TakeResponseBodyAsStreamResultDict
