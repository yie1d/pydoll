class ConnectionFailed(Exception):
    pass


class InvalidCommand(Exception):
    pass


class InvalidCallback(Exception):
    pass


class NetworkError(Exception):
    pass


class InvalidResponse(Exception):
    pass


class ReconnectionFailed(Exception):
    pass


class ResendCommandFailed(Exception):
    pass


class BrowserNotRunning(Exception):
    pass


class ElementNotFound(Exception):
    pass


class ClickIntercepted(Exception):
    pass


class ElementNotVisible(Exception):
    pass


class ElementNotInteractable(Exception):
    pass
