import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Secrets", parent="UI Tests")
class TestUISecrets(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Create First Secret without project via UI")
    async def test_create_first_secret_no_project_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.

        ### Verify that:

        - User **cannot** create first Secret if **no project created** yet.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        await steps.main_page.ui_click_secrets_btn()
        await steps.secrets_page.verify_ui_page_not_displayed()
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.main_page.verify_ui_create_project_message_displayed(
            org_name=org.org_name
        )

    @async_title("Create First Secret via UI")
    async def test_create_first_secret_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.

        ### Verify that:

        - User can create first Secret after project created.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_secret(
            secret_name="Secret_Key", secret_value="Secret_Value"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )

    @async_title("Create Second Secret via UI")
    async def test_create_second_secret_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create Secret.

        ### Verify that:

        - User can create second Secret.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_secret(
            secret_name="Secret_Key", secret_value="Secret_Value"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )

        await steps.ui_create_secret(
            secret_name="New_Key", secret_value="Secret_Value", first_secret=False
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(secret_name="New_Key")

    @async_title("Search Secret via UI")
    async def test_search_secret_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create Secret.

        ### Verify that:

        - User can Search for secret via UI.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_secret(
            secret_name="Secret_Key", secret_value="Secret_Value"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )

        await steps.ui_create_secret(
            secret_name="New_Key", secret_value="Secret_Value", first_secret=False
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(secret_name="New_Key")

        await steps.secrets_page.ui_enter_secret_name_into_search_input(
            secret_name="Secret_Key"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )
        await steps.secrets_page.verify_ui_secret_row_not_displayed(
            secret_name="New_Key"
        )

    @async_title("Delete Secret via UI")
    async def test_delete_secret_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create Secret.

        ### Verify that:

        - User can delete Secret.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_secret(
            secret_name="Secret_Key", secret_value="Secret_Value"
        )
        await steps.secrets_page.verify_ui_secret_row_displayed(
            secret_name="Secret_Key"
        )

        await steps.secrets_page.ui_click_delete_secret_btn(secret_name="Secret_Key")
        await steps.delete_secret_popup.verify_ui_popup_displayed(
            secret_name="Secret_Key"
        )

        await steps.delete_secret_popup.ui_click_delete_btn()
        await steps.delete_secret_popup.ui_wait_to_disappear(secret_name="Secret_Key")
        await steps.secrets_page.verify_ui_secret_row_not_displayed(
            secret_name="Secret_Key"
        )
        await steps.secrets_page.verify_ui_no_secrets_message_displayed()
