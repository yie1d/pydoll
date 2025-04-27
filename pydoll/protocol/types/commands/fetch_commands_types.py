from typing import List, NotRequired, TypedDict

from pydoll.constants import (
    AuthChallengeResponseValues,
    NetworkErrorReason,
    RequestMethod,
    RequestStage,
    ResourceType,
)
from pydoll.protocol.types.commands.base_commands_types import CommandParams


class HeaderEntry(TypedDict):
    """HTTP header entry structure."""

    name: str
    value: str


class AuthChallengeResponseDict(TypedDict):
    response: AuthChallengeResponseValues
    username: NotRequired[str]
    password: NotRequired[str]


class RequestPattern(TypedDict):
    urlPattern: str
    resourceType: NotRequired[ResourceType]
    requestStage: NotRequired[RequestStage]


class ContinueRequestParams(CommandParams):
    """Parameters for continuing a request."""

    requestId: str
    url: NotRequired[str]
    method: NotRequired[RequestMethod]
    postData: NotRequired[dict]
    headers: NotRequired[List[HeaderEntry]]
    interceptResponse: NotRequired[bool]


class ContinueWithAuthParams(CommandParams):
    requestId: str
    authChallengeResponse: AuthChallengeResponseDict


class FetchEnableParams(CommandParams):
    patterns: NotRequired[List[RequestPattern]]
    handleAuthRequests: NotRequired[bool]


class FailRequestParams(CommandParams):
    requestId: str
    errorReason: NetworkErrorReason


class FulfillRequestParams(CommandParams):
    requestId: str
    responseCode: int
    responseHeaders: NotRequired[List[HeaderEntry]]
    body: NotRequired[dict]
    responsePhrase: NotRequired[str]


class GetResponseBodyParams(CommandParams):
    requestId: str


class TakeResponseBodyAsStreamParams(CommandParams):
    requestId: str


class ContinueResponseParams(CommandParams):
    requestId: str
    responseCode: NotRequired[int]
    responsePhrase: NotRequired[str]
    responseHeaders: NotRequired[List[HeaderEntry]]
