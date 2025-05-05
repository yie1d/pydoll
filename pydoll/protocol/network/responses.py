from typing import List, NotRequired

from pydoll.protocol.base import Response, ResponseResult
from pydoll.protocol.network.types import Cookie,SecurityIsolationStatus, SearchMatch
from pydoll.protocol.fetch.types import HeaderEntry


class GetCookiesResultDict(ResponseResult):
    """Response result for getCookies command."""

    cookies: List[Cookie]


class GetRequestPostDataResultDict(ResponseResult):
    """Response result for getRequestPostData command."""

    postData: str


class GetResponseBodyResultDict(ResponseResult):
    """Response result for getResponseBody command."""

    body: str
    base64Encoded: bool


class GetResponseBodyForInterceptionResultDict(ResponseResult):
    """Response result for getResponseBodyForInterception command."""

    body: str
    base64Encoded: bool


class GetCertificateResultDict(ResponseResult):
    """Response result for getCertificate command."""

    tableNames: List[str]


class SearchInResponseBodyResultDict(ResponseResult):
    """Response result for searchInResponseBody command."""

    result: List[SearchMatch]


class SetCookieResultDict(ResponseResult):
    """Response result for setCookie command."""

    success: bool


class StreamResourceContentResultDict(ResponseResult):
    """Response result for streamResourceContent command."""

    bufferedData: str


class TakeResponseBodyForInterceptionAsStreamResultDict(ResponseResult):
    """Response result for takeResponseBodyForInterceptionAsStream command."""

    stream: str


class CanClearBrowserCacheResultDict(ResponseResult):
    """Response result for canClearBrowserCache command."""

    result: bool


class CanClearBrowserCookiesResultDict(ResponseResult):
    """Response result for canClearBrowserCookies command."""

    result: bool


class CanEmulateNetworkConditionsResultDict(ResponseResult):
    """Response result for canEmulateNetworkConditions command."""

    result: bool


class GetSecurityIsolationStatusResultDict(ResponseResult):
    """Response result for getSecurityIsolationStatus command."""

    status: SecurityIsolationStatus


class LoadNetworkResourceResultDict(ResponseResult):
    """Response result for loadNetworkResource command."""

    success: bool
    netError: NotRequired[float]
    netErrorName: NotRequired[str]
    httpStatusCode: NotRequired[float]
    stream: NotRequired[str]
    headers: NotRequired[List[HeaderEntry]]


# Response classes that inherit from Response
class GetCookiesResponse(Response):
    """Response for getCookies command."""

    result: GetCookiesResultDict


class GetRequestPostDataResponse(Response):
    """Response for getRequestPostData command."""

    result: GetRequestPostDataResultDict


class GetResponseBodyResponse(Response):
    """Response for getResponseBody command."""

    result: GetResponseBodyResultDict


class GetResponseBodyForInterceptionResponse(Response):
    """Response for getResponseBodyForInterception command."""

    result: GetResponseBodyForInterceptionResultDict


class GetCertificateResponse(Response):
    """Response for getCertificate command."""

    result: GetCertificateResultDict


class SearchInResponseBodyResponse(Response):
    """Response for searchInResponseBody command."""

    result: SearchInResponseBodyResultDict


class SetCookieResponse(Response):
    """Response for setCookie command."""

    result: SetCookieResultDict


class StreamResourceContentResponse(Response):
    """Response for streamResourceContent command."""

    result: StreamResourceContentResultDict


class TakeResponseBodyForInterceptionAsStreamResponse(Response):
    """Response for takeResponseBodyForInterceptionAsStream command."""

    result: TakeResponseBodyForInterceptionAsStreamResultDict


class CanClearBrowserCacheResponse(Response):
    """Response for canClearBrowserCache command."""

    result: CanClearBrowserCacheResultDict


class CanClearBrowserCookiesResponse(Response):
    """Response for canClearBrowserCookies command."""

    result: CanClearBrowserCookiesResultDict


class CanEmulateNetworkConditionsResponse(Response):
    """Response for canEmulateNetworkConditions command."""

    result: CanEmulateNetworkConditionsResultDict


class GetSecurityIsolationStatusResponse(Response):
    """Response for getSecurityIsolationStatus command."""

    result: GetSecurityIsolationStatusResultDict


class LoadNetworkResourceResponse(Response):
    """Response for loadNetworkResource command."""

    result: LoadNetworkResourceResultDict
