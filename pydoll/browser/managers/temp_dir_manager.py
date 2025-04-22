import inspect
import shutil
import time
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory


class TempDirectoryManager:
    def __init__(self, temp_dir_factory=TemporaryDirectory):
        """
        Initializes the TempDirectoryManager.

        This manager handles the creation and cleanup of temporary directories
        used by browser instances.

        Args:
            temp_dir_factory (callable, optional): A function that creates
                temporary directories. Defaults to TemporaryDirectory.
        """
        sig = inspect.signature(temp_dir_factory)
        if 'prefix' in sig.parameters:
            temp_dir_factory = partial(
                temp_dir_factory, prefix='pydoll_chromium_profile-'
            )
        self._temp_dir_factory = temp_dir_factory
        self._temp_dirs = []

    def create_temp_dir(self):
        """
        Creates a temporary directory for a browser instance.

        This method creates a new temporary directory and tracks it
        for later cleanup.

        Returns:
            TemporaryDirectory: The created temporary directory instance.
        """
        temp_dir = self._temp_dir_factory()
        self._temp_dirs.append(temp_dir)
        return temp_dir

    @staticmethod
    def retry_process_file(func: callable, path: str, retry_times: int = 10):
        """
        Repeatedly attempts to execute a function until it succeeds or the
         number of retries is exhausted.

        Args:
            func (callable): process function to execute.
            path (str): The path of the temporary directory.:
            retry_times (int): The number of times to retry the process.
                Defaults to 10.

        Returns:

        """
        retry_time = 0
        while retry_times < 0 or retry_time < retry_times:
            retry_time += 1
            try:
                func(path)
                break
            except PermissionError:
                time.sleep(0.1)
        else:
            raise PermissionError

    def handle_cleanup_error(self, func: callable, path: str, exc_info: tuple):
        """
        Handles errors during directory removal.

        Args:
            func (callable): The function that raised the exception.
            path (str): The path of the temporary directory.:
            exc_info (tuple): The exception information. From sys.exc_info()

        Returns:

        """
        matches = ['CrashpadMetrics-active.pma']
        exc_type, exc_value, _ = exc_info

        if exc_type is PermissionError:
            if Path(path).name in matches:
                try:
                    self.retry_process_file(func, path)
                    return
                except PermissionError:
                    raise exc_value
        elif exc_type is OSError:
            return
        raise exc_value

    def cleanup(self):
        """
        Cleans up all temporary directories created by this manager.

        This method removes all temporary directories created with
        create_temp_dir, suppressing any OS errors that might occur
        during deletion.

        Returns:
            None
        """
        for temp_dir in self._temp_dirs:
            shutil.rmtree(temp_dir.name, onerror=self.handle_cleanup_error)
