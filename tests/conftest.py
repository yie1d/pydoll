import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
import websockets

from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options
from pydoll.connection import ConnectionHandler


@pytest_asyncio.fixture
async def ws_server():
    async def echo_server(websocket, path):
        try:
            # Função para enviar um evento
            async def send_event():
                await asyncio.sleep(0.1)
                await websocket.send(
                    json.dumps({
                        'method': 'Network.requestWillBeSent',
                        'params': {},
                    })
                )

            # Envio de evento em paralelo com a recepção de mensagens
            send_event_task = asyncio.create_task(send_event())

            async for message in websocket:
                data = json.loads(message)
                if 'id' in data:
                    response = json.dumps({
                        'id': data['id'],
                        'result': 'success',
                    })
                    await websocket.send(response)

            # Espera a tarefa do evento ser concluída antes de fechar a conexão
            await send_event_task
        except websockets.ConnectionClosed:
            pass

    server = await websockets.serve(echo_server, 'localhost', 9222)

    yield server
    server.close()
    await server.wait_closed()


@pytest_asyncio.fixture(scope='function')
async def handler(ws_server):
    return ConnectionHandler(connection_port=9222)


@pytest.fixture
def mock_runtime_commands():
    with patch('pydoll.commands.dom.RuntimeCommands') as mock:
        yield mock


@pytest.fixture
def mock_subprocess_popen():
    with patch('pydoll.browser.base.subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        yield mock_popen, mock_process


@pytest.fixture
def mock_connection_handler():
    with patch('pydoll.browser.base.ConnectionHandler') as mock_handler_cls:
        mock_handler = AsyncMock(spec=ConnectionHandler)
        mock_handler_cls.return_value = mock_handler
        yield mock_handler_cls, mock_handler


@pytest.fixture
def browser_instance(mock_connection_handler):
    options = Options()
    return Chrome(options=options, connection_port=9222)
