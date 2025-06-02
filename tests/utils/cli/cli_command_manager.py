import logging
import subprocess
import threading
from typing import Optional

logger = logging.getLogger(__name__)


class CLICommandManager:
    def __init__(self, binary: str = "apolo"):
        self.binary = binary
        self._process: Optional[subprocess.Popen] = None
        self._stdout = ""
        self._stderr = ""

    def run_async(self, *args):
        """Start CLI command asynchronously (non-blocking)."""
        self._process = subprocess.Popen(
            [self.binary, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        thread = threading.Thread(target=self._capture_output)
        thread.daemon = True
        thread.start()

    def _capture_output(self):
        if self._process.stdout:
            self._stdout = self._process.stdout.read()
        if self._process.stderr:
            self._stderr = self._process.stderr.read()

    def is_running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def wait(self, timeout: Optional[int] = None):
        if self._process:
            try:
                self._process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                self._process.kill()
                raise TimeoutError("CLI command timed out")

    def get_output(self) -> str:
        # logger.info(f"\nCLI command output: {self._stdout}")
        return self._stdout.strip()

    def get_error(self) -> str:
        return self._stderr.strip()

    def stop(self):
        if self._process and self.is_running():
            self._process.terminate()
