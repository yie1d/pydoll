import aiohttp
import pytest
from aioresponses import aioresponses

from pydoll import exceptions
from pydoll.utils import decode_image_to_bytes, get_browser_ws_address


class TestUtils:
    """
    Classe de testes para as funções utilitárias do módulo pydoll.utils.
    Agrupa testes relacionados à decodificação de imagens e comunicação com o navegador.
    """

    def test_decode_image_to_bytes(self):
        """
        Testa a função decode_image_to_bytes.
        Verifica se a função consegue decodificar corretamente uma string base64
        para seus bytes originais.
        """
        base64code = 'aGVsbG8gd29ybGQ='  # 'hello world' em base64
        assert decode_image_to_bytes(base64code) == b'hello world'

    @pytest.mark.asyncio
    async def test_successful_response(self):
        """
        Testa o cenário de sucesso ao obter o endereço WebSocket do navegador.
        Verifica se a função retorna corretamente a URL do WebSocket quando
        a resposta da API contém o campo esperado.
        """
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
    async def test_network_error(self):
        """
        Testa o comportamento da função quando ocorre um erro de rede.
        Verifica se a função lança a exceção NetworkError apropriada
        quando há falha na comunicação com o navegador.
        """
        port = 9222

        with pytest.raises(exceptions.NetworkError):
            with aioresponses() as mocked:
                mocked.get(
                    f'http://localhost:{port}/json/version',
                    exception=aiohttp.ClientError,
                )
                await get_browser_ws_address(port)

    @pytest.mark.asyncio
    async def test_missing_websocket_url(self):
        """
        Testa o comportamento quando a resposta da API não contém a URL do WebSocket.
        Verifica se a função lança a exceção InvalidResponse quando o campo
        'webSocketDebuggerUrl' está ausente na resposta.
        """
        port = 9222

        with aioresponses() as mocked:
            mocked.get(
                f'http://localhost:{port}/json/version',
                payload={'someOtherKey': 'value'},
            )
            with pytest.raises(exceptions.InvalidResponse):
                await get_browser_ws_address(port)
