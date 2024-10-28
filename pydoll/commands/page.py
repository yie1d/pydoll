class PageCommands:
    SCREENSHOT_TEMPLATE = {
        'method': 'Page.captureScreenshot',
        'params': {},
    }
    GO_TO_TEMPLATE = {'method': 'Page.navigate', 'params': {}}
    REFRESH_TEMPLATE = {'method': 'Page.reload', 'params': {}}
    PRINT_TO_PDF_TEMPLATE = {'method': 'Page.printToPDF', 'params': {}}
    ENABLE_PAGE = {'method': 'Page.enable'}

    @classmethod
    def screenshot(cls, format: str = 'png', quality: int = 100) -> dict:
        """
        Generates the command to capture a screenshot of the current page.

        Args:
            format (str): The format of the image to be captured.
            quality (int): The quality of the image to be captured.

        Returns:
            dict: The command to be sent to the browser.
        """
        command = cls.SCREENSHOT_TEMPLATE.copy()
        command['params']['format'] = format
        command['params']['quality'] = quality
        return command

    @classmethod
    def go_to(cls, url: str) -> dict:
        """
        Generates the command to navigate to a specific URL.

        Args:
            url (str): The URL to navigate to.

        Returns:
            dict: The command to be sent to the browser.
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

        Returns:
            dict: The command to be sent to the browser.
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
            scale (int): The scale of the page to print.
            paper_width (float): The width of the paper to print on.
            paper_height (float): The height of the paper to print on.

        Returns:
            dict: The command to be sent to the browser.
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
            dict: The command to be sent to the browser.
        """
        return cls.ENABLE_PAGE
