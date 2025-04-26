from typing import List, NotRequired, TypedDict

from pydoll.protocol.types.commands.base_types import CommandParams
from pydoll.protocol.types.enums import (
    AuthChallengeResponseValues,
    RequestMethods,
    ResourceType,
    RequestStage
)


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
    method: NotRequired[RequestMethods]
    postData: NotRequired[dict]
    headers: NotRequired[List[HeaderEntry]]
    interceptResponse: NotRequired[bool]


class ContinueWithAuthParams(CommandParams):
    requestId: str
    authChallengeResponse: AuthChallengeResponseDict


class EnableParams(CommandParams):
    patterns: NotRequired[List[RequestPattern]]
    handleAuthRequests: NotRequired[bool] 