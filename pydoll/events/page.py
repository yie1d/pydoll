class PageEvents:
    """
    A class that defines constants for various page-related events.

    These constants represent significant events in the lifecycle of a web
    page, particularly in the context of web automation, testing,
    or monitoring.
    """

    PAGE_LOADED = 'Page.loadEventFired'
    """
    Event triggered when the page has fully loaded.

    This includes the loading of all resources, such as images and stylesheets.
    It is typically used to perform actions that require the entire page to be
    ready for interaction or manipulation.
    """

    DOM_CONTENT_LOADED = 'Page.domContentEventFired'
    """
    Event fired when the DOMContentLoaded event is fired.

    This event indicates that the initial HTML document has been completely
    loaded and parsed, which allows for immediate manipulation of the DOM
    before external resources like images are fully loaded.
    """

    FILE_CHOOSER_OPENED = 'Page.fileChooserOpened'
    """
    Event indicating that a file chooser dialog has been opened.

    This event is crucial for applications that require user interaction for
    file uploads, allowing for tracking when a user is prompted to select
    files.
    """

    FRAME_ATTACHED = 'Page.frameAttached'
    """
    Event that occurs when a frame is attached to the page.

    This event is significant in scenarios involving iframes or nested browsing
    contexts, enabling developers to manage and interact with newly added
    frames.
    """

    FRAME_DETACHED = 'Page.frameDetached'
    """
    Event triggered when a frame is detached from the page.

    This can happen when iframes are removed or navigated away, and it’s
    important for cleanup and managing resources associated with those frames.
    """

    FRAME_NAVIGATED = 'Page.frameNavigated'
    """
    Event that indicates a frame has been navigated to a new URL.

    This is essential for tracking navigation within iframes, allowing for
    updates to the application state or user interface based on the content
    of the frame.
    """

    JS_DIALOG_CLOSED = 'Page.javascriptDialogClosed'
    """
    Event fired when a JavaScript dialog (such as an alert or confirmation)
    is closed.

    This is useful for managing user interactions with dialogs, allowing for
    actions to be taken after a dialog has been dismissed.
    """

    JS_DIALOG_OPENING = 'Page.javascriptDialogOpening'
    """
    Event triggered when a JavaScript dialog is about to open.

    This event can be used to intervene in the opening of the dialog, such as
    providing automated responses or logging dialog interactions.
    """

    LIFECYCLE_EVENT = 'Page.lifecycleEvent'
    """
    Event representing a generic lifecycle event for the page.

    This event is a catch-all for various lifecycle-related events and can be
    used for monitoring changes in the page state throughout its lifetime.
    """

    WINDOW_OPENED = 'Page.windowOpen'
    """
    Event that indicates a new window has been opened.

    This is useful for applications that need to monitor or manage multiple
    windows and their interactions, particularly in the context of pop-ups
    or new tabs.
    """

    DOCUMENT_OPENED = 'Page.documentOpened'
    """
    Event that signifies a new document has been opened in the page.

    This event is important for tracking changes in the document context,
    particularly in environments where documents can be dynamically created
    or loaded.
    """

    FRAME_STARTED_LOADING = 'Page.frameStartedLoading'
    """
    Event triggered when a frame starts loading content.

    This event is useful for tracking the loading state of frames,
    enabling developers to manage loading indicators or perform actions when
    frames begin loading resources.
    """

    FRAME_STOPPED_LOADING = 'Page.frameStoppedLoading'
    """
    Event that indicates a frame has stopped loading content.

    This can signify that a frame has successfully loaded or encountered an
    error, allowing for appropriate handling of frame loading states.
    """

    DOWNLOAD_PROGRESS = 'Page.downloadProgress'
    """
    Event fired to indicate progress on a download operation.

    This event provides updates on the download status, enabling the
    application to inform users about ongoing downloads and their completion.
    """

    DOWNLOAD_WILL_BEGIN = 'Page.downloadWillBegin'
    """
    Event that occurs when a download is about to start.

    This event is significant for tracking the initiation of downloads,
    allowing for pre-download actions such as logging or user notifications.
    """
    NAVIGATED_WITHIN_DOCUMENT = 'Page.navigatedWithinDocument'
    """
    Event that indicates navigation within the same document.

    This event is useful for tracking changes in the document state, such as
    anchor links or in-page navigation, without requiring a full page reload.
    """

    ALL_EVENTS = [
        PAGE_LOADED,
        DOM_CONTENT_LOADED,
        FILE_CHOOSER_OPENED,
        FRAME_ATTACHED,
        FRAME_DETACHED,
        FRAME_NAVIGATED,
        JS_DIALOG_CLOSED,
        JS_DIALOG_OPENING,
        LIFECYCLE_EVENT,
        WINDOW_OPENED,
        DOCUMENT_OPENED,
        FRAME_STARTED_LOADING,
        FRAME_STOPPED_LOADING,
        DOWNLOAD_PROGRESS,
        DOWNLOAD_WILL_BEGIN,
        NAVIGATED_WITHIN_DOCUMENT,
    ]
