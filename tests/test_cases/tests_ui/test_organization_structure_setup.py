import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.test_cases.steps.ui_steps.ui_organization_structure_setup_steps import (
    UIOrganizationStructureSetupSteps,
)
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Organization Structure Setup")
class TestUIOrganizationStructureSetup(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps, ui_common_steps = await self.init_test_steps(
            UIOrganizationStructureSetupSteps
        )
        self._steps: UIOrganizationStructureSetupSteps = steps
        self._ui_common_steps: UICommonSteps = ui_common_steps
        # Login via UI
        self._user = self._users_manager.default_user

    @async_title("Create First Organization via UI")
    async def test_create_first_organization_via_ui(self) -> None:
        user = self._user
        steps = self._steps
        await self._ui_common_steps.ui_login(user.email, user.password)
        await steps.ui_click_welcome_lets_do_it_button()
        await steps.verify_ui_join_organization_page_displayed(user.username)
        await steps.ui_click_create_organization_button()
        await steps.verify_ui_name_organization_page_displayed()
        await steps.ui_enter_organization_name("My-organization")
        await steps.ui_click_next_button()
        await steps.verify_ui_thats_it_page_displayed()
        await steps.ui_click_thats_it_lets_do_it_button()
        await steps.verify_ui_main_page_displayed()
        await steps.verify_ui_create_project_message_displayed("My-organization")
        await steps.verify_ui_create_project_button_displayed()

    @async_title("Invite registered user without organization to organization via UI")
    async def test_invite_registered_user_without_org_via_ui(self) -> None:
        user = self._user
        ui_common_steps = self._ui_common_steps
        add_steps, add_ui_common_steps = await self.init_test_steps(
            UIOrganizationStructureSetupSteps
        )
        add_user = await add_ui_common_steps.ui_signup_new_user_ver_link()

        await ui_common_steps.ui_pass_new_user_onboarding(
            email=user.email,
            password=user.password,
            gherkin_name="Default-organization",
        )
        await ui_common_steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=add_user.email
        )

        await add_steps.ui_click_welcome_lets_do_it_button()
        await add_ui_common_steps.reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await add_steps.verify_ui_invite_to_org_page_displayed(org.org_name, "user")
        await add_steps.ui_click_accept_and_go_button()
        await add_steps.verify_ui_create_project_message_displayed(org.gherkin_name)
        await add_steps.verify_ui_create_project_button_displayed()

    @async_title("Invite user with organization to organization via UI")
    async def test_invite_registered_user_without_org_via_ui(self) -> None:
        user = self._user
        ui_common_steps = self._ui_common_steps
        add_steps, add_ui_common_steps = await self.init_test_steps(
            UIOrganizationStructureSetupSteps
        )
        add_user = await add_ui_common_steps.ui_signup_new_user_ver_link()

        await ui_common_steps.ui_pass_new_user_onboarding(
            email=user.email,
            password=user.password,
            gherkin_name="Default-organization",
        )
        await ui_common_steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=add_user.email
        )

        await add_steps.ui_click_welcome_lets_do_it_button()
        await add_ui_common_steps.reload_page()

