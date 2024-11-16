class FetchCommands:
    """
    A collection of command templates for handling fetch events in the browser.

    This class provides a structured way to create and manage commands related
    to fetch operations intercepted by the Fetch API. Each command corresponds
    to specific actions that can be performed on fetch requests, such as
    continuing a fetch request, fulfilling a fetch response, or handling
    authentication challenges.

    Attributes:
        CONTINUE_REQUEST (dict): Template for continuing an intercepted fetch
            request.
        CONTINUE_REQUEST_WITH_AUTH (dict): Template for continuing a fetch
            request that requires authentication.
        DISABLE (dict): Template for disabling fetch interception.
        ENABLE (dict): Template for enabling fetch interception.
        FAIL_REQUEST (dict): Template for simulating a failure in a fetch
            request.
        FULFILL_REQUEST (dict): Template for fulfilling a fetch request with
            custom responses.
        GET_RESPONSE_BODY (dict): Template for retrieving the response body of
            a fetch request.
        CONTINUE_RESPONSE (dict): Template for continuing a fetch response for
            an intercepted request.
    """

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
    def continue_request(  # noqa: PLR0913, PLR0917
        cls,
        request_id: str,
        url: str = '',
        method: str = '',
        post_data: str = '',
        headers: dict = {},
        intercept_response: bool = False,
    ):
        """
        Creates a command to continue a paused fetch request.

        This command allows the browser to resume a fetch operation that has
        been intercepted. You can modify the fetch request URL, method,
        headers, and body before continuing.

        Args:
            request_id (str): The ID of the fetch request to continue.
            url (str, optional): The new URL for the fetch request. Defaults to
                ''.
            method (str, optional): The HTTP method to use (e.g., 'GET',
                'POST'). Defaults to ''.
            postData (str, optional): The body data to send with the fetch
                request. Defaults to ''.
            headers (dict, optional): A dictionary of HTTP headers to include
              in the fetch request. Defaults to {}.
            interceptResponse (bool, optional): Indicates if the response
              should be intercepted. Defaults to False.

        Returns:
            dict: A command template for continuing the fetch request.
        """
        continue_request_template = cls.CONTINUE_REQUEST.copy()
        continue_request_template['params']['requestId'] = request_id
        if url:
            continue_request_template['params']['url'] = url
        if method:
            continue_request_template['params']['method'] = method
        if post_data:
            continue_request_template['params']['postData'] = post_data
        if headers:
            continue_request_template['params']['headers'] = headers
        if intercept_response:
            continue_request_template['params']['interceptResponse'] = (
                intercept_response
            )
        return continue_request_template

    @classmethod
    def continue_request_with_auth(
        cls, request_id: str, proxy_username: str, proxy_password: str
    ):
        """
        Creates a command to continue a paused fetch request with
        authentication.

        This command is used when the fetch operation requires authentication.
        It provides the necessary credentials to continue the request.

        Args:
            request_id (str): The ID of the fetch request to continue.
            proxy_username (str): The username for proxy authentication.
            proxy_password (str): The password for proxy authentication.

        Returns:
            dict: A command template for continuing the fetch request with
                authentication.
        """
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
        """
        Creates a command to disable fetch interception.

        This command stops the browser from intercepting fetch requests.

        Returns:
            dict: A command template for disabling fetch interception.
        """
        return cls.DISABLE

    @classmethod
    def enable_fetch_events(
        cls, handle_auth_requests: bool, resource_type: str
    ):
        """
        Creates a command to enable fetch interception.

        This command allows the browser to start intercepting fetch requests.
        You can specify whether to handle authentication challenges and the
        types of resources to intercept.

        Args:
            handle_auth_requests (bool): Indicates if authentication requests
                should be handled.
            resource_type (str): The type of resource to intercept (e.g.,
                'Document', 'Image').

        Returns:
            dict: A command template for enabling fetch interception.
        """
        enable_fetch_events_template = cls.ENABLE.copy()
        enable_fetch_events_template['params']['patterns'] = [
            {'urlPattern': '*'}
        ]
        if resource_type:
            enable_fetch_events_template['params']['patterns'][0][
                'resourceType'
            ] = resource_type

        enable_fetch_events_template['params']['handleAuthRequests'] = (
            handle_auth_requests
        )
        return enable_fetch_events_template

    @classmethod
    def fail_request(cls, request_id: str, error_reason: str):
        """
        Creates a command to simulate a failure in a fetch request.

        This command allows you to simulate a failure for a specific fetch
        operation, providing a reason for the failure.

        Args:
            request_id (str): The ID of the fetch request to fail.
            errorReason (str): A description of the failure reason.

        Returns:
            dict: A command template for failing the fetch request.
        """
        fail_request_template = cls.FAIL_REQUEST.copy()
        fail_request_template['params']['requestId'] = request_id
        fail_request_template['params']['errorReason'] = error_reason
        return fail_request_template

    @classmethod
    def fulfill_request(  # noqa: PLR0913, PLR0917
        cls,
        request_id: str,
        response_code: int,
        response_headers: dict = {},
        binary_response_headers: str = '',
        body: str = '',
        response_phrase: str = '',
    ):
        """
        Creates a command to fulfill a fetch request with a custom response.

        This command allows you to provide a custom response for a fetch
        operation, including the HTTP status code, headers, and body content.

        Args:
            request_id (str): The ID of the fetch request to fulfill.
            responseCode (int): The HTTP status code to return.
            responseHeaders (dict, optional): A dictionary of response headers.
                Defaults to {}.
            binaryResponseHeaders (str, optional): Binary response headers.
                Defaults to ''.
            body (str, optional): The body content of the response. Defaults to
                ''.
            responsePhrase (str, optional): The response phrase (e.g., 'OK',
                'Not Found'). Defaults to ''.

        Returns:
            dict: A command template for fulfilling the fetch request.
        """
        fulfill_request_template = cls.FULFILL_REQUEST.copy()
        fulfill_request_template['params']['requestId'] = request_id
        if response_code:
            fulfill_request_template['params']['responseCode'] = response_code
        if response_headers:
            fulfill_request_template['params']['responseHeaders'] = (
                response_headers
            )
        if binary_response_headers:
            fulfill_request_template['params']['binaryResponseHeaders'] = (
                binary_response_headers
            )
        if body:
            fulfill_request_template['params']['body'] = body
        if response_phrase:
            fulfill_request_template['params']['responsePhrase'] = (
                response_phrase
            )
        return fulfill_request_template

    @classmethod
    def get_response_body(cls, request_id: str):
        """
        Creates a command to retrieve the response body of a fetch request.

        This command allows you to access the body of a completed fetch
        operation, which can be useful for analyzing the response data.

        Args:
            request_id (str): The ID of the fetch request to retrieve the body
                from.

        Returns:
            dict: A command template for getting the response body.
        """
        get_response_body_template = cls.GET_RESPONSE_BODY.copy()
        get_response_body_template['params']['requestId'] = request_id
        return get_response_body_template

    @classmethod
    def continue_response(
        cls,
        request_id: str,
        response_code: int = '',
        response_headers: dict = {},
        binary_response_headers: str = '',
        response_phrase: str = '',
    ):
        """
        Creates a command to continue a fetch response for an intercepted
        request.

        This command allows the browser to continue the response flow for a
        specific fetch request, including customizing the HTTP status code,
        headers, and response phrase.

        Args:
            requestId (str): The ID of the fetch request to continue the
                response for.
            responseCode (int, optional): The HTTP status code to send.
                Defaults to ''.
            responseHeaders (dict, optional): A dictionary of response headers.
                Defaults to {}.
            binaryResponseHeaders (str, optional): Binary response headers.
                Defaults to ''.
            responsePhrase (str, optional): The response phrase (e.g., 'OK').
                Defaults to ''.

        Returns:
            dict: A command template for continuing the fetch response.
        """
        continue_response_template = cls.CONTINUE_RESPONSE.copy()
        continue_response_template['params']['requestId'] = request_id
        if response_code:
            continue_response_template['params']['responseCode'] = (
                response_code
            )
        if response_headers:
            continue_response_template['params']['responseHeaders'] = (
                response_headers
            )
        if binary_response_headers:
            continue_response_template['params']['binaryResponseHeaders'] = (
                binary_response_headers
            )
        if response_phrase:
            continue_response_template['params']['responsePhrase'] = (
                response_phrase
            )
        return continue_response_template
