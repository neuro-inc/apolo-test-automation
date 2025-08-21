from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.job_data import JobData
from tests.utils.test_data_management.test_data import DataManager


class JobSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Verify CLI login output")
    async def run_job(self, job: JobData) -> str:
        job_id = await self._apolo_cli.job.run_job(
            job_name=job.job_name,
            image=job.image_name,
            command=job.command,
        )
        assert job_id, "Job ID is None, check logs!"
        return job_id
