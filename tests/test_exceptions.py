import pytest
from pydoll.exceptions import (
    ConnectionFailed,
    InvalidCommand,
    InvalidCallback,
    NetworkError,
    InvalidResponse,
    ReconnectionFailed,
    ResendCommandFailed,
    BrowserNotRunning,
    ElementNotFound,
    ClickIntercepted,
    ElementNotVisible,
    ElementNotInteractable,
    InvalidFileExtension,
    EventNotSupported,
)


def test_connection_failed():
    with pytest.raises(ConnectionFailed) as exc_info:
        raise ConnectionFailed()
    assert str(exc_info.value) == 'Failed to connect to the browser'


def test_invalid_command():
    with pytest.raises(InvalidCommand) as exc_info:
        raise InvalidCommand()
    assert str(exc_info.value) == 'The command provided is invalid'


def test_invalid_callback():
    with pytest.raises(InvalidCallback) as exc_info:
        raise InvalidCallback()
    assert str(exc_info.value) == 'The callback provided is invalid'


def test_network_error():
    with pytest.raises(NetworkError) as exc_info:
        raise NetworkError()
    assert str(exc_info.value) == 'A network error occurred'


def test_invalid_response():
    with pytest.raises(InvalidResponse) as exc_info:
        raise InvalidResponse()
    assert str(exc_info.value) == 'The response received is invalid'


def test_reconnection_failed():
    with pytest.raises(ReconnectionFailed) as exc_info:
        raise ReconnectionFailed()
    assert str(exc_info.value) == 'Failed to reconnect to the browser'


def test_resend_command_failed():
    with pytest.raises(ResendCommandFailed) as exc_info:
        raise ResendCommandFailed()
    assert str(exc_info.value) == 'Failed to resend the command'


def test_browser_not_running():
    with pytest.raises(BrowserNotRunning) as exc_info:
        raise BrowserNotRunning()
    assert str(exc_info.value) == 'The browser is not running'


def test_element_not_found():
    with pytest.raises(ElementNotFound) as exc_info:
        raise ElementNotFound()
    assert str(exc_info.value) == 'The specified element was not found'


def test_click_intercepted():
    with pytest.raises(ClickIntercepted) as exc_info:
        raise ClickIntercepted()
    assert str(exc_info.value) == 'The click was intercepted'


def test_element_not_visible():
    with pytest.raises(ElementNotVisible) as exc_info:
        raise ElementNotVisible()
    assert str(exc_info.value) == 'The element is not visible'


def test_element_not_interactable():
    with pytest.raises(ElementNotInteractable) as exc_info:
        raise ElementNotInteractable()
    assert str(exc_info.value) == 'The element is not interactable'


def test_invalid_file_extension():
    with pytest.raises(InvalidFileExtension) as exc_info:
        raise InvalidFileExtension()
    assert str(exc_info.value) == 'The file extension provided is not supported'


def test_event_not_supported():
    with pytest.raises(EventNotSupported) as exc_info:
        raise EventNotSupported('Custom error message')
    assert str(exc_info.value) == 'Custom error message'

    # Testing default message
    with pytest.raises(EventNotSupported) as exc_info:
        raise EventNotSupported()
    assert str(exc_info.value) == 'The event is not supported'
