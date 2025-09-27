import logging
import re

from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloJob:
    def __init__(self, runner: ApoloRunner) -> None:
        self._runner = runner

    async def run_job(
        self,
        job_name: str,
        image: str,
        command: str,
        wait_for_output_timeout: int = 60,
    ) -> str:
        base_command = ["job", "run", "--name", job_name, image, "--"]
        command_parts = command.strip().split()
        cli_args = base_command + command_parts

        result, error_message = await self._runner.run_command(
            *cli_args, action=f"run job '{job_name}'", timeout=wait_for_output_timeout
        )
        if not result:
            raise RuntimeError(error_message)

        job_id_match = re.search(
            r"Job ID:\s*(job-[\w-]+)", self._runner.last_command_output or ""
        )
        logger.info(f"Job ID match: {job_id_match}")
        job_id = job_id_match.group(1) if job_id_match else ""
        logger.info(f"Job ID logging: {job_id}")

        if job_id:
            logger.info(f"Extracted Job ID: {job_id}")
        else:
            logger.warning("Job ID not found in output.")

        return job_id
