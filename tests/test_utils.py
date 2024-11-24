import aiohttp
import pytest
from aioresponses import aioresponses

from pydoll import exceptions
from pydoll.utils import decode_image_to_bytes, get_browser_ws_address


def test_decode_image_to_bytes():
    base64code = 'aGVsbG8gd29ybGQ='
    assert decode_image_to_bytes(base64code) == b'hello world'


@pytest.mark.asyncio
async def test_successful_response():
    """Teste para uma resposta bem-sucedida retornando o WebSocket URL."""
    port = 9222
    expected_url = 'ws://localhost:9222/devtools/browser/abc123'

    with aioresponses() as mocked:
        mocked.get(
            f'http://localhost:{port}/json/version',
            payload={'webSocketDebuggerUrl': expected_url},
        )

        result = await get_browser_ws_address(port)
        assert result == expected_url


@pytest.mark.asyncio
async def test_network_error():
    """Teste para erro de rede (aiohttp.ClientError)."""
    port = 9222

    with pytest.raises(exceptions.NetworkError):  # noqa: PT012
        with aioresponses() as mocked:
            mocked.get(
                f'http://localhost:{port}/json/version',
                exception=aiohttp.ClientError,
            )
            await get_browser_ws_address(port)


@pytest.mark.asyncio
async def test_missing_websocket_url():
    """Teste para KeyError quando o campo esperado não está na resposta."""
    port = 9222

    with aioresponses() as mocked:
        mocked.get(
            f'http://localhost:{port}/json/version',
            payload={'someOtherKey': 'value'},
        )

        with pytest.raises(exceptions.InvalidResponse):
            await get_browser_ws_address(port)
