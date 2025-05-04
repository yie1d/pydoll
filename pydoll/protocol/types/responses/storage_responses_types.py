from typing import List, TypedDict

from pydoll.constants import StorageType
from pydoll.protocol.types.commands.storage_commands_types import RelatedWebsiteSet
from pydoll.protocol.types.responses.base_responses_types import (
    Response,
    ResponseResult,
)
from pydoll.protocol.types.responses.network_responses_types import Cookie


class UsageForType(TypedDict):
    storageType: StorageType
    usage: float


class SharedStorageEntry(TypedDict):
    key: str
    value: str


class SharedStorageMetadata(TypedDict):
    creationTime: float
    length: int
    remainingBudget: float
    bytesUsed: int


class TrustToken(TypedDict):
    issuerOrigin: str
    count: float


class GetCookiesResultDict(ResponseResult):
    cookies: List[Cookie]


class GetStorageKeyForFrameResultDict(ResponseResult):
    storageKey: str


class GetUsageAndQuotaResultDict(ResponseResult):
    usage: float
    quota: float
    overrideActive: bool
    usageBreakdown: List[UsageForType]


class ClearTrustTokensResultDict(ResponseResult):
    didDeleteTokens: bool


class GetAffectedUrlsForThirdPartyCookieMetadataResultDict(ResponseResult):
    matchedUrls: List[str]


class GetInterestGroupDetailsResultDict(ResponseResult):
    details: dict


class GetRelatedWebsiteSetsResultDict(ResponseResult):
    sets: List[RelatedWebsiteSet]


class GetSharedStorageEntriesResultDict(ResponseResult):
    entries: List[SharedStorageEntry]


class GetSharedStorageMetadataResultDict(ResponseResult):
    metadata: SharedStorageMetadata


class GetTrustTokensResultDict(ResponseResult):
    tokens: List[TrustToken]


class RunBounceTrackingMitigationsResultDict(ResponseResult):
    deletedSites: List[str]


class SendPendingAttributionReportsResultDict(ResponseResult):
    numSent: int


class GetCookiesResponse(Response):
    result: GetCookiesResultDict


class GetStorageKeyForFrameResponse(Response):
    result: GetStorageKeyForFrameResultDict


class GetUsageAndQuotaResponse(Response):
    result: GetUsageAndQuotaResultDict


class ClearTrustTokensResponse(Response):
    result: ClearTrustTokensResultDict


class GetAffectedUrlsForThirdPartyCookieMetadataResponse(Response):
    result: GetAffectedUrlsForThirdPartyCookieMetadataResultDict


class GetInterestGroupDetailsResponse(Response):
    result: GetInterestGroupDetailsResultDict


class GetRelatedWebsiteSetsResponse(Response):
    result: GetRelatedWebsiteSetsResultDict


class GetSharedStorageEntriesResponse(Response):
    result: GetSharedStorageEntriesResultDict


class GetSharedStorageMetadataResponse(Response):
    result: GetSharedStorageMetadataResultDict


class GetTrustTokensResponse(Response):
    result: GetTrustTokensResultDict


class RunBounceTrackingMitigationsResponse(Response):
    result: RunBounceTrackingMitigationsResultDict


class SendPendingAttributionReportsResponse(Response):
    result: SendPendingAttributionReportsResultDict
