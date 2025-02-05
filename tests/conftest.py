import asyncio
import json
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
import pytest_asyncio
import websockets

from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options
from pydoll.connection.connection import ConnectionHandler


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

            # Função para enviar um evento não json
            async def send_event_non_json():
                await asyncio.sleep(0.1)
                await websocket.send('Non JSON event')

            # Envio de evento em paralelo com a recepção de mensagens
            send_event_task = asyncio.create_task(send_event())
            send_event_non_json_task = asyncio.create_task(
                send_event_non_json()
            )

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
            await send_event_non_json_task
        except websockets.ConnectionClosed:
            pass

    server = await websockets.serve(echo_server, 'localhost', 9222)

    yield server
    server.close()
    await server.wait_closed()


@pytest_asyncio.fixture(scope='function')
async def page_handler(ws_server):
    return ConnectionHandler(connection_port=9222, page_id='page_id')


@pytest.fixture
def mock_runtime_commands():
    with patch('pydoll.commands.dom.RuntimeCommands') as mock:
        yield mock


@pytest.fixture
def mock_connection_handler():
    with patch('pydoll.browser.base.ConnectionHandler') as MockHandler:
        yield MockHandler


@pytest_asyncio.fixture
async def mock_browser_instance(mock_connection_handler):
    options = MagicMock(spec=Options)
    return Chrome(options=options, connection_port=9222)


@pytest_asyncio.fixture
async def mock_browser_class(mock_connection_handler):
    return Chrome


@pytest.fixture
def mock_shutil():
    with patch('pydoll.browser.base.shutil') as mock_shutil:
        yield mock_shutil


@pytest.fixture
def mock_temp_dir():
    with patch('pydoll.browser.base.TemporaryDirectory') as mock_temp_dir:
        mock_temp_dir.return_value = MagicMock()
        mock_temp_dir.return_value.name = 'temp_dir'
        yield mock_temp_dir


@pytest.fixture
def mock_os_name():
    with patch('pydoll.browser.chrome.os') as mock_os:
        type(mock_os).name = PropertyMock(return_value='posix')
        yield mock_os


@pytest.fixture
def mock_options():
    mock = MagicMock()
    mock.binary_location = None
    mock.arguments = []
    return mock


@pytest.fixture
def mock_subprocess_popen():
    with patch('pydoll.browser.base.subprocess.Popen') as mock_popen:
        yield mock_popen
