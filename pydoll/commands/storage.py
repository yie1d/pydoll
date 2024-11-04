class StorageCommands:
    CLEAR_COOKIES = {'method': 'Storage.clearCookies', 'params': {}}
    SET_COOKIES = {'method': 'Storage.setCookies', 'params': {}}
    GET_COOKIES = {'method': 'Storage.getCookies', 'params': {}}

    @classmethod
    def clear_cookies(cls) -> dict:
        return cls.CLEAR_COOKIES

    @classmethod
    def set_cookies(cls, cookies: list) -> dict:
        set_cookies = cls.SET_COOKIES.copy()
        set_cookies['params']['cookies'] = cookies
        return set_cookies

    @classmethod
    def get_cookies(cls) -> dict:
        return cls.GET_COOKIES
