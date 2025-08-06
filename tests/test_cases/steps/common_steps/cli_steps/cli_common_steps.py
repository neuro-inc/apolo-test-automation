from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UserData


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
        self._current_token = ""

    @async_step("Login to apolo CLI with access token")
    async def cli_login_with_token(self, token: str) -> None:
        self._current_token = token
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
    async def cli_add_new_organization(self, gherkin_name: str, user: UserData) -> None:
        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        try:
            await self._apolo_cli.create_organization(org_name=organization.org_name)
            user.orgs.append(organization.org_name)
        except Exception as ex:
            msg = str(ex)
            if (
                "ERROR: There are no clusters available. Please logout and login again."
                in msg
            ):
                await self.cli_login_with_token(self._current_token)
            else:
                raise

    @async_step("Add new project via apolo CLI")
    async def cli_add_new_project(
        self,
        org_name: str,
        proj_name: str,
        default_role: str = "reader",
        default_proj: bool = False,
    ) -> None:
        await self._apolo_cli.create_project(
            org_name=org_name,
            proj_name=proj_name,
            default_role=default_role,
            default_proj=default_proj,
        )

    @async_step("Run admin get-projects via CLI")
    async def cli_run_get_projects(self, org_name: str) -> None:
        await self._apolo_cli.get_projects(org_name=org_name)

    @async_step("Add user to project via CLI")
    async def cli_add_user_to_project(
        self, org_name: str, proj_name: str, username: str, role: str
    ) -> None:
        await self._apolo_cli.add_proj_user(
            org_name=org_name, proj_name=proj_name, username=username, role=role
        )

    @async_step("Verify admin get-projects output via CLI")
    async def verify_cli_admin_get_projects_output(
        self, org_name: str, proj_name: str, default_role: str, default_proj: bool
    ) -> None:
        await self._apolo_cli.verify_get_projects_output(
            org_name=org_name,
            proj_name=proj_name,
            default_role=default_role,
            default_proj=default_proj,
        )

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

    @async_step("Run config show command via CLI")
    async def cli_show_config(self) -> None:
        assert await self._apolo_cli.config_show(), (
            "Run config show command via CLI failed!"
        )

    @async_step("Switch organization via CLI")
    async def cli_switch_org(self, org_name: str) -> None:
        assert await self._apolo_cli.switch_org(org_name=org_name), (
            "Run config switch-org command via CLI failed!"
        )

    @async_step("Add user to organization via CLI")
    async def cli_add_user_to_org(
        self, org_name: str, username: str, role: str = "user"
    ) -> None:
        assert await self._apolo_cli.add_user_to_org(
            org_name=org_name, username=username, role=role.lower()
        ), "Run config add-user-to-org command via CLI failed!"

    @async_step("Get organization users via CLI")
    async def cli_get_org_users(self, org_name: str) -> None:
        assert await self._apolo_cli.get_org_users(org_name=org_name), (
            "Run admin get-org-users command via CLI failed!"
        )

    @async_step("Verify admin get-org-users command output")
    async def verify_cli_admin_get_orgs_users_output(
        self, username: str, role: str, email: str, credits: str | float | int
    ) -> None:
        await self._apolo_cli.verify_get_org_users_output(
            username=username, role=role, email=email, credits=credits
        )

    @async_step("Set organization credits via CLI")
    async def cli_set_org_default_credits(
        self, org_name: str, credits_amount: int
    ) -> None:
        assert await self._apolo_cli.set_org_default_credits(
            org_name=org_name, credits_amount=credits_amount
        ), "Run config set-org-defaults command via CLI failed!"

    @async_step("Verify config show command output")
    async def verify_cli_show_command_output(
        self,
        expected_username: str,
        expected_org: str,
        expected_cluster: str = "default",
        expected_project: str = "<no-project>",
        expected_org_credits: int = 500,
    ) -> None:
        assert await self._apolo_cli.verify_config_show_output(
            expected_username=expected_username,
            expected_org=expected_org,
            expected_cluster=expected_cluster,
            expected_project=expected_project,
            expected_org_credit=expected_org_credits,
        ), "Verify config show command output failed!"
