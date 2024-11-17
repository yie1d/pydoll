import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import websockets

from pydoll import exceptions


@pytest.mark.asyncio
async def test_connection_initialization(handler):
    DEFAULT_PORT = 9222
    assert handler._connection_port == DEFAULT_PORT
    assert handler._page_id == 'browser'
    assert handler._connection is None


@pytest.mark.asyncio
async def test_connect_to_page(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        assert handler._connection is not None


@pytest.mark.asyncio
async def test_execute_command(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        response = await handler.execute_command({'method': 'test'})
        assert response == {'id': 1, 'result': 'success'}


@pytest.mark.asyncio
async def test_id_increment(handler):
    EXPECTED_ID = 3
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        await handler.execute_command({'method': 'test'})
        await handler.execute_command({'method': 'test'})
        assert handler._id == EXPECTED_ID


@pytest.mark.asyncio
async def test_execute_command_timeout(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        with pytest.raises(asyncio.TimeoutError):
            with patch(
                'pydoll.connection.asyncio.wait_for',
                side_effect=asyncio.TimeoutError,
            ):
                await handler.execute_command({'method': 'test'})


@pytest.mark.asyncio
async def test_register_callback(handler):
    EXPECTED_CALLBACK_ID = 2
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        callback = MagicMock()
        await handler.register_callback('test', callback)
        assert handler._callback_id == EXPECTED_CALLBACK_ID
        assert handler._event_callbacks[1] == {
            'event': 'test',
            'callback': callback,
            'temporary': False,
        }


@pytest.mark.asyncio
async def test_register_temporary_callback(handler):
    EXPECTED_CALLBACK_ID = 2
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        callback = MagicMock()
        await handler.register_callback('test', callback, temporary=True)
        assert handler._callback_id == EXPECTED_CALLBACK_ID
        assert handler._event_callbacks[1] == {
            'event': 'test',
            'callback': callback,
            'temporary': True,
        }


@pytest.mark.asyncio
async def test_callback_id_increment(handler):
    EXPECTED_CALLBACK_ID = 3
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        callback = MagicMock()
        await handler.register_callback('test', callback)
        await handler.register_callback('test', callback)
        assert handler._callback_id == EXPECTED_CALLBACK_ID


@pytest.mark.asyncio
async def test_callback_execution(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        callback = MagicMock()
        await handler.register_callback('Network.requestWillBeSent', callback)
        await handler.connect_to_page()
        await asyncio.sleep(0.2)
        callback.assert_called_once()


@pytest.mark.asyncio
async def test_callback_removal(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        callback = MagicMock()
        await handler.register_callback(
            'Network.requestWillBeSent', callback, temporary=True
        )
        await handler.connect_to_page()
        await asyncio.sleep(0.2)
        callback.assert_called_once()
        assert handler._event_callbacks == {}


@pytest.mark.asyncio
async def test_network_events_are_being_saved(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        await asyncio.sleep(0.2)
        assert handler.network_logs == [
            {'method': 'Network.requestWillBeSent', 'params': {}}
        ]


@pytest.mark.asyncio
async def test_execute_invalid_command(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        with pytest.raises(exceptions.InvalidCommand):
            await handler.execute_command('Invalid command')


@pytest.mark.asyncio
async def test_register_invalid_callback(handler):
    with pytest.raises(exceptions.InvalidCallback):
        await handler.register_callback('test', 'Invalid callback')


@pytest.mark.asyncio
async def test_async_callback_execution(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        callback = AsyncMock()
        await handler.register_callback('Network.requestWillBeSent', callback)
        await handler.connect_to_page()
        await asyncio.sleep(0.2)
        callback.assert_called_once()


@pytest.mark.asyncio
async def test_clear_callbacks(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        callback = MagicMock()
        await handler.register_callback('Network.requestWillBeSent', callback)
        handler.clear_callbacks()
        assert handler._event_callbacks == {}


@pytest.mark.asyncio
async def test_close(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        await handler.connect_to_page()
        callback = MagicMock()
        await handler.register_callback('Network.requestWillBeSent', callback)
        await handler.close()
        handler._connection.closed is True


def test_repr(handler):
    assert repr(handler) == 'ConnectionHandler(port=9222)'


def test_str(handler):
    assert str(handler) == 'ConnectionHandler(port=9222)'


@pytest.mark.asyncio
async def test_aenter(handler):
    async with handler as h:
        h._connection = AsyncMock()
        assert h is handler


@pytest.mark.asyncio
async def test_aexit(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        async with handler as h:
            await h.connect_to_page()

    assert h._connection.closed is True
    assert h._event_callbacks == {}


@pytest.mark.asyncio
async def test_connection_property(handler):
    with patch(
        'pydoll.connection.get_browser_ws_address', new_callable=AsyncMock
    ) as mock_get_browser_ws_address:
        mock_get_browser_ws_address.return_value = 'ws://localhost:9222'
        connection = await handler.connection
        assert connection is handler._connection
        assert (
            isinstance(connection, websockets.WebSocketClientProtocol) is True
        )
