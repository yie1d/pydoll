import subprocess


class BrowserProcessManager:
    def __init__(self, process_creator=None):
        """
        Initializes the BrowserProcessManager.

        This manager handles the creation and management of browser processes.

        Args:
            process_creator (callable, optional): A function that creates a
                browser process. If None, the default process creator is used.
        """
        self._process_creator = (
            process_creator or self._default_process_creator
        )
        self._process = None

    def start_browser_process(
        self, binary_location: str, port: int, arguments: list
    ) -> None:
        """
        Starts the browser process with the given parameters.

        This method launches a new browser process with the specified binary,
        debugging port, and command-line arguments.

        Args:
            binary_location (str): Path to the browser executable.
            port (int): The remote debugging port to use.
            arguments (list): Additional command-line arguments for the
                browser.

        Returns:
            subprocess.Popen: The started browser process.
        """
        self._process = self._process_creator([
            binary_location,
            f'--remote-debugging-port={port}',
            *arguments,
        ])
        return self._process

    @staticmethod
    def _default_process_creator(command: list[str]):
        """
        Default function to create a browser process.

        This method creates a subprocess with the given command-line arguments.

        Args:
            command (list[str]): The command and arguments to start the
                process.

        Returns:
            subprocess.Popen: The created process instance.
        """
        return subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def stop_process(self):
        """
        Stops the browser process if it's running.

        This method terminates the browser process that was previously
        started with start_browser_process.

        Returns:
            None
        """
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self._process.kill()
