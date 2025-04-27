from typing import List, Optional

from pydoll.constants import (
    ConnectionType,
    ContentEncoding,
    CookieSameSite,
)
from pydoll.protocol.types.commands import (
    Command,
    DeleteCookiesParams,
    EmulateNetworkConditionsParams,
    NetworkEnableParams,
    GetCertificateParams,
    GetCookiesParams,
    GetRequestPostDataParams,
    GetResponseBodyForInterceptionParams,
    GetResponseBodyParams,
    HeaderEntry,
    RequestPattern,
    SearchInResponseBodyParams,
    SetAcceptedEncodingsParams,
    SetAttachDebugStackParams,
    SetBlockedURLsParams,
    SetBypassServiceWorkerParams,
    SetCacheDisabledParams,
    SetCookieControlsParams,
    SetCookieParams,
    SetCookiesParams,
    SetExtraHTTPHeadersParams,
    SetRequestInterceptionParams,
    SetUserAgentOverrideParams,
    StreamResourceContentParams,
    TakeResponseBodyForInterceptionAsStreamParams,
)
from pydoll.protocol.types.commands.network_commands_types import (
    CookiePartitionKey,
)
from pydoll.protocol.types.responses import (
    CanClearBrowserCacheResponse,
    CanClearBrowserCookiesResponse,
    CanEmulateNetworkConditionsResponse,
    GetCertificateResponse,
    GetCookiesResponse,
    GetRequestPostDataResponse,
    GetResponseBodyForInterceptionResponse,
    GetResponseBodyResponse,
    Response,
    SearchInResponseBodyResponse,
    SetCookieResponse,
    StreamResourceContentResponse,
    TakeResponseBodyForInterceptionAsStreamResponse,
)


