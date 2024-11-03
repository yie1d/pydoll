class NetworkCommands:
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
        return cls.CLEAR_BROWSER_CACHE

    @classmethod
    def clear_browser_cookies(cls):
        return cls.CLEAR_BROWSER_COOKIES

    @classmethod
    def delete_cookies(cls, name: str, url: str = ''):
        delete_cookies_template = cls.DELETE_COOKIES_TEMPLATE.copy()
        delete_cookies_template['params']['name'] = name
        delete_cookies_template['params']['url'] = url if url else None
        return delete_cookies_template

    @classmethod
    def disable_network_events(cls):
        return cls.DISABLE

    @classmethod
    def enable_network_events(cls):
        return cls.ENABLE

    @classmethod
    def get_cookies(cls, urls: list[str] = []):
        get_cookies_template = cls.GET_COOKIES_TEMPLATE.copy()
        get_cookies_template['params']['urls'] = urls if urls else None
        return get_cookies_template

    @classmethod
    def get_request_post_data(cls, request_id: str):
        get_request_post_data_template = (
            cls.GET_REQUEST_POST_DATA_TEMPLATE.copy()
        )
        get_request_post_data_template['params']['requestId'] = request_id
        return get_request_post_data_template

    @classmethod
    def get_response_body(cls, request_id: str):
        get_response_body_template = cls.GET_RESPONSE_BODY_TEMPLATE.copy()
        get_response_body_template['params']['requestId'] = request_id
        return get_response_body_template

    @classmethod
    def set_cache_disabled(cls, cache_disabled: bool):
        set_cache_disabled_template = cls.SET_CACHE_DISABLED_TEMPLATE.copy()
        set_cache_disabled_template['params']['cacheDisabled'] = cache_disabled
        return set_cache_disabled_template

    @classmethod
    def set_cookie(cls, name: str, value: str, url: str = ''):
        set_cookie_template = cls.SET_COOKIE_TEMPLATE.copy()
        set_cookie_template['params']['name'] = name
        set_cookie_template['params']['value'] = value
        set_cookie_template['params']['url'] = url if url else None
        return set_cookie_template

    @classmethod
    def set_cookies(cls, cookies: list[dict]):
        set_cookies_template = cls.SET_COOKIES_TEMPLATE.copy()
        set_cookies_template['params']['cookies'] = cookies
        return set_cookies_template

    @classmethod
    def set_extra_http_headers(cls, headers: dict):
        set_extra_http_headers_template = (
            cls.SET_EXTRA_HTTP_HEADERS_TEMPLATE.copy()
        )
        set_extra_http_headers_template['params']['headers'] = headers
        return set_extra_http_headers_template

    @classmethod
    def set_useragent_override(cls, user_agent: str):
        set_useragent_override_template = (
            cls.SET_USERAGENT_OVERRIDE_TEMPLATE.copy()
        )
        set_useragent_override_template['params']['userAgent'] = user_agent
        return set_useragent_override_template

    @classmethod
    def get_all_cookies(cls):
        return cls.GET_ALL_COOKIES

    @classmethod
    def search_in_response(
        cls,
        request_id: str,
        query: str,
        case_sensitive: bool = False,
        is_regex: bool = False,
    ):
        search_in_response_template = cls.SEARCH_IN_RESPONSE_TEMPLATE.copy()
        search_in_response_template['params']['requestId'] = request_id
        search_in_response_template['params']['query'] = query
        search_in_response_template['params']['caseSensitive'] = case_sensitive
        search_in_response_template['params']['isRegex'] = is_regex
        return search_in_response_template

    @classmethod
    def set_blocked_urls(cls, urls: list[str]):
        set_blocked_urls = cls.SET_BLOCKED_URLS.copy()
        set_blocked_urls['params']['urls'] = urls
        return set_blocked_urls
