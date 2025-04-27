from typing import List, NotRequired, TypedDict

from pydoll.constants import CookiePriority, CookieSameSite, CookieSourceScheme
from pydoll.protocol.types.commands.network_commands_types import (
    CookiePartitionKey,
)
from pydoll.protocol.types.responses import ResponseResult


class SearchMatch(TypedDict):
    """Search match object."""

    lineNumber: int
    lineContent: str


class Cookie(TypedDict):
    """Cookie object."""

    name: str
    value: str
    domain: str
    path: str
    expires: float
    size: int
    httpOnly: bool
    secure: bool
    session: bool
    sameSite: NotRequired[CookieSameSite]
    priority: NotRequired[CookiePriority]
    sameParty: NotRequired[bool]
    sourceScheme: NotRequired[CookieSourceScheme]
    sourcePort: NotRequired[int]
    partitionKey: NotRequired[CookiePartitionKey]
    partitionKeyOpaque: NotRequired[bool]


class GetCookiesResponse(ResponseResult):
    """Response for getCookies command."""

    cookies: List[Cookie]


class GetRequestPostDataResponse(ResponseResult):
    """Response for getRequestPostData command."""

    postData: str


class GetResponseBodyResponse(ResponseResult):
    """Response for getResponseBody command."""

    body: str
    base64Encoded: bool


class GetResponseBodyForInterceptionResponse(ResponseResult):
    """Response for getResponseBodyForInterception command."""

    body: str
    base64Encoded: bool


class GetCertificateResponse(ResponseResult):
    """Response for getCertificate command."""

    tableNames: List[str]


class SearchInResponseBodyResponse(ResponseResult):
    """Response for searchInResponseBody command."""

    result: List[SearchMatch]


class SetCookieResponse(ResponseResult):
    """Response for setCookie command."""

    success: bool


class StreamResourceContentResponse(ResponseResult):
    """Response for streamResourceContent command."""

    bufferedData: str


class TakeResponseBodyForInterceptionAsStreamResponse(ResponseResult):
    """Response for takeResponseBodyForInterceptionAsStream command."""

    stream: str


class CanClearBrowserCacheResponse(ResponseResult):
    """Response for canClearBrowserCache command."""

    result: bool


class CanClearBrowserCookiesResponse(ResponseResult):
    """Response for canClearBrowserCookies command."""

    result: bool


class CanEmulateNetworkConditionsResponse(ResponseResult):
    """Response for canEmulateNetworkConditions command."""

    result: bool
