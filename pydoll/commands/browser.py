class BrowserCommands:
    SCREENSHOT = {
        'method': 'Page.captureScreenshot',
        'params': {'format': 'png'},
    }
    CLOSE = {'method': 'Browser.close'}