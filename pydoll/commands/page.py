class PageCommands:
    """
    PageCommands class provides a set of commands to interact with the
    Page domain of the Chrome DevTools Protocol (CDP). These commands enable
    users to perform operations related to web pages, such as capturing
    screenshots, navigating to URLs, refreshing pages, printing to PDF,
    and enabling the Page domain.

    The following operations can be performed:
    - Capture a screenshot of the current page.
    - Navigate to a specified URL.
    - Refresh the current page, with an option to ignore the cache.
    - Print the current page to a PDF document.
    - Enable the Page domain for further interactions.

    Each method generates a command that can be sent to the browser as part of
    the DevTools Protocol communication.
    """

    SCREENSHOT_TEMPLATE = {
        'method': 'Page.captureScreenshot',
        'params': {},
    }
    GO_TO_TEMPLATE = {'method': 'Page.navigate', 'params': {}}
    REFRESH_TEMPLATE = {'method': 'Page.reload', 'params': {}}
    PRINT_TO_PDF_TEMPLATE = {'method': 'Page.printToPDF', 'params': {}}
    ENABLE_PAGE = {'method': 'Page.enable'}
    DISABLE_PAGE = {'method': 'Page.disable'}
    SET_DOWNLOAD_BEHAVIOR = {
        'method': 'Page.setDownloadBehavior',
        'params': {},
    }
    HANDLE_DIALOG = {'method': 'Page.handleJavaScriptDialog', 'params': {}}
    CLOSE = {'method': 'Page.close'}

    @classmethod
    def handle_dialog(cls, accept: bool = True) -> dict:
        """
        Generates the command to handle a JavaScript dialog.

        Args:
            accept (bool): Whether to accept the dialog.
                           If True, the dialog will be accepted.
                           If False, the dialog will be dismissed.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method and parameters for handling the dialog.
        """
        command = cls.HANDLE_DIALOG.copy()
        command['params']['accept'] = accept
        return command

    @classmethod
    def set_download_path(cls, path: str) -> dict:
        """
        Generates the command to set the download path for the browser.

        Args:
            path (str): The path where the downloaded files should be saved.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method and parameters for setting
                  the download path.
        """
        command = cls.SET_DOWNLOAD_BEHAVIOR.copy()
        command['params']['behavior'] = 'allow'
        command['params']['downloadPath'] = path
        return command

    @classmethod
    def screenshot(
        cls, fmt: str = 'jpeg', quality: int = 100, clip: dict = None
    ) -> dict:
        """
        Generates the command to capture a screenshot of the current page.

        Args:
            fmt (str): The format of the image to be captured.
                          Can be 'png' or 'jpeg'.
            quality (int): The quality of the image to be captured,
                           applicable only if the format is 'jpeg'.
                           Value should be between 0 (lowest quality)
                           and 100 (highest quality).

        Returns:
            dict: The command to be sent to the browser,
                  containing the method and parameters for the screenshot.
        """
        command = cls.SCREENSHOT_TEMPLATE.copy()
        command['params']['format'] = fmt
        command['params']['quality'] = quality
        if clip:
            command['params']['clip'] = clip
        return command

    @classmethod
    def go_to(cls, url: str) -> dict:
        """
        Generates the command to navigate to a specific URL.

        Args:
            url (str): The URL to navigate to. It should be a valid URL format.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method and parameters for navigation.
        """
        command = cls.GO_TO_TEMPLATE.copy()
        command['params']['url'] = url
        return command

    @classmethod
    def refresh(cls, ignore_cache: bool = False) -> dict:
        """
        Generates the command to refresh the current page.

        Args:
            ignore_cache (bool): Whether to ignore the cache when refreshing.
                                 If True, the cached resources will not be
                                 used.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method and parameters for page refresh.
        """
        command = cls.REFRESH_TEMPLATE.copy()
        command['params']['ignoreCache'] = ignore_cache
        return command

    @classmethod
    def print_to_pdf(
        cls, scale: int = 1, paper_width: float = 8.5, paper_height: float = 11
    ) -> dict:
        """
        Generates the command to print the current page to a PDF.

        Args:
            scale (int): The scale of the page to print. Default is 1 (100%).
            paper_width (float): The width of the paper to print on, in inches.
                Default is 8.5 inches.
            paper_height (float): The height of the paper to print on,
                in inches. Default is 11 inches.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method and parameters for printing to PDF.
        """
        command = cls.PRINT_TO_PDF_TEMPLATE.copy()
        command['params']['scale'] = scale
        command['params']['paperWidth'] = paper_width
        command['params']['paperHeight'] = paper_height
        return command

    @classmethod
    def enable_page(cls) -> dict:
        """
        Generates the command to enable the Page domain.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method to enable the Page domain.
        """
        return cls.ENABLE_PAGE

    @classmethod
    def disable_page(cls) -> dict:
        """
        Generates the command to disable the Page domain.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method to disable the Page domain.
        """
        return cls.DISABLE_PAGE

    @classmethod
    def close(cls) -> dict:
        """
        Generates the command to close the current page.

        Returns:
            dict: The command to be sent to the browser,
                  containing the method to close the current page.
        """
        return cls.CLOSE
