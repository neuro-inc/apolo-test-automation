import asyncio
import logging
from typing import Optional


from tests.utils.cli.cli_command_manager import CLICommandManager

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloRunner:
    def __init__(self) -> None:
        self._binary: str = "apolo"
        self._manager: CLICommandManager = CLICommandManager(binary=self._binary)
        self.last_command_executed: str = ""
        self.last_command_output: str = ""

    async def is_cli_installed(self) -> tuple[bool, str]:
        return await self.run_command("--version", action="check CLI version")

    async def run_command(
        self, *args: str, action: str, timeout: Optional[int] = None
    ) -> tuple[bool, str]:
        default_timeout: int = timeout if timeout else 60
        logger.info(
            f"{action}. Running command via cli:\n\n{self._binary} {' '.join(args)}\n"
        )
        self.last_command_executed = f"{self._binary} {' '.join(args)}"

        try:
            await asyncio.wait_for(
                self._manager.run_async(*args), timeout=default_timeout
            )
            await asyncio.wait_for(self._manager.wait(), timeout=default_timeout)
        except asyncio.TimeoutError:
            if hasattr(self._manager, "kill"):
                self._manager.kill()
            elif hasattr(self._manager, "process") and self._manager.process:
                self._manager.process.kill()
            logger.error(
                f"Command timed out after {default_timeout} seconds and was killed."
            )
            raise Exception(
                f"Command timed out after {default_timeout} seconds and was killed."
            )
        except Exception as exc:
            logger.exception(f"Error running command {args}: {exc}")
            raise

        raw_output = await self._manager.get_output()
        raw_error = await self._manager.get_error()

        def clean_output(text: str) -> str:
            if not text:
                return ""

            ignored_starts = [
                "You are using",
                "You should consider upgrading via the following command:",
            ]

            cleaned_lines: list[str] = []
            skip_block = False
            for line in text.splitlines():
                if any(line.strip().startswith(prefix) for prefix in ignored_starts):
                    skip_block = True
                    continue
                if skip_block and (
                    line.strip().startswith("python -m") or not line.strip()
                ):
                    continue
                skip_block = False
                cleaned_lines.append(line)

            return "\n".join(cleaned_lines)

        self.last_command_output = raw_output
        cleaned_error = clean_output(raw_error)

        if cleaned_error:
            error_message = f"{action} failed:\n\n{cleaned_error}\n{self.last_command_output or ''}\n"
            logger.error(error_message)
            self.last_command_output = cleaned_error
            return False, cleaned_error

        logger.info(f"{action} succeeded:\n\n{self.last_command_output}\n")
        return True, ""
