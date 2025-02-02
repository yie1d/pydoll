import os
import shutil
import subprocess
from contextlib import suppress
from tempfile import TemporaryDirectory

from pydoll.browser.options import Options


class ProxyManager:
    def __init__(self, options):
        self.options = options

    def get_proxy_credentials(self) -> tuple[bool, tuple[str, str]]:
        """
        Configura as configurações de proxy e extrai credenciais se presentes.

        Returns:
            tuple[bool, tuple[str, str]]: (private_proxy, (username, password))
        """
        private_proxy = False
        credentials = (None, None)

        proxy_arg = self._find_proxy_argument()

        if proxy_arg is not None:
            index, proxy_value = proxy_arg
            has_credentials, username, password, clean_proxy = (
                self._parse_proxy(proxy_value)
            )

            if has_credentials:
                self._update_proxy_argument(index, clean_proxy)
                private_proxy = True
                credentials = (username, password)

        return private_proxy, credentials

    def _find_proxy_argument(self) -> tuple[int, str] | None:
        """Encontra o primeiro argumento --proxy-server válido"""
        for index, arg in enumerate(self.options.arguments):
            if arg.startswith('--proxy-server='):
                return index, arg.split('=', 1)[1]
        return None

    @staticmethod
    def _parse_proxy(proxy_value: str) -> tuple[bool, str, str, str]:
        """Extrai credenciais e limpa o valor do proxy"""
        if '@' not in proxy_value:
            return False, None, None, proxy_value

        try:
            creds_part, server_part = proxy_value.split('@', 1)
            username, password = creds_part.split(':', 1)
            return True, username, password, server_part
        except ValueError:
            return False, None, None, proxy_value

    def _update_proxy_argument(self, index: int, clean_proxy: str) -> None:
        """Atualiza a lista de argumentos com proxy limpo"""
        self.options.arguments[index] = f'--proxy-server={clean_proxy}'


class BrowserProcessManager:
    def __init__(self, process_creator=None):
        self._process_creator = (
            process_creator or self._default_process_creator
        )
        self._process = None

    def start_browser_process(
        self, binary_location: str, port: int, arguments: list
    ) -> None:
        """Inicia o processo do navegador"""
        self._process = self._process_creator([
            binary_location,
            f'--remote-debugging-port={port}',
            *arguments,
        ])
        return self._process

    @staticmethod
    def _default_process_creator(command: list[str]):
        return subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def stop_process(self):
        """Para o processo do navegador se estiver em execução"""
        if self._process:
            self._process.terminate()


class TempDirectoryManager:
    def __init__(self, temp_dir_factory=TemporaryDirectory):
        self._temp_dir_factory = temp_dir_factory
        self._temp_dirs = []

    def create_temp_dir(self):
        """
        Cria um diretório temporário para a instância do navegador.

        Returns:
            TemporaryDirectory: O diretório temporário.
        """
        temp_dir = self._temp_dir_factory()
        self._temp_dirs.append(temp_dir)
        return temp_dir

    def cleanup(self):
        """Limpa todos os diretórios temporários"""
        for temp_dir in self._temp_dirs:
            with suppress(OSError):
                shutil.rmtree(temp_dir.name)


class BrowserOptionsManager:
    @staticmethod
    def initialize_options(options: Options | None) -> Options:
        """
        Inicializa as opções para o navegador.

        Args:
            options (Options | None): Uma instância da classe Options ou None.

        Returns:
            Options: A instância de opções inicializada.
        """
        if options is None:
            return Options()
        if not isinstance(options, Options):
            raise ValueError('Invalid options')
        return options

    @staticmethod
    def add_default_arguments(options: Options):
        """Adiciona argumentos padrão aos argumentos fornecidos"""
        options.arguments.append('--no-first-run')
        options.arguments.append('--no-default-browser-check')

    @staticmethod
    def validate_browser_path(path: str) -> str:
        """
        Valida o caminho fornecido do navegador.

        Args:
            path (str): O caminho do arquivo executável do navegador.

        Returns:
            str: O caminho do navegador validado.
        """
        if not os.path.exists(path):
            raise ValueError(f'Browser not found: {path}')
        return path
