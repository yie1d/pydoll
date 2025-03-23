import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from pydoll.element import WebElement
from pydoll.common.keys import Keys


@pytest_asyncio.fixture
async def mock_connection_handler():
    with patch(
        'pydoll.connection.connection.ConnectionHandler', autospec=True
    ) as mock:
        handler = mock.return_value
        handler.execute_command = AsyncMock()
        yield handler


@pytest.fixture
def web_element(mock_connection_handler):
    attributes_list = [
        'id',
        'test-id',
        'class',
        'test-class',
        'value',
        'test-value',
        'tag_name',
        'div',
    ]
    # Mocking key_down and key_up methods
    element = WebElement(
        object_id='test-object-id',
        connection_handler=mock_connection_handler,
        method='css',
        selector='#test',
        attributes_list=attributes_list,
    )
    element.key_down = AsyncMock()
    element.key_up = AsyncMock()
    return element


@pytest.mark.asyncio
async def test_send_keys_functionality(web_element):
    test_text = 'abc'
    interval = 0.1

    await web_element.send_keys(test_text, interval)

    for key in test_text:
        web_element.key_down.assert_any_call((key, ord(key.upper())))
        web_element.key_up.assert_any_call((key, ord(key.upper())))

    assert web_element.key_down.call_count == len(test_text)
    assert web_element.key_up.call_count == len(test_text)

    await web_element.send_keys(Keys.ENTER, interval)

    web_element.key_down.assert_any_call(Keys.ENTER)
    web_element.key_up.assert_any_call(Keys.ENTER)


@pytest.mark.asyncio
async def test_backspace_removal(web_element):
    web_element._last_input = 'hello'
    web_element.send_keys = AsyncMock()

    await web_element.backspace(interval=0.1)

    assert web_element._last_input == ""

    assert web_element.send_keys.call_count == 5
    web_element.send_keys.assert_any_call(('Backspace', 8))

