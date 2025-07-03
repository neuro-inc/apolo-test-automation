import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Organization Structure Setup")
class TestUIOrganizationStructureSetup(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps
        self._user = self._users_manager.default_user

    @async_title("Create First Organization via UI")
    async def test_create_first_organization_via_ui(self) -> None:
        user = self._user
        steps = self._steps
        await steps.ui_login(user.email, user.password)
        await steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await steps.join_org_page.verify_ui_page_displayed(user.username)
        await steps.join_org_page.ui_click_create_organization_button()
        await steps.name_org_page.verify_ui_page_displayed()
        org = self._data_manager.add_organization("My-organization")
        await steps.name_org_page.ui_enter_organization_name(org.org_name)
        await steps.name_org_page.ui_click_next_button()
        await steps.thats_it_page.verify_ui_page_displayed()
        await steps.thats_it_page.ui_click_lets_do_it_button()
        await steps.main_page.verify_ui_page_displayed()
        await steps.main_page.verify_ui_create_project_message_displayed(org.org_name)
        await steps.main_page.verify_ui_create_project_button_displayed()

    @async_title("Invite registered user without organization to organization via UI")
    async def test_invite_registered_user_without_org_via_ui(self) -> None:
        user = self._user
        steps = self._steps
        add_steps = await self.init_test_steps()
        add_user = await add_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
            gherkin_name="Default-organization",
        )
        await add_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=add_user.email
        )

        await add_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await add_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await add_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await add_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        await add_steps.main_page.verify_ui_create_project_button_displayed()

    @async_title(
        "Invite registered user without organization to organization with default project via UI"
    )
    async def test_invite_registered_user_without_org_default_proj_via_ui(self) -> None:
        user = self._user
        steps = self._steps
        add_steps = await self.init_test_steps()
        add_user = await add_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
            gherkin_name="Default-organization",
        )
        org = self._data_manager.default_organization
        proj = org.add_project("First-project")
        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="Reader",
            make_default=True,
        )

        await add_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=add_user.email
        )

        await add_steps.ui_reload_page()

        await add_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await add_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await add_steps.apps_page.verify_ui_page_displayed()

    @async_title("Invite user with organization to organization via UI")
    async def test_invite_registered_user_with_org_via_ui(self) -> None:
        user = self._user
        steps = self._steps
        add_steps = await self.init_test_steps()
        self.log("User1 login")
        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        self.log("User1 pass new user onboarding and create organization")
        await steps.ui_pass_new_user_onboarding(
            gherkin_name="Default-organization",
        )

        self.log("User2 Login")
        add_user = await add_steps.ui_signup_new_user_ver_link()
        self.log("User2 password new user onboarding and create organization")
        await add_steps.ui_pass_new_user_onboarding(gherkin_name="new-organization")

        self.log("User1 invite User2 to organization")
        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=add_user.email
        )

        self.log("User2 reload page")
        await add_steps.ui_reload_page()
        org = self._data_manager.get_organization_by_gherkin_name(
            gherkin_name="Default-organization"
        )
        self.log("User2 verify that invite to organization button displayed")
        await add_steps.main_page.verify_ui_invite_to_org_displayed(
            org_name=org.org_name
        )
        self.log("User2 click invite to organization button")
        await add_steps.main_page.ui_click_invite_to_org_button(org_name=org.org_name)

        self.log("User2 verify that invite row displayed on the main page")
        await add_steps.main_page.verify_ui_invite_org_info_displayed(
            org_name=org.org_name
        )
        self.log("User2 verify that user role is valid")
        await add_steps.main_page.verify_ui_invite_to_org_role_is_valid(
            org_name=org.org_name, role="user"
        )
        self.log("User2 click accept button")
        await add_steps.main_page.ui_click_accept_invite_to_org(org_name=org.org_name)

        self.log("User2 click organization settings button")
        await add_steps.main_page.ui_click_organization_settings_button(
            email=add_user.email
        )
        self.log("User2 verify that second organization displayed")
        await add_steps.org_settings_popup.verify_ui_select_org_button_displayed(
            org_name=org.org_name
        )
