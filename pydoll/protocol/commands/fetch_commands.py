from copy import deepcopy
from typing import List, Optional

from pydoll.constants import (
    AuthChallengeResponseValues,
    NetworkErrorReason,
    RequestMethod,
    RequestStage,
    ResourceType,
)
from pydoll.protocol.types.commands import (
    AuthChallengeResponseDict,
    Command,
    ContinueRequestParams,
    ContinueResponseParams,
    ContinueWithAuthParams,
    EnableParams,
    FailRequestParams,
    FulfillRequestParams,
    GetResponseBodyParams,
    HeaderEntry,
    RequestPattern,
    TakeResponseBodyAsStreamParams,
)
from pydoll.protocol.types.responses import (
    GetResponseBodyResponse,
    Response,
    TakeResponseBodyAsStreamResponse,
)


class FetchCommands:
    """
    A collection of command templates for handling fetch events in the browser.

    This class provides a structured way to create and manage commands related
    to fetch operations intercepted by the Fetch API. Each command corresponds
    to specific actions that can be performed on fetch requests, such as
    continuing a fetch request, fulfilling a fetch response, or handling
    authentication challenges.

    Attributes:
        CONTINUE_REQUEST (Command): Template for continuing an intercepted fetch
            request.
        CONTINUE_REQUEST_WITH_AUTH (Command): Template for continuing a fetch
            request that requires authentication.
        DISABLE (Command): Template for disabling fetch interception.
        ENABLE (Command): Template for enabling fetch interception.
        FAIL_REQUEST (Command): Template for simulating a failure in a fetch
            request.
        FULFILL_REQUEST (Command): Template for fulfilling a fetch request with
            custom responses.
        GET_RESPONSE_BODY (Command): Template for retrieving the response body of
            a fetch request.
        CONTINUE_RESPONSE (Command): Template for continuing a fetch response for
            an intercepted request.
        TAKE_RESPONSE_BODY_AS_STREAM (Command): Template for taking response body
            as a stream.
    """

    CONTINUE_REQUEST = Command(method='Fetch.continueRequest')
    CONTINUE_REQUEST_WITH_AUTH = Command(method='Fetch.continueWithAuth')
    DISABLE = Command(method='Fetch.disable')
    ENABLE = Command(method='Fetch.enable')
    FAIL_REQUEST = Command(method='Fetch.failRequest')
    FULFILL_REQUEST = Command(method='Fetch.fulfillRequest')
    GET_RESPONSE_BODY = Command(method='Fetch.getResponseBody')
    CONTINUE_RESPONSE = Command(method='Fetch.continueResponse')
    TAKE_RESPONSE_BODY_AS_STREAM = Command(
        method='Fetch.takeResponseBodyAsStream'
    )

    @classmethod
    def continue_request(  # noqa: PLR0913, PLR0917
        cls,
        request_id: str,
        url: Optional[str] = None,
        method: Optional[RequestMethod] = None,
        post_data: Optional[dict] = None,
        headers: Optional[List[HeaderEntry]] = None,
        intercept_response: Optional[bool] = None,
    ) -> Command[Response]:
        """
        Creates a command to continue a paused fetch request.

        This command allows the browser to resume a fetch operation that has
        been intercepted. You can modify the fetch request URL, method,
        headers, and body before continuing.

        Args:
            request_id (str): The ID of the fetch request to continue.
            url (Optional[str]): The new URL for the fetch request. Defaults to None.
            method (Optional[RequestMethod]): The HTTP method to use (e.g., 'GET',
                'POST'). Defaults to None.
            post_data (Optional[dict]): The body data to send with the fetch
                request. Defaults to None.
            headers (Optional[List[HeaderEntry]]): A list of HTTP headers to include
              in the fetch request. Defaults to None.
            intercept_response (Optional[bool]): Indicates if the response
              should be intercepted. Defaults to None.

        Returns:
            Command[Response]: A command for continuing the fetch request.
        """
        continue_request_template = deepcopy(cls.CONTINUE_REQUEST)
        params = ContinueRequestParams(requestId=request_id)
        if url:
            params['url'] = url
        if method:
            params['method'] = method
        if post_data:
            params['postData'] = post_data
        if headers:
            params['headers'] = headers
        if intercept_response:
            params['interceptResponse'] = intercept_response
        continue_request_template['params'] = params
        return continue_request_template

    @classmethod
    def continue_request_with_auth(
        cls,
        request_id: str,
        auth_challenge_response: AuthChallengeResponseValues,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
    ) -> Command[Response]:
        """
        Creates a command to continue a paused fetch request with
        authentication.

        This command is used when the fetch operation requires authentication.
        It provides the necessary credentials to continue the request.

        Args:
            request_id (str): The ID of the fetch request to continue.
            auth_challenge_response (AuthChallengeResponseValues): The authentication
                challenge response type.
            proxy_username (Optional[str]): The username for proxy authentication.
                Defaults to None.
            proxy_password (Optional[str]): The password for proxy authentication.
                Defaults to None.

        Returns:
            Command[Response]: A command for continuing the fetch request with
                authentication.
        """
        continue_request_with_auth_template = deepcopy(
            cls.CONTINUE_REQUEST_WITH_AUTH
        )
        auth_challenge_response_dict = AuthChallengeResponseDict(
            response=auth_challenge_response
        )
        if proxy_username:
            auth_challenge_response_dict['username'] = proxy_username
        if proxy_password:
            auth_challenge_response_dict['password'] = proxy_password

        params = ContinueWithAuthParams(
            requestId=request_id,
            authChallengeResponse=auth_challenge_response_dict,
        )
        continue_request_with_auth_template['params'] = params
        return continue_request_with_auth_template

    @classmethod
    def disable_fetch_events(cls) -> Command[Response]:
        """
        Creates a command to disable fetch interception.

        This command stops the browser from intercepting fetch requests.

        Returns:
            Command[Response]: A command for disabling fetch interception.
        """
        return cls.DISABLE

    @classmethod
    def enable_fetch_events(
        cls,
        handle_auth_requests: bool,
        url_pattern: str = '*',
        resource_type: Optional[ResourceType] = None,
        request_stage: Optional[RequestStage] = None,
    ) -> Command[Response]:
        """
        Creates a command to enable fetch interception.

        This command allows the browser to start intercepting fetch requests.
        You can specify whether to handle authentication challenges and the
        types of resources to intercept.

        Args:
            handle_auth_requests (bool): Indicates if authentication requests
                should be handled.
            url_pattern (str): Pattern to match URLs for interception. Defaults to '*'.
            resource_type (Optional[ResourceType]): The type of resource to intercept.
                Defaults to None.
            request_stage (Optional[RequestStage]): The stage of the request to intercept.
                Defaults to None.

        Returns:
            Command[Response]: A command for enabling fetch interception.
        """
        enable_fetch_events_template = deepcopy(cls.ENABLE)
        request_pattern = RequestPattern(urlPattern=url_pattern)
        if resource_type:
            request_pattern['resourceType'] = resource_type
        if request_stage:
            request_pattern['requestStage'] = request_stage

        params = EnableParams(
            patterns=[request_pattern], handleAuthRequests=handle_auth_requests
        )
        enable_fetch_events_template['params'] = params
        return enable_fetch_events_template

    @classmethod
    def fail_request(
        cls, request_id: str, error_reason: NetworkErrorReason
    ) -> Command[Response]:
        """
        Creates a command to simulate a failure in a fetch request.

        This command allows you to simulate a failure for a specific fetch
        operation, providing a reason for the failure.

        Args:
            request_id (str): The ID of the fetch request to fail.
            error_reason (NetworkErrorReason): The reason for the failure.

        Returns:
            Command[Response]: A command for failing the fetch request.
        """
        fail_request_template = deepcopy(cls.FAIL_REQUEST)
        params = FailRequestParams(
            requestId=request_id, errorReason=error_reason
        )
        fail_request_template['params'] = params
        return fail_request_template

    @classmethod
    def fulfill_request(  # noqa: PLR0913, PLR0917
        cls,
        request_id: str,
        response_code: int,
        response_headers: Optional[List[HeaderEntry]] = None,
        body: Optional[dict] = None,
        response_phrase: Optional[str] = None,
    ) -> Command[Response]:
        """
        Creates a command to fulfill a fetch request with a custom response.

        This command allows you to provide a custom response for a fetch
        operation, including the HTTP status code, headers, and body content.

        Args:
            request_id (str): The ID of the fetch request to fulfill.
            response_code (int): The HTTP status code to return.
            response_headers (Optional[List[HeaderEntry]]): A list of response headers.
                Defaults to None.
            body (Optional[dict]): The body content of the response. Defaults to None.
            response_phrase (Optional[str]): The response phrase (e.g., 'OK',
                'Not Found'). Defaults to None.

        Returns:
            Command[Response]: A command for fulfilling the fetch request.
        """
        fulfill_request_template = deepcopy(cls.FULFILL_REQUEST)
        params = FulfillRequestParams(
            requestId=request_id,
            responseCode=response_code,
        )
        if response_headers:
            params['responseHeaders'] = response_headers
        if body:
            params['body'] = body
        if response_phrase:
            params['responsePhrase'] = response_phrase
        fulfill_request_template['params'] = params
        return fulfill_request_template

    @classmethod
    def get_response_body(
        cls, request_id: str
    ) -> Command[GetResponseBodyResponse]:
        """
        Creates a command to retrieve the response body of a fetch request.

        This command allows you to access the body of a completed fetch
        operation, which can be useful for analyzing the response data.

        Args:
            request_id (str): The ID of the fetch request to retrieve the body
                from.

        Returns:
            Command[GetResponseBodyResponse]: A command for getting the response body.
        """
        get_response_body_template = deepcopy(cls.GET_RESPONSE_BODY)
        params = GetResponseBodyParams(requestId=request_id)
        get_response_body_template['params'] = params
        return get_response_body_template

    @classmethod
    def continue_response(
        cls,
        request_id: str,
        response_code: Optional[int] = None,
        response_headers: Optional[List[HeaderEntry]] = None,
        response_phrase: Optional[str] = None,
    ) -> Command[Response]:
        """
        Creates a command to continue a fetch response for an intercepted
        request.

        This command allows the browser to continue the response flow for a
        specific fetch request, including customizing the HTTP status code,
        headers, and response phrase.

        Args:
            request_id (str): The ID of the fetch request to continue the
                response for.
            response_code (Optional[int]): The HTTP status code to send.
                Defaults to None.
            response_headers (Optional[List[HeaderEntry]]): A list of response headers.
                Defaults to None.
            response_phrase (Optional[str]): The response phrase (e.g., 'OK').
                Defaults to None.

        Returns:
            Command[Response]: A command for continuing the fetch response.
        """
        continue_response_template = deepcopy(cls.CONTINUE_RESPONSE)

        params = ContinueResponseParams(requestId=request_id)
        if response_code:
            params['responseCode'] = response_code
        if response_headers:
            params['responseHeaders'] = response_headers
        if response_phrase:
            params['responsePhrase'] = response_phrase
        continue_response_template['params'] = params
        return continue_response_template

    @classmethod
    def take_response_body_as_stream(
        cls, request_id: str
    ) -> Command[TakeResponseBodyAsStreamResponse]:
        """
        Creates a command to take the response body as a stream.

        This command allows you to receive the response body as a stream
        which can be useful for handling large responses.

        Args:
            request_id (str): The ID of the fetch request to take the response
                body stream from.

        Returns:
            Command[TakeResponseBodyAsStreamResponse]: A command for taking the response
                body as a stream.
        """
        take_response_body_as_stream_template = deepcopy(
            cls.TAKE_RESPONSE_BODY_AS_STREAM
        )
        params = TakeResponseBodyAsStreamParams(requestId=request_id)
        take_response_body_as_stream_template['params'] = params
        return take_response_body_as_stream_template
