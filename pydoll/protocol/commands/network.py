import copy


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

    CLEAR_BROWSER_CACHE = {'method': 'Network.clearBrowserCache'}
    CLEAR_BROWSER_COOKIES = {'method': 'Network.clearBrowserCookies'}
    DELETE_COOKIES_TEMPLATE = {'method': 'Network.deleteCookies', 'params': {}}
    DISABLE = {'method': 'Network.disable'}
    ENABLE = {'method': 'Network.enable'}
    GET_COOKIES_TEMPLATE = {'method': 'Network.getCookies', 'params': {}}
    GET_REQUEST_POST_DATA_TEMPLATE = {
        'method': 'Network.getRequestPostData',
        'params': {},
    }
    GET_RESPONSE_BODY_TEMPLATE = {
        'method': 'Network.getResponseBody',
        'params': {},
    }
    SET_CACHE_DISABLED_TEMPLATE = {
        'method': 'Network.setCacheDisabled',
        'params': {},
    }
    SET_COOKIE_TEMPLATE = {'method': 'Network.setCookie', 'params': {}}
    SET_COOKIES_TEMPLATE = {'method': 'Network.setCookies', 'params': {}}
    SET_EXTRA_HTTP_HEADERS_TEMPLATE = {
        'method': 'Network.setExtraHTTPHeaders',
        'params': {},
    }
    SET_USERAGENT_OVERRIDE_TEMPLATE = {
        'method': 'Network.setUserAgentOverride',
        'params': {},
    }
    GET_ALL_COOKIES = {'method': 'Network.getAllCookies'}
    SEARCH_IN_RESPONSE_TEMPLATE = {
        'method': 'Network.searchInResponseBody',
        'params': {},
    }
    SET_BLOCKED_URLS = {'method': 'Network.setBlockedURLs', 'params': {}}

    @classmethod
    def clear_browser_cache(cls):
        """
        Command to clear the browser's cache.

        This is useful when you want to ensure that your application retrieves
        the most up-to-date resources from the server instead of loading
        potentially stale data from the cache.

        Args:
            None

        Returns:
            dict: A command to clear the browser's cache.
        """
        return cls.CLEAR_BROWSER_CACHE

    @classmethod
    def clear_browser_cookies(cls):
        """
        Command to clear all cookies stored in the browser.

        This can be beneficial for testing scenarios where you need
        to simulate a fresh user session without any previously stored
        cookies that might affect the application's behavior.

        Args:
            None

        Returns:
            dict: A command to clear all cookies in the browser.
        """
        return cls.CLEAR_BROWSER_COOKIES

    @classmethod
    def delete_cookies(cls, name: str, url: str = ''):
        """
        Creates a command to delete a specific cookie by name.

        Args:
            name (str): The name of the cookie to delete.
            url (str, optional): The URL associated with the cookie.
            If specified, only the cookie matching both the name and
            URL will be deleted. If omitted, all cookies with the given
            name will be deleted regardless of URL.

        Returns:
            dict: A command to delete the specified cookie.
        """
        delete_cookies_template = copy.deepcopy(cls.DELETE_COOKIES_TEMPLATE)
        delete_cookies_template['params']['name'] = name
        if url:
            delete_cookies_template['params']['url'] = url
        return delete_cookies_template

    @classmethod
    def disable_network_events(cls):
        """
        Command to disable network event notifications.

        Use this command when you want to temporarily suspend the emission of
        network events, which can be useful during specific operations
        where you don't want to be notified about every network request
        and response.

        Args:
            None

        Returns:
            dict: A command to disable network event notifications.
        """
        return cls.DISABLE

    @classmethod
    def enable_network_events(cls):
        """
        Command to enable network event notifications.

        This allows you to start receiving network-related events again after
        they have been disabled. It's essential to call this before you expect
        to receive network events.

        Args:
            None

        Returns:
            dict: A command to enable network event notifications.
        """
        return cls.ENABLE

    @classmethod
    def get_cookies(cls, urls: list[str] = []):
        """
        Creates a command to retrieve cookies from specified URLs.

        Args:
            urls (list[str], optional): A list of URLs for which to retrieve
                cookies. If not provided, cookies from all URLs will
                be fetched.

        Returns:
            dict: A command to get cookies associated with the specified URLs.
        """
        get_cookies_template = copy.deepcopy(cls.GET_COOKIES_TEMPLATE)
        if urls:
            get_cookies_template['params']['urls'] = urls
        return get_cookies_template

    @classmethod
    def get_request_post_data(cls, request_id: str):
        """
        Creates a command to retrieve POST data associated with a specific
        request.

        Args:
            request_id (str): The unique identifier of the network
                request whose POST data is to be retrieved.

        Returns:
            dict: A command to get the POST data for the specified request.
        """
        get_request_post_data_template = copy.deepcopy(
            cls.GET_REQUEST_POST_DATA_TEMPLATE
        )
        get_request_post_data_template['params']['requestId'] = request_id
        return get_request_post_data_template

    @classmethod
    def get_response_body(cls, request_id: str):
        """
        Creates a command to retrieve the body of a response for a specific
        request.

        Args:
            request_id (str): The unique identifier of the request
                for which the response body is to be fetched.

        Returns:
            dict: A command to get the response body associated with the
                specified request.
        """
        get_response_body_template = copy.deepcopy(
            cls.GET_RESPONSE_BODY_TEMPLATE
        )
        get_response_body_template['params']['requestId'] = request_id
        return get_response_body_template

    @classmethod
    def set_cache_disabled(cls, cache_disabled: bool):
        """
        Creates a command to enable or disable the browser cache.

        Args:
            cache_disabled (bool): Set to True to disable caching, or False to
                enable it.

        Returns:
            dict: A command to set the cache state in the browser.
        """
        set_cache_disabled_template = copy.deepcopy(
            cls.SET_CACHE_DISABLED_TEMPLATE
        )
        set_cache_disabled_template['params']['cacheDisabled'] = cache_disabled
        return set_cache_disabled_template

    @classmethod
    def set_cookie(cls, name: str, value: str, url: str = ''):
        """
        Creates a command to set a specific cookie.

        Args:
            name (str): The name of the cookie.
            value (str): The value of the cookie.
            url (str, optional): The URL associated with the cookie.
                If provided, the cookie will be valid for this URL only.

        Returns:
            dict: A command to set the specified cookie in the browser.
        """
        set_cookie_template = copy.deepcopy(cls.SET_COOKIE_TEMPLATE)
        set_cookie_template['params']['name'] = name
        set_cookie_template['params']['value'] = value
        if url:
            set_cookie_template['params']['url'] = url
        return set_cookie_template

    @classmethod
    def set_cookies(cls, cookies: list[dict]):
        """
        Creates a command to set multiple cookies at once.

        Args:
            cookies (list[dict]): A list of dictionaries, each representing a
                cookie with its properties (name, value, url, etc.).

        Returns:
            dict: A command to set the specified cookies in the browser.
        """
        set_cookies_template = copy.deepcopy(cls.SET_COOKIES_TEMPLATE)
        set_cookies_template['params']['cookies'] = cookies
        return set_cookies_template

    @classmethod
    def set_extra_http_headers(cls, headers: dict):
        """
        Creates a command to set additional HTTP headers for subsequent network
        requests.

        Args:
            headers (dict): A dictionary of headers to include in all future
                requests.

        Returns:
            dict: A command to set extra HTTP headers for the browser's network
                requests.
        """
        set_extra_http_headers_template = copy.deepcopy(
            cls.SET_EXTRA_HTTP_HEADERS_TEMPLATE
        )
        set_extra_http_headers_template['params']['headers'] = headers
        return set_extra_http_headers_template

    @classmethod
    def set_useragent_override(cls, user_agent: str):
        """
        Creates a command to override the user agent string used in network
        requests.

        Args:
            user_agent (str): The user agent string to set for future network
                requests.

        Returns:
            dict: A command to override the browser's user agent for network
                requests.
        """
        set_useragent_override_template = copy.deepcopy(
            cls.SET_USERAGENT_OVERRIDE_TEMPLATE
        )
        set_useragent_override_template['params']['userAgent'] = user_agent
        return set_useragent_override_template

    @classmethod
    def get_all_cookies(cls):
        """
        Command to retrieve all cookies stored in the browser.

        This can be useful for diagnostics, testing, or ensuring that your
        application behaves as expected when accessing cookies.

        Args:
            None

        Returns:
            dict: A command to retrieve all cookies in the browser.
        """
        return cls.GET_ALL_COOKIES

    @classmethod
    def search_in_response(
        cls,
        request_id: str,
        query: str,
        case_sensitive: bool = False,
        is_regex: bool = False,
    ):
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
            dict: A command to search the specified query within the response
                body of the given request.
        """
        search_in_response_template = copy.deepcopy(
            cls.SEARCH_IN_RESPONSE_TEMPLATE
        )
        search_in_response_template['params']['requestId'] = request_id
        search_in_response_template['params']['query'] = query
        search_in_response_template['params']['caseSensitive'] = case_sensitive
        search_in_response_template['params']['isRegex'] = is_regex
        return search_in_response_template

    @classmethod
    def set_blocked_urls(cls, urls: list[str]):
        """
        Creates a command to block specific URLs from being requested by the
        browser.

        Args:
            urls (list[str]): A list of URL patterns to block. The browser will
                not make requests to any URLs matching these patterns.

        Returns:
            dict: A command to set the specified URLs as blocked.
        """
        set_blocked_urls_template = copy.deepcopy(cls.SET_BLOCKED_URLS)
        set_blocked_urls_template['params']['urls'] = urls
        return set_blocked_urls_template
