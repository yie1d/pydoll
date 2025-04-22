class FetchEvents:
    """
    A class to define the Fetch events available through the
    Chrome DevTools Protocol (CDP). These events are related to
    the management of network requests, allowing developers to
    intercept, modify, and monitor HTTP requests and responses
    made by the browser.
    """

    AUTH_REQUIRED = 'Fetch.authRequired'
    """
    Event triggered when authentication is required for a network
    request.

    This event allows developers to respond to authentication
    challenges, enabling them to provide credentials or take
    appropriate actions when the requested resource requires
    authentication.
    """

    REQUEST_PAUSED = 'Fetch.requestPaused'
    """
    Event triggered when a network request is paused.

    This event is particularly useful for developers who want to
    analyze or modify requests before they are sent. When a request
    is paused, it gives the opportunity to inspect the request data
    or alter headers before resuming it.
    """
