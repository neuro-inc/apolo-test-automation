from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


class ConfigSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self.current_token = ""
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Login to apolo CLI with access token")
    async def cli_login_with_token(self, token: str) -> None:
        self._current_token = token
        url = self._test_config.cli_login_url
        result, error_message = await self._apolo_cli.config.login_with_token(
            token, url
        )
        assert result, error_message

    @async_step("Verify CLI login output")
    async def cli_verify_login_output(
        self, username: str, org_name: str | None = None, proj_name: str | None = None
    ) -> None:
        url: str = self._test_config.cli_login_url

        assert await self._apolo_cli.config.verify_login_output(
            url, username, org_name, proj_name
        ), "CLI login output should be valid!"

    @async_step("Switch project via CLI")
    async def cli_switch_project(self, proj_name: str) -> None:
        result, error_message = await self._apolo_cli.config.switch_proj(
            proj_name=proj_name
        )
        assert result, error_message

    @async_step("Run config show command via CLI")
    async def cli_show_config(self) -> None:
        result, error_message = await self._apolo_cli.config.config_show()
        assert result, error_message

    @async_step("Switch organization via CLI")
    async def cli_switch_org(self, org_name: str) -> None:
        result, error_message = await self._apolo_cli.config.switch_org(
            org_name=org_name
        )
        assert result, error_message

    @async_step("Verify config show command output")
    async def verify_cli_show_command_output(
        self,
        expected_username: str,
        expected_org: str,
        expected_cluster: str = "default",
        expected_project: str = "<no-project>",
        expected_org_credits: int = 500,
    ) -> None:
        assert await self._apolo_cli.config.verify_config_show_output(
            expected_username=expected_username,
            expected_org=expected_org,
            expected_cluster=expected_cluster,
            expected_project=expected_project,
            expected_org_credit=expected_org_credits,
        ), "Verify config show command output failed!"
