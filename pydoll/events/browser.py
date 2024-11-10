class BrowserEvents:
    """
    A class to define the browser events available through the
    Chrome DevTools Protocol (CDP). These events allow for monitoring
    specific actions and states within the browser, such as downloads.
    """

    DOWNLOAD_PROGRESS = 'Browser.downloadProgress'
    """
    Event triggered when the download progress updates.

    This event provides details about the ongoing download,
    including the amount downloaded and the total size.
    It is part of the CDP's capabilities for monitoring
    download activities in the browser.
    """

    DOWNLOAD_WILL_BEGIN = 'Browser.downloadWillBegin'
    """
    Event triggered when a download is about to start.

    This event notifies listeners before the download begins,
    providing an opportunity to handle or react to download events.
    This is part of the CDP's support for download management
    in the browser.
    """
