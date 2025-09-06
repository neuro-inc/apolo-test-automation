import pytest

from tests.reporting_hooks.reporting import async_suite, async_title

from tests.test_cases.base_test_class import BaseTestClass


@async_suite("CLI Secrets", parent="CLI Tests")
class TestCLISecrets(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_cli_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("Admin create secret with no project created via CLI")
    async def test_admin_create_secret_no_proj_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Login with Bearer auth token via **CLI**.

        ### Verify that:

        - User **cannot** create secret if there is no project created via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)

        expected_error = "ERROR: The current project is not selected. Please create one with 'apolo admin add-project', or switch to the existing one with 'apolo config switch-project'."
        await self._cli_steps.secret.cli_create_secret(
            secret_name="My-secret",
            secret_value="Secret value",
            expected_error=expected_error,
        )

    @async_title("Admin create first secret via CLI")
    async def test_admin_create_first_secret_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Login with Bearer auth token via **CLI**.
        - Create new project via **CLI**.

        ### Verify that:

        - User can create first secret via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.secret.cli_create_secret(
            secret_name="My-secret", secret_value="Secret value"
        )
        await self._cli_steps.secret.cli_list_secrets()
        await self._cli_steps.secret.verify_secret_listed(
            secret_name="My-secret", org_name=org.org_name, proj_name=proj.project_name
        )

    @async_title("Admin create second secret via CLI")
    async def test_admin_create_second_secret_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Login with Bearer auth token via **CLI**.
        - Create new project via **CLI**.
        - Create first secret via **CLI**.

        ### Verify that:

        - User can create second secret via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.secret.cli_create_secret(
            secret_name="My-secret", secret_value="Secret value"
        )
        await self._cli_steps.secret.cli_create_secret(
            secret_name="Second-secret", secret_value="Secret value"
        )
        await self._cli_steps.secret.cli_list_secrets()
        await self._cli_steps.secret.verify_secret_listed(
            secret_name="My-secret", org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.secret.verify_secret_listed(
            secret_name="Second-secret",
            org_name=org.org_name,
            proj_name=proj.project_name,
        )

    @async_title("Admin remove secret via CLI")
    async def test_admin_remove_secret_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Login with Bearer auth token via **CLI**.
        - Create new project via **CLI**.
        - Create first secret via **CLI**.
        - Create second secret via **CLI**.

        ### Verify that:

        - User can remove second secret via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.secret.cli_create_secret(
            secret_name="My-secret", secret_value="Secret value"
        )
        await self._cli_steps.secret.cli_create_secret(
            secret_name="Second-secret", secret_value="Secret value"
        )
        await self._cli_steps.secret.cli_list_secrets()
        await self._cli_steps.secret.verify_secret_listed(
            secret_name="My-secret", org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.secret.verify_secret_listed(
            secret_name="Second-secret",
            org_name=org.org_name,
            proj_name=proj.project_name,
        )

        await self._cli_steps.secret.cli_remove_secret(secret_name="My-secret")
        await self._cli_steps.secret.cli_list_secrets()
        await self._cli_steps.secret.verify_secret_not_listed(
            secret_name="My-secret", org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.secret.verify_secret_listed(
            secret_name="Second-secret",
            org_name=org.org_name,
            proj_name=proj.project_name,
        )
