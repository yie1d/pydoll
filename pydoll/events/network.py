class NetworkEvents:
    """
    A class that defines constants for various network-related events.

    These constants can be used to identify and handle network interactions in
    applications, particularly in event-driven architectures or APIs that
    monitor network activity.
    """

    DATA_RECEIVED = 'Network.dataReceived'
    """
    Event triggered when data is received over the network.

    This can include responses from HTTP requests, incoming WebSocket messages,
    or data from other network interactions. Useful for tracking incoming data
    flow.
    """

    EVENT_SOURCE_MESSAGE_RECEIVED = 'Network.eventSourceMessageReceived'
    """
    Event fired when a message is received from an EventSource.

    Typically used for server-sent events (SSE), this event indicates that a
    new message has been sent from the server to the client, enabling real-time
    updates.
    """

    LOADING_FAILED = 'Network.loadingFailed'
    """
    Event that indicates a failure in loading a network resource.

    This can occur due to various reasons, such as network errors, resource
    not found, or permission issues. This event is critical for error handling
    and debugging.
    """

    LOADING_FINISHED = 'Network.loadingFinished'
    """
    Event fired when a network loading operation is completed.

    This event is triggered regardless of whether the loading was successful
    or failed, making it useful for cleaning up or updating the user interface
    after loading operations.
    """

    REQUEST_SERVED_FROM_CACHE = 'Network.requestServedFromCache'
    """
    Event indicating that a network request was fulfilled from the cache.

    This helps identify when data is being retrieved from cache instead of
    making a new network request, which can improve performance and reduce
    latency.
    """

    REQUEST_WILL_BE_SENT = 'Network.requestWillBeSent'
    """
    Event triggered just before a network request is sent.

    This is useful for logging, modifying request headers, or performing
    actions before the actual request is made. It allows developers to
    intercept and examine requests.
    """

    RESPONSE_RECEIVED = 'Network.responseReceived'
    """
    Event that indicates a response has been received from a network request.

    This event contains details about the response, such as status codes,
    headers, and the body of the response. It's crucial for processing the
    results of network requests.
    """

    WEB_SOCKET_CLOSED = 'Network.webSocketClosed'
    """
    Event that occurs when a WebSocket connection has been closed.

    This can happen due to normal closure, errors, or network interruptions.
    Handling this event is important for managing WebSocket connections and
    reconnection logic.
    """

    WEB_SOCKET_CREATED = 'Network.webSocketCreated'
    """
    Event fired when a new WebSocket connection is established.

    This indicates that a WebSocket connection is active and ready for
    communication, allowing developers to set up message handlers or perform
    other initialization tasks.
    """

    WEB_SOCKET_FRAME_ERROR = 'Network.webSocketFrameError'
    """
    Event indicating that there was an error with a frame in a WebSocket
    communication.

    This can be used to handle specific frame-related errors and improve the
    robustness of WebSocket implementations by allowing for error logging and
    corrective actions.
    """

    WEB_SOCKET_FRAME_RECEIVED = 'Network.webSocketFrameReceived'
    """
    Event fired when a frame is received through a WebSocket.

    This is essential for processing incoming messages and performing actions
    based on the content of those messages.
    """

    WEB_SOCKET_FRAME_SENT = 'Network.webSocketFrameSent'
    """
    Event representing a frame that has been sent through a WebSocket.

    This event can be used for logging sent messages, monitoring communication,
    or performing actions after a message has been sent.
    """

    WEB_TRANSPORT_CLOSED = 'Network.webTransportClosed'
    """
    Event indicating that a web transport connection has been closed.

    Web transport connections are often used for low-latency communication.
    Handling this event is vital for ensuring that resources are properly
    released and that the application can react to disconnections.
    """

    WEB_TRANSPORT_CONNECTION_ESTABLISHED = (
        'Network.webTransportConnectionEstablished'
    )
    """
    Event fired when a web transport connection is successfully established.

    This signifies that the connection is ready for use, allowing for
    immediate data transmission and interaction.
    """

    WEB_TRANSPORT_CREATED = 'Network.webTransportCreated'
    """
    Event that signifies that a new web transport connection has been created.

    This is useful for setting up communication channels and initializing
    necessary resources for the newly created transport.
    """

    POLICY_UPDATED = 'Network.policyUpdated'
    """
    Event that indicates that the network policy has been updated.

    This might relate to security, access controls, or other network-related
    policies that affect how requests and responses are handled. It’s important
    for maintaining compliance and security in applications.
    """

    REQUEST_INTERCEPTED = 'Network.requestIntercepted'
    """
    Event fired when a network request has been intercepted.

    This is often used in service workers or other intermediary layers to
    modify or block requests before they reach the network. Handling this event
    is crucial for implementing custom request logic or caching strategies.
    """
