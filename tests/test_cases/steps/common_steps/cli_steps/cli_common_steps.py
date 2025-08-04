from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


class CLICommonSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Login to apolo CLI with access token")
    async def cli_login_with_token(self) -> None:
        token = self._test_config.token
        url = self._test_config.cli_login_url
        await self._apolo_cli.login_with_token(token, url)
        assert self._apolo_cli.login_successful, "Login via CLI should be successful!"

    @async_step("Verify Apolo CLI client is installed")
    async def verify_cli_client_installed(self) -> None:
        assert await self._apolo_cli.is_cli_installed(), (
            "Apolo CLI client should be installed!"
        )

    @async_step("Verify organization_count")
    async def verify_cli_organization_count(self, count: int) -> None:
        organizations = await self._apolo_cli.get_organizations()
        assert len(organizations) == count, (
            f"Expected {count} organizations, got {len(organizations)}"
        )

    @async_step("Add new organization via apolo CLI")
    async def cli_add_new_organization(self, gherkin_name: str) -> None:
        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        try:
            await self._apolo_cli.create_organization(org_name=organization.org_name)
        except Exception as ex:
            msg = str(ex)
            if (
                "ERROR: There are no clusters available. Please logout and login again."
                in msg
            ):
                await self.cli_login_with_token()
            else:
                raise

    @async_step("Verify organization is listed in the CLI output")
    async def verify_cli_organization_listed(self, gherkin_name: str) -> None:
        created_organizations = self._data_manager.get_all_organizations()
        org = next(
            (o for o in created_organizations if o.gherkin_name == gherkin_name), None
        )
        assert org is not None, (
            f"No organization found with gherkin_name '{gherkin_name}'"
        )

        assert org.org_name in self._apolo_cli.parsed_get_orgs_output, (
            f"Organization '{org.org_name}' (for gherkin_name '{gherkin_name}') "
            f"not found in CLI output: {self._apolo_cli.parsed_get_orgs_output}"
        )

    @async_step("Remove organization via CLI")
    async def cli_remove_org(self, gherkin_name: str) -> None:
        org = self._data_manager.get_organization_by_gherkin_name(gherkin_name)
        org_name = org.org_name
        await self._apolo_cli.remove_organization(org_name=org_name)
        self._data_manager.remove_organization(org_name=org_name)
