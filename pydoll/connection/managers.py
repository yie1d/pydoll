import asyncio
import logging
from typing import Callable, Dict

from pydoll import exceptions

logger = logging.getLogger(__name__)


class CommandManager:
    def __init__(self):
        self._pending_commands: dict[int, asyncio.Future] = {}
        self._id = 1

    def create_command_future(self, command: dict) -> asyncio.Future:
        command['id'] = self._id
        future = asyncio.Future()
        self._pending_commands[self._id] = future
        self._id += 1
        return future

    def resolve_command(self, response_id: int, result: str):
        if response_id in self._pending_commands:
            self._pending_commands[response_id].set_result(result)
            del self._pending_commands[response_id]

    def remove_pending_command(self, command_id: int):
        """
        Remove um comando pendente sem resolvê-lo (útil para timeouts).

        Args:
            command_id: ID do comando a ser removido
        """
        if command_id in self._pending_commands:
            del self._pending_commands[command_id]


class EventsHandler:
    """
    Gerencia registro de callbacks, processamento de eventos e logs de rede.
    """

    def __init__(self):
        self._event_callbacks: Dict[int, dict] = {}
        self._callback_id = 0
        self.network_logs = []
        self.dialog = {}
        logger.info('EventsHandler initialized')

    def register_callback(
        self, event_name: str, callback: Callable, temporary: bool = False
    ) -> int:
        """
        Registra um callback para um tipo específico de evento.

        Retorna:
            int: ID do callback registrado
        """
        if not callable(callback):
            logger.error('Callback must be a callable function.')
            raise exceptions.InvalidCallback('Callback must be callable')

        self._callback_id += 1
        self._event_callbacks[self._callback_id] = {
            'event': event_name,
            'callback': callback,
            'temporary': temporary,
        }
        logger.info(
            f"Registered callback '{event_name}' with ID {self._callback_id}"
        )
        return self._callback_id

    def remove_callback(self, callback_id: int) -> bool:
        """Remove um callback pelo ID."""
        if callback_id not in self._event_callbacks:
            logger.warning(f'Callback ID {callback_id} not found')
            return False

        del self._event_callbacks[callback_id]
        logger.info(f'Removed callback ID {callback_id}')
        return True

    def clear_callbacks(self):
        """Reseta todos os callbacks registrados."""
        self._event_callbacks.clear()
        logger.info('All callbacks cleared')

    async def process_event(self, event_data: dict):
        """
        Processa um evento recebido e dispara os callbacks correspondentes.

        Args:
            event_data: Dados do evento no formato dicionário
        """
        event_name = event_data.get('method')
        logger.debug(f'Processing event: {event_name}')

        # Atualiza logs de rede se necessário
        if 'Network.requestWillBeSent' in event_name:
            self._update_network_logs(event_data)

        if 'Page.javascriptDialogOpening' in event_name:
            self.dialog = event_data

        if 'Page.javascriptDialogClosed' in event_name:
            self.dialog = {}

        # Processa callbacks
        await self._trigger_callbacks(event_name, event_data)

    def _update_network_logs(self, event_data: dict):
        """Mantém os logs de rede atualizados."""
        self.network_logs.append(event_data)
        self.network_logs = self.network_logs[-10000:]  # Mantém tamanho máximo

    async def _trigger_callbacks(self, event_name: str, event_data: dict):
        """Dispara todos os callbacks registrados para o evento."""
        callbacks_to_remove = []

        for cb_id, cb_data in list(self._event_callbacks.items()):
            if cb_data['event'] == event_name:
                try:
                    if asyncio.iscoroutinefunction(cb_data['callback']):
                        await cb_data['callback'](event_data)
                    else:
                        cb_data['callback'](event_data)
                except Exception as e:
                    logger.error(f'Error in callback {cb_id}: {str(e)}')

                if cb_data['temporary']:
                    callbacks_to_remove.append(cb_id)

        # Remove callbacks temporários após processamento
        for cb_id in callbacks_to_remove:
            self.remove_callback(cb_id)
