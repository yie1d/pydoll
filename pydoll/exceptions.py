class ConnectionFailed(Exception):
    message = 'Failed to connect to the browser'

    def __str__(self):
        return self.message


class InvalidCommand(Exception):
    message = 'The command provided is invalid'

    def __str__(self):
        return self.message


class InvalidCallback(Exception):
    message = 'The callback provided is invalid'

    def __str__(self):
        return self.message


class NetworkError(Exception):
    message = 'A network error occurred'

    def __str__(self):
        return self.message


class InvalidResponse(Exception):
    message = 'The response received is invalid'

    def __str__(self):
        return self.message


class ReconnectionFailed(Exception):
    message = 'Failed to reconnect to the browser'

    def __str__(self):
        return self.message


class ResendCommandFailed(Exception):
    message = 'Failed to resend the command'

    def __str__(self):
        return self.message


class BrowserNotRunning(Exception):
    message = 'The browser is not running'

    def __str__(self):
        return self.message


class ElementNotFound(Exception):
    message = 'The specified element was not found'

    def __str__(self):
        return self.message


class ClickIntercepted(Exception):
    message = 'The click was intercepted'

    def __str__(self):
        return self.message


class ElementNotVisible(Exception):
    message = 'The element is not visible'

    def __str__(self):
        return self.message


class ElementNotInteractable(Exception):
    message = 'The element is not interactable'

    def __str__(self):
        return self.message


class InvalidFileExtension(Exception):
    message = 'The file extension provided is not supported'

    def __str__(self):
        return self.message


class EventNotSupported(Exception):
    message = 'The event is not supported'

    def __init__(self, message: str = ''):
        self.message = message or self.message

    def __str__(self):
        return self.message
