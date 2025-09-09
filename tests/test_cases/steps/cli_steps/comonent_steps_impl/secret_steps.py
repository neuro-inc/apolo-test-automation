from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


class SecretSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Create secret via CLI")
    async def cli_create_secret(
        self,
        secret_name: str,
        secret_value: str,
        expected_error: str = "",
    ) -> None:
        result, error_message = await self._apolo_cli.secret.create_secret(
            secret_name=secret_name,
            secret_value=secret_value,
        )
        if expected_error:
            assert not result, f"Command should fail with: {expected_error}"
            assert error_message == expected_error, (
                f"Expected: \n{expected_error} \nbut got \n{error_message}"
            )
        else:
            assert result, error_message

    @async_step("List secrets via CLI")
    async def cli_list_secrets(self) -> None:
        result, error_message = await self._apolo_cli.secret.list_secrets()
        assert result, error_message

    @async_step("Remove secret via CLI")
    async def cli_remove_secret(self, secret_name: str) -> None:
        result, error_message = await self._apolo_cli.secret.remove_secret(
            secret_name=secret_name
        )
        assert result, error_message

    @async_step("Verify secret listed in list secrets output")
    async def verify_secret_listed(
        self, secret_name: str, org_name: str, proj_name: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.secret.verify_secret_in_list_output(
            key=secret_name, org_name=org_name, proj_name=proj_name
        )
        assert result, error_message

    @async_step("Verify secret not listed in list secrets output")
    async def verify_secret_not_listed(
        self, secret_name: str, org_name: str, proj_name: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.secret.verify_secret_in_list_output(
            key=secret_name, org_name=org_name, proj_name=proj_name
        )
        assert not result, (
            f"Secret {secret_name} should not be listed in secrets output"
        )
