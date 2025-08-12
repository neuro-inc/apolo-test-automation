from tests.reporting_hooks.reporting import async_step
from tests.test_cases.steps.cli_steps.comonent_steps_impl.admin_steps import AdminSteps
from tests.test_cases.steps.cli_steps.comonent_steps_impl.config_steps import (
    ConfigSteps,
)
from tests.test_cases.steps.cli_steps.comonent_steps_impl.disk_steps import DiskSteps
from tests.test_cases.steps.cli_steps.comonent_steps_impl.job_steps import JobSteps
from tests.test_cases.steps.cli_steps.comonent_steps_impl.secret_steps import (
    SecretSteps,
)
from tests.test_cases.steps.cli_steps.comonent_steps_impl.storage_steps import (
    StorageSteps,
)
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


class CLISteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

        self.admin = AdminSteps(
            test_config=test_config, apolo_cli=apolo_cli, data_manager=data_manager
        )
        self.config = ConfigSteps(
            test_config=test_config, apolo_cli=apolo_cli, data_manager=data_manager
        )
        self.disk = DiskSteps(
            test_config=test_config, apolo_cli=apolo_cli, data_manager=data_manager
        )
        self.job = JobSteps(
            test_config=test_config, apolo_cli=apolo_cli, data_manager=data_manager
        )
        self.storage = StorageSteps(
            test_config=test_config, apolo_cli=apolo_cli, data_manager=data_manager
        )
        self.secret = SecretSteps(
            test_config=test_config, apolo_cli=apolo_cli, data_manager=data_manager
        )

    @async_step("Verify Apolo CLI client is installed")
    async def verify_cli_client_installed(self) -> None:
        result, error_message = await self._apolo_cli.runner.is_cli_installed()
        assert result, error_message
