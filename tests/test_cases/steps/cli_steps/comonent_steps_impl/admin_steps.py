from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UserData


class AdminSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Verify organization_count")
    async def verify_cli_organization_count(self, count: int) -> None:
        organizations = await self._apolo_cli.admin.get_organizations()
        assert len(organizations) == count, (
            f"Expected {count} organizations, got {len(organizations)}"
        )

    @async_step("Add new organization via apolo CLI")
    async def cli_add_new_organization(self, gherkin_name: str, user: UserData) -> None:
        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        result, error_message = await self._apolo_cli.admin.create_organization(
            org_name=organization.org_name
        )
        if not result:
            if (
                "ERROR: There are no clusters available. Please run 'apolo logout' and then 'apolo login'."
                in error_message
            ):
                url = self._test_config.cli_login_url
                await self._apolo_cli.config.login_with_token(
                    self._apolo_cli.config.current_token, url
                )
            else:
                raise AssertionError(error_message)

    @async_step("Add new project via apolo CLI")
    async def cli_add_new_project(
        self,
        org_name: str,
        proj_name: str,
        default_role: str = "reader",
        default_proj: bool = False,
    ) -> None:
        result, error_message = await self._apolo_cli.admin.create_project(
            org_name=org_name,
            proj_name=proj_name,
            default_role=default_role,
            default_proj=default_proj,
        )
        assert result, error_message

    @async_step("Run admin get-projects via CLI")
    async def cli_run_get_projects(self, org_name: str) -> None:
        result, error_message = await self._apolo_cli.admin.get_projects(
            org_name=org_name
        )
        assert result, error_message

    @async_step("Add organization member to project via CLI")
    async def cli_add_org_member_to_project(
        self,
        org_name: str,
        proj_name: str,
        username: str,
        role: str,
        cluster: str = "default",
    ) -> None:
        result, error_message = await self._apolo_cli.admin.add_proj_user(
            org_name=org_name,
            proj_name=proj_name,
            username=username,
            role=role,
            cluster=cluster,
        )
        assert result, error_message

    @async_step("Add user not in organization to project via CLI")
    async def cli_add_user_not_in_org_to_project(
        self,
        org_name: str,
        proj_name: str,
        username: str,
        role: str,
        cluster: str = "default",
    ) -> None:
        result, error_message = await self._apolo_cli.admin.add_proj_user(
            org_name=org_name,
            proj_name=proj_name,
            username=username,
            role=role,
            cluster=cluster,
        )
        expected_error = (
            f"ERROR: User '{org_name}/{username}' not found in cluster '{cluster}'"
        )
        assert not result, f"Command should fail with: {expected_error}"
        assert error_message == expected_error, (
            f"Expected: \n{expected_error} \nbut got \n{error_message}"
        )

    @async_step("Get project users via CLI")
    async def cli_get_proj_users(self, org_name: str, proj_name: str) -> None:
        result, error_message = await self._apolo_cli.admin.get_proj_users(
            org_name=org_name, proj_name=proj_name
        )
        assert result, error_message

    @async_step("Verify user present in get-project-users output via CLI")
    async def verify_cli_user_in_proj_users_output(
        self, username: str, role: str, email: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.admin.verify_user_in_proj_users_output(
            username=username, role=role, email=email
        )
        assert result, error_message

    @async_step("Verify user is not present in get-project-users output via CLI")
    async def verify_cli_user_not_in_proj_users_output(
        self, username: str, role: str, email: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.admin.verify_user_in_proj_users_output(
            username=username, role=role, email=email
        )
        assert not result, (
            f"User '{username}' should not be listed in get-project-users output"
        )

    @async_step("Remove user from project via CLI")
    async def cli_remove_user_from_proj(
        self, org_name: str, proj_name: str, username: str, expected_error: str = ""
    ) -> None:
        result, error_message = await self._apolo_cli.admin.remove_proj_user(
            org_name=org_name, proj_name=proj_name, username=username
        )
        if expected_error:
            assert not result, f"Command should fail with: {expected_error}"
            assert error_message == expected_error, (
                f" Expected: {expected_error}, got: {error_message}"
            )
        else:
            assert result, error_message

    @async_step("Update user role on a project via CLI")
    async def cli_update_proj_user_role(
        self,
        org_name: str,
        proj_name: str,
        username: str,
        role: str,
        expected_error: str = "",
    ) -> None:
        result, error_message = await self._apolo_cli.admin.update_proj_user(
            org_name=org_name, proj_name=proj_name, username=username, role=role
        )
        if expected_error:
            assert not result, f"Command should fail with: {expected_error}"
            assert error_message == expected_error, (
                f" Expected: {expected_error}, got: {error_message}"
            )
        else:
            assert result, error_message

    @async_step("Verify admin get-projects output via CLI")
    async def verify_cli_admin_get_projects_output(
        self, org_name: str, proj_name: str, default_role: str, default_proj: bool
    ) -> None:
        resut, error_message = await self._apolo_cli.admin.verify_get_projects_output(
            org_name=org_name,
            proj_name=proj_name,
            default_role=default_role,
            default_proj=default_proj,
        )
        assert resut, error_message

    @async_step("Add user to project via CLI")
    async def cli_add_user_to_project(
        self, org_name: str, proj_name: str, username: str, role: str
    ) -> None:
        await self._apolo_cli.admin.add_proj_user(
            org_name=org_name, proj_name=proj_name, username=username, role=role
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

        assert org.org_name in self._apolo_cli.admin.parsed_get_orgs_output, (
            f"Organization '{org.org_name}' (for gherkin_name '{gherkin_name}') "
            f"not found in CLI output: {self._apolo_cli.admin.parsed_get_orgs_output}"
        )

    @async_step("Remove organization via CLI")
    async def cli_remove_org(self, gherkin_name: str) -> None:
        org = self._data_manager.get_organization_by_gherkin_name(gherkin_name)
        org_name = org.org_name
        result, error_message = await self._apolo_cli.admin.remove_organization(
            org_name=org_name
        )
        assert result, error_message

    @async_step("Add user to organization via CLI")
    async def cli_add_user_to_org(
        self, org_name: str, username: str, role: str = "user"
    ) -> None:
        result, error_message = await self._apolo_cli.admin.add_user_to_org(
            org_name=org_name, username=username, role=role.lower()
        )
        assert result, error_message

    @async_step("Remove user from organization via CLI")
    async def cli_remove_user_from_org(
        self, org_name: str, username: str, expected_error: str = ""
    ) -> None:
        result, error_message = await self._apolo_cli.admin.remove_user_from_org(
            org_name=org_name, username=username
        )
        if expected_error:
            assert not result, f"Command should fail with: {expected_error}"
            assert error_message == expected_error, (
                f"Expected: \n{expected_error} \nbut got \n{error_message}"
            )
        else:
            assert result, error_message

    @async_step("Get organization users via CLI")
    async def cli_get_org_users(self, org_name: str) -> None:
        result, error_message = await self._apolo_cli.admin.get_org_users(
            org_name=org_name
        )
        assert result, error_message

    @async_step("Verify user is present in get-org-users command output")
    async def verify_cli_user_in_orgs_users_output(
        self, username: str, role: str, email: str, credits: str | float | int
    ) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.admin.verify_user_in_org_users_output(
            username=username, role=role, email=email, credits=credits
        )
        assert result, error_message

    @async_step("Verify user is not present in get-org-users command output")
    async def verify_cli_user_not_in_orgs_users_output(
        self, username: str, role: str, email: str, credits: str | float | int
    ) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.admin.verify_user_in_org_users_output(
            username=username, role=role, email=email, credits=credits
        )
        assert not result, f"{username} should not be present in get-org-users output"

    @async_step("Set organization credits via CLI")
    async def cli_set_org_default_credits(
        self, org_name: str, credits_amount: int
    ) -> None:
        result, error_message = await self._apolo_cli.admin.set_org_default_credits(
            org_name=org_name, credits_amount=credits_amount
        )
        assert result, error_message
