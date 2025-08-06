from enum import Enum

from typing_extensions import NotRequired, TypedDict

from pydoll.protocol.network.types import ResourceType


class RequestStage(Enum):
    """Stages of the request to handle."""

    REQUEST = 'Request'
    RESPONSE = 'Response'


class AuthChallengeSource(Enum):
    """Source of the authentication challenge."""

    SERVER = 'Server'
    PROXY = 'Proxy'


class AuthChallengeResponseType(Enum):
    """The decision on what to do in response to the authorization challenge."""

    DEFAULT = 'Default'
    CANCEL_AUTH = 'CancelAuth'
    PROVIDE_CREDENTIALS = 'ProvideCredentials'


class RequestPattern(TypedDict, total=False):
    """Pattern for request interception."""

    urlPattern: str  # Wildcards allowed. Omitting is equivalent to "*".
    resourceType: ResourceType
    requestStage: RequestStage


class HeaderEntry(TypedDict):
    """Response HTTP header entry."""

    name: str
    value: str


class AuthChallenge(TypedDict, total=False):
    """Authorization challenge for HTTP status code 401 or 407."""

    source: AuthChallengeSource
    origin: str
    scheme: str  # e.g. basic, digest
    realm: str


class AuthChallengeResponse(TypedDict, total=False):
    """Response to an AuthChallenge."""

    response: AuthChallengeResponseType
    username: str  # Only when response is ProvideCredentials
    password: str  # Only when response is ProvideCredentials


# Legacy compatibility
class AuthChallengeResponseDict(TypedDict):
    """Legacy auth challenge response structure."""

    response: AuthChallengeResponseType
    username: NotRequired[str]
    password: NotRequired[str]