class NetworkCommands:
    """
    This class encapsulates the network commands of the
    Chrome DevTools Protocol (CDP).

    CDP allows developers to interact with the Chrome browser's internal
    mechanisms to inspect, manipulate, and monitor network operations,
    which can be invaluable for debugging web applications, testing network
    behaviors, and optimizing performance.

    The commands defined in this class provide functionality for:
    - Managing browser cache and cookies.
    - Enabling and disabling network events.
    - Retrieving and modifying request and response data.
    - Customizing HTTP headers and user agent strings.
    - Blocking specific URLs to prevent unwanted network traffic.
    """

    @staticmethod
    def clear_browser_cache() -> Command[Response]:
        """
        Command to clear the browser's cache.

        This is useful when you want to ensure that your application retrieves
        the most up-to-date resources from the server instead of loading
        potentially stale data from the cache.

        Args:
            None

        Returns:
            Command[Response]: A command to clear the browser's cache.
        """
        return Command(method='Network.clearBrowserCache')

    @staticmethod
    def clear_browser_cookies() -> Command[Response]:
        """
        Command to clear all cookies stored in the browser.

        This can be beneficial for testing scenarios where you need
        to simulate a fresh user session without any previously stored
        cookies that might affect the application's behavior.

        Args:
            None

        Returns:
            Command[Response]: A command to clear all cookies in the browser.
        """
        return Command(method='Network.clearBrowserCookies')

    @staticmethod
    def delete_cookies(
        name: str,
        url: Optional[str] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
        partition_key: Optional[CookiePartitionKey] = None,
    ) -> Command[Response]:
        """
        Creates a command to delete a specific cookie by name.

        Args:
            name (str): The name of the cookie to delete.
            url (str, optional): The URL associated with the cookie.
            If specified, only the cookie matching both the name and
            URL will be deleted. If omitted, all cookies with the given
            name will be deleted regardless of URL.
            domain (str, optional): The domain of the cookie to delete.
            path (str, optional): The path of the cookie to delete.

        Returns:
            Command[Response]: A command to delete the specified cookie.
        """
        params = DeleteCookiesParams(name=name)
        if url:
            params['url'] = url
        if domain:
            params['domain'] = domain
        if path:
            params['path'] = path
        if partition_key:
            params['partitionKey'] = partition_key
        return Command(method='Network.deleteCookies', params=params)

    @staticmethod
    def disable_network_events() -> Command[Response]:
        """
        Command to disable network event notifications.

        Use this command when you want to temporarily suspend the emission of
        network events, which can be useful during specific operations
        where you don't want to be notified about every network request
        and response.

        Args:
            None

        Returns:
            Command[Response]: A command to disable network event notifications.
        """
        return Command(method='Network.disable')

    @staticmethod
    def enable_network_events(
        max_total_buffer_size: Optional[int] = None,
        max_resource_buffer_size: Optional[int] = None,
        max_post_data_size: Optional[int] = None,
    ) -> Command[Response]:
        """
        Command to enable network event notifications.

        This allows you to start receiving network-related events again after
        they have been disabled. It's essential to call this before you expect
        to receive network events.

        Args:
            max_total_buffer_size (int, optional): The maximum total buffer size for network events.
            max_resource_buffer_size (int, optional): The maximum resource buffer size for network events.
            max_post_data_size (int, optional): The maximum post data size for network events.

        Returns:
            Command[Response]: A command to enable network event notifications.
        """
        params = NetworkEnableParams()
        if max_total_buffer_size is not None:
            params['maxTotalBufferSize'] = max_total_buffer_size
        if max_resource_buffer_size is not None:
            params['maxResourceBufferSize'] = max_resource_buffer_size
        if max_post_data_size is not None:
            params['maxPostDataSize'] = max_post_data_size
        return Command(method='Network.enable', params=params)

    @staticmethod
    def get_cookies(
        urls: Optional[List[str]] = None,
    ) -> Command[GetCookiesResponse]:
        """
        Creates a command to retrieve cookies from specified URLs.

        Args:
            urls (list[str], optional): A list of URLs for which to retrieve
                cookies. If not provided, cookies from all URLs will
                be fetched.

        Returns:
            Command[GetCookiesResponse]: A command to get cookies associated with the specified URLs.
        """
        params = GetCookiesParams()
        if urls:
            params['urls'] = urls
        return Command(method='Network.getCookies', params=params)

    @staticmethod
    def get_request_post_data(
        request_id: str,
    ) -> Command[GetRequestPostDataResponse]:
        """
        Creates a command to retrieve POST data associated with a specific
        request.

        Args:
            request_id (str): The unique identifier of the network
                request whose POST data is to be retrieved.

        Returns:
            Command[GetRequestPostDataResponse]: A command to get the POST data for the specified request.
        """
        params = GetRequestPostDataParams(requestId=request_id)
        return Command(method='Network.getRequestPostData', params=params)

    @staticmethod
    def get_response_body(request_id: str) -> Command[GetResponseBodyResponse]:
        """
        Creates a command to retrieve the body of a response for a specific
        request.

        Args:
            request_id (str): The unique identifier of the request
                for which the response body is to be fetched.

        Returns:
            Command[GetResponseBodyResponse]: A command to get the response body associated with the
                specified request.
        """
        params = GetResponseBodyParams(requestId=request_id)
        return Command(method='Network.getResponseBody', params=params)

    @staticmethod
    def set_cache_disabled(cache_disabled: bool) -> Command[Response]:
        """
        Creates a command to enable or disable the browser cache.

        Args:
            cache_disabled (bool): Set to True to disable caching, or False to
                enable it.

        Returns:
            Command[Response]: A command to set the cache state in the browser.
        """
        params = SetCacheDisabledParams(cacheDisabled=cache_disabled)
        return Command(method='Network.setCacheDisabled', params=params)

    @staticmethod
    def set_cookie(
        name: str,
        value: str,
        url: Optional[str] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
        secure: Optional[bool] = None,
        http_only: Optional[bool] = None,
        same_site: Optional[CookieSameSite] = None,
        expires: Optional[float] = None,
    ) -> Command[SetCookieResponse]:
        """
        Creates a command to set a specific cookie.

        Args:
            name (str): The name of the cookie.
            value (str): The value of the cookie.
            url (str, optional): The URL associated with the cookie.
                If provided, the cookie will be valid for this URL only.
            domain (str, optional): The domain of the cookie.
            path (str, optional): The path of the cookie.
            secure (bool, optional): Whether the cookie should be marked as secure.
            http_only (bool, optional): Whether the cookie should be marked as HTTP only.
            same_site (CookieSameSite, optional): The SameSite attribute of the cookie.
            expires (float, optional): The expiration date of the cookie as a Unix timestamp.

        Returns:
            Command[SetCookieResponse]: A command to set the specified cookie in the browser.
        """
        params = SetCookieParams(name=name, value=value)
        if url:
            params['url'] = url
        if domain:
            params['domain'] = domain
        if path:
            params['path'] = path
        if secure is not None:
            params['secure'] = secure
        if http_only is not None:
            params['httpOnly'] = http_only
        if same_site:
            params['sameSite'] = same_site
        if expires:
            params['expires'] = expires
        return Command(method='Network.setCookie', params=params)

    @staticmethod
    def set_cookies(cookies: List[SetCookieParams]) -> Command[Response]:
        """
        Creates a command to set multiple cookies at once.

        Args:
            cookies (list[dict]): A list of dictionaries, each representing a
                cookie with its properties (name, value, url, etc.).

        Returns:
            Command[Response]: A command to set the specified cookies in the browser.
        """
        params = SetCookiesParams(cookies=cookies)
        return Command(method='Network.setCookies', params=params)

    @staticmethod
    def set_extra_http_headers(
        headers: List[HeaderEntry],
    ) -> Command[Response]:
        """
        Creates a command to set additional HTTP headers for subsequent network
        requests.

        Args:
            headers (list[HeaderEntry]): A list of headers to include in all future
                requests.

        Returns:
            Command[Response]: A command to set extra HTTP headers for the browser's network
                requests.
        """
        params = SetExtraHTTPHeadersParams(headers=headers)
        return Command(method='Network.setExtraHTTPHeaders', params=params)

    @staticmethod
    def set_useragent_override(
        user_agent: str,
        accept_language: Optional[str] = None,
        platform: Optional[str] = None,
    ) -> Command[Response]:
        """
        Creates a command to override the user agent string used in network
        requests.

        Args:
            user_agent (str): The user agent string to set for future network
                requests.
            accept_language (str, optional): The accept language header to set for future network
                requests.
            platform (str, optional): The platform header to set for future network
                requests.

        Returns:
            Command[Response]: A command to override the browser's user agent for network
                requests.
        """
        params = SetUserAgentOverrideParams(userAgent=user_agent)
        if accept_language:
            params['acceptLanguage'] = accept_language
        if platform:
            params['platform'] = platform
        return Command(method='Network.setUserAgentOverride', params=params)

    @staticmethod
    def search_in_response(
        request_id: str,
        query: str,
        case_sensitive: bool = False,
        is_regex: bool = False,
    ) -> Command[SearchInResponseBodyResponse]:
        """
        Creates a command to search for a specific query in the response body
        of a network request.

        Args:
            request_id (str): The unique identifier of the request to search
                within.
            query (str): The string to search for within the response body.
            case_sensitive (bool, optional): Whether the search should be case
                sensitive. Defaults to False.
            is_regex (bool, optional): Whether the query should be treated as a
                regular expression. Defaults to False.

        Returns:
            Command[SearchInResponseBodyResponse]: A command to search the specified query within the response
                body of the given request.
        """
        params = SearchInResponseBodyParams(requestId=request_id, query=query)
        if case_sensitive:
            params['caseSensitive'] = case_sensitive
        if is_regex:
            params['isRegex'] = is_regex
        return Command(method='Network.searchInResponseBody', params=params)

    @staticmethod
    def set_blocked_urls(urls: List[str]) -> Command[Response]:
        """
        Creates a command to block specific URLs from being requested by the
        browser.

        Args:
            urls (list[str]): A list of URL patterns to block. The browser will
                not make requests to any URLs matching these patterns.

        Returns:
            Command[Response]: A command to set the specified URLs as blocked.
        """
        params = SetBlockedURLsParams(urls=urls)
        return Command(method='Network.setBlockedURLs', params=params)

    @staticmethod
    def can_clear_browser_cache() -> Command[CanClearBrowserCacheResponse]:
        """Tells whether clearing browser cache is supported."""
        return Command(method='Network.canClearBrowserCache')

    @staticmethod
    def can_clear_browser_cookies() -> Command[CanClearBrowserCookiesResponse]:
        """Tells whether clearing browser cookies is supported."""
        return Command(method='Network.canClearBrowserCookies')

    @staticmethod
    def can_emulate_network_conditions() -> Command[
        CanEmulateNetworkConditionsResponse
    ]:
        """Tells whether emulation of network conditions is supported."""
        return Command(method='Network.canEmulateNetworkConditions')

    @staticmethod
    def set_bypass_service_worker(bypass: bool) -> Command[Response]:
        """Toggles ignoring of service worker for each request."""
        params = SetBypassServiceWorkerParams(bypass=bypass)
        return Command(method='Network.setBypassServiceWorker', params=params)

    @staticmethod
    def get_certificate(origin: str) -> Command[GetCertificateResponse]:
        """Returns the DER-encoded certificate."""
        params = GetCertificateParams(origin=origin)
        return Command(method='Network.getCertificate', params=params)

    @staticmethod
    def get_response_body_for_interception(
        interception_id: str,
    ) -> Command[GetResponseBodyForInterceptionResponse]:
        """Returns content served for the given currently intercepted request."""
        params = GetResponseBodyForInterceptionParams(
            interceptionId=interception_id
        )
        return Command(
            method='Network.getResponseBodyForInterception', params=params
        )

    @staticmethod
    def set_accepted_encodings(
        encodings: List[ContentEncoding],
    ) -> Command[Response]:
        """Sets a list of content encodings that will be accepted."""
        params = SetAcceptedEncodingsParams(encodings=encodings)
        return Command(method='Network.setAcceptedEncodings', params=params)

    @staticmethod
    def clear_accepted_encodings_override() -> Command[Response]:
        """Clears accepted encodings set by setAcceptedEncodings."""
        return Command(method='Network.clearAcceptedEncodingsOverride')

    @staticmethod
    def set_attach_debug_stack(enabled: bool) -> Command[Response]:
        """Specifies whether to attach a page script stack id in requests."""
        params = SetAttachDebugStackParams(enabled=enabled)
        return Command(method='Network.setAttachDebugStack', params=params)

    @staticmethod
    def set_cookie_controls(
        enable_third_party_cookie_restriction: bool,
        disable_third_party_cookie_metadata: Optional[bool] = None,
        disable_third_party_cookie_heuristics: Optional[bool] = None,
    ) -> Command[Response]:
        """Sets Controls for third-party cookie access."""
        params = SetCookieControlsParams(
            enableThirdPartyCookieRestriction=enable_third_party_cookie_restriction
        )
        if disable_third_party_cookie_metadata is not None:
            params['disableThirdPartyCookieMetadata'] = (
                disable_third_party_cookie_metadata
            )
        if disable_third_party_cookie_heuristics is not None:
            params['disableThirdPartyCookieHeuristics'] = (
                disable_third_party_cookie_heuristics
            )
        return Command(method='Network.setCookieControls', params=params)

    @staticmethod
    def stream_resource_content(
        request_id: str,
    ) -> Command[StreamResourceContentResponse]:
        """Enables streaming of the response for the given requestId."""
        params = StreamResourceContentParams(requestId=request_id)
        return Command(method='Network.streamResourceContent', params=params)

    @staticmethod
    def take_response_body_for_interception_as_stream(
        interception_id: str,
    ) -> Command[TakeResponseBodyForInterceptionAsStreamResponse]:
        """Returns a handle to the stream representing the response body."""
        params = TakeResponseBodyForInterceptionAsStreamParams(
            interceptionId=interception_id
        )
        return Command(
            method='Network.takeResponseBodyForInterceptionAsStream',
            params=params,
        )

    @staticmethod
    def set_request_interception(
        patterns: List[RequestPattern],
    ) -> Command[Response]:
        """Sets the requests to intercept that match the provided patterns."""
        params = SetRequestInterceptionParams(patterns=patterns)
        return Command(method='Network.setRequestInterception', params=params)

    @staticmethod
    def emulate_network_conditions(
        offline: bool,
        latency: float,
        download_throughput: float,
        upload_throughput: float,
        connection_type: Optional[ConnectionType] = None,
        packet_loss: Optional[float] = None,
        packet_queue_length: Optional[int] = None,
        packet_reordering: Optional[bool] = None,
    ) -> Command[Response]:
        """Activates emulation of network conditions."""
        params = EmulateNetworkConditionsParams(
            offline=offline,
            latency=latency,
            downloadThroughput=download_throughput,
            uploadThroughput=upload_throughput,
        )
        if connection_type:
            params['connectionType'] = connection_type
        if packet_loss is not None:
            params['packetLoss'] = packet_loss
        if packet_queue_length is not None:
            params['packetQueueLength'] = packet_queue_length
        if packet_reordering is not None:
            params['packetReordering'] = packet_reordering
        return Command(
            method='Network.emulateNetworkConditions', params=params
        )
