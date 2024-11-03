class FetchCommands:
    CONTINUE_REQUEST = {'method': 'Fetch.continueRequest', 'params': {}}
    CONTINUE_REQUEST_WITH_AUTH = {
        'method': 'Fetch.continueWithAuth',
        'params': {},
    }
    DISABLE = {'method': 'Fetch.disable', 'params': {}}
    ENABLE = {'method': 'Fetch.enable', 'params': {}}
    FAIL_REQUEST = {'method': 'Fetch.failRequest', 'params': {}}
    FULFILL_REQUEST = {'method': 'Fetch.fulfillRequest', 'params': {}}
    GET_RESPONSE_BODY = {'method': 'Fetch.getResponseBody', 'params': {}}
    CONTINUE_RESPONSE = {'method': 'Fetch.continueResponse', 'params': {}}

    @classmethod
    def continue_request(
        cls,
        request_id: str,
        url: str = '',
        method: str = '',
        postData: str = '',
        headers: dict = {},
        interceptResponse: bool = False,
    ):
        continue_request_template = cls.CONTINUE_REQUEST.copy()
        continue_request_template['params']['requestId'] = request_id
        if url:
            continue_request_template['params']['url'] = url
        if method:
            continue_request_template['params']['method'] = method
        if postData:
            continue_request_template['params']['postData'] = postData
        if headers:
            continue_request_template['params']['headers'] = headers
        if interceptResponse:
            continue_request_template['params']['interceptResponse'] = (
                interceptResponse
            )
        return continue_request_template

    @classmethod
    def continue_request_with_auth(
        cls, request_id: str, proxy_username: str, proxy_password: str
    ):
        continue_request_with_auth_template = (
            cls.CONTINUE_REQUEST_WITH_AUTH.copy()
        )
        continue_request_with_auth_template['params']['requestId'] = request_id
        continue_request_with_auth_template['params'][
            'authChallengeResponse'
        ] = {
            'response': 'ProvideCredentials',
            'username': proxy_username,
            'password': proxy_password,
        }
        return continue_request_with_auth_template

    @classmethod
    def disable_fetch_events(cls):
        return cls.DISABLE

    @classmethod
    def enable_fetch_events(cls, handle_auth_requests: bool):
        enable_fetch_events_template = cls.ENABLE.copy()
        enable_fetch_events_template['params']['patterns'] = [
            {'urlPattern': '*', 'resourceType': 'Document'}
        ]
        enable_fetch_events_template['params']['handleAuthRequests'] = (
            handle_auth_requests
        )
        return enable_fetch_events_template

    @classmethod
    def fail_request(cls, request_id: str, errorReason: str):
        fail_request_template = cls.FAIL_REQUEST.copy()
        fail_request_template['params']['requestId'] = request_id
        fail_request_template['params']['errorReason'] = errorReason
        return fail_request_template

    @classmethod
    def fulfill_request(
        cls,
        request_id: str,
        responseCode: int,
        responseHeaders: dict = {},
        binaryResponseHeaders: str = '',
        body: str = '',
        responsePhrase: str = '',
    ):
        fulfill_request_template = cls.FULFILL_REQUEST.copy()
        fulfill_request_template['params']['requestId'] = request_id
        if responseCode:
            fulfill_request_template['params']['responseCode'] = responseCode
        if responseHeaders:
            fulfill_request_template['params']['responseHeaders'] = (
                responseHeaders
            )
        if binaryResponseHeaders:
            fulfill_request_template['params']['binaryResponseHeaders'] = (
                binaryResponseHeaders
            )
        if body:
            fulfill_request_template['params']['body'] = body
        if responsePhrase:
            fulfill_request_template['params']['responsePhrase'] = (
                responsePhrase
            )
        return fulfill_request_template

    @classmethod
    def get_response_body(cls, request_id: str):
        get_response_body_template = cls.GET_RESPONSE_BODY.copy()
        get_response_body_template['params']['requestId'] = request_id
        return get_response_body_template

    @classmethod
    def continue_response(
        cls,
        requestId: str,
        responseCode: int = '',
        responseHeaders: dict = {},
        binaryResponseHeaders: str = '',
        responsePhrase: str = '',
    ):
        continue_response_template = cls.CONTINUE_RESPONSE.copy()
        continue_response_template['params']['requestId'] = requestId
        if responseCode:
            continue_response_template['params']['responseCode'] = responseCode
        if responseHeaders:
            continue_response_template['params']['responseHeaders'] = (
                responseHeaders
            )
        if binaryResponseHeaders:
            continue_response_template['params']['binaryResponseHeaders'] = (
                binaryResponseHeaders
            )
        if responsePhrase:
            continue_response_template['params']['responsePhrase'] = (
                responsePhrase
            )
        return continue_response_template
