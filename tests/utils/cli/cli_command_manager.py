import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class CLICommandManager:
    def __init__(self, binary: str = "apolo") -> None:
        self.binary: str = binary
        self._process: Optional[asyncio.subprocess.Process] = None
        self._stdout: str = ""
        self._stderr: str = ""
        self._raw_stderr: str = ""

    async def run_async(self, *args: str) -> None:
        """Start CLI command asynchronously (non-blocking)."""
        self._process = await asyncio.create_subprocess_exec(
            self.binary,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await self._capture_output()

    async def _capture_output(self) -> None:
        if not self._process:
            return

        stdout_data, stderr_data = await self._process.communicate()
        self._stdout = stdout_data.decode().strip()

        stderr_text = stderr_data.decode().strip()
        self._raw_stderr = stderr_text

        returncode = self._process.returncode
        if returncode and returncode != 0:
            self._stderr = stderr_text
        else:
            self._stderr = ""

    async def is_running(self) -> bool:
        return self._process is not None and self._process.returncode is None

    async def wait(self, timeout: Optional[int] = None) -> None:
        if self._process:
            try:
                await asyncio.wait_for(self._process.wait(), timeout=timeout)
            except TimeoutError:
                self._process.kill()
                raise TimeoutError("CLI command timed out")

    async def get_output(self) -> str:
        return self._stdout

    async def get_error(self) -> str:
        return self._stderr

    async def stop(self) -> None:
        if self._process and await self.is_running():
            self._process.terminate()
