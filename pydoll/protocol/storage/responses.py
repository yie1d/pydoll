from typing import List

from pydoll.protocol.base import Response, ResponseResult
from pydoll.protocol.storage.types import (
    RelatedWebsiteSet,
    SharedStorageEntry,
    SharedStorageMetadata,
    TrustToken,
)
from pydoll.protocol.network.types import Cookie
from pydoll.constants import UsageForType


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
