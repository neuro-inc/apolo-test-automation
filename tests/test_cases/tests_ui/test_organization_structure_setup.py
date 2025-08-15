import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Organization Structure Setup", parent="UI Tests")
class TestUIOrganizationStructureSetup(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Create First Organization via UI")
    async def test_create_first_organization_via_ui(self) -> None:
        """
        -Login with valid credentials.
        Verify that:
            User can create first organization during onboarding.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
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

    @async_title("Create Second Organization via UI")
    async def test_create_second_organization_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        Verify that:
            User can create second organization.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org2 = self._data_manager.add_organization(gherkin_name="Second-organization")

        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_click_create_new_org_btn()
        await steps.create_org_popup.verify_ui_popup_displayed()

        await steps.create_org_popup.ui_enter_org_name(org2.org_name)
        await steps.create_org_popup.ui_click_create_button()
        await steps.create_org_popup.ui_wait_to_disappear()

        await steps.main_page.verify_ui_create_project_message_displayed(
            org_name=org2.org_name
        )
        await steps.main_page.verify_ui_create_project_button_displayed()

    @async_title("Switch between organization via UI")
    async def test_switch_org_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create second organization via UI.
        Verify that:
            User can switch between organizations.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        org2 = self._data_manager.add_organization(gherkin_name="Second-organization")
        proj = org.add_project("First-project")
        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="Reader",
            make_default=True,
        )

        await steps.ui_create_add_org(email=user.email, org_name=org2.org_name)

        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_select_org(org_name=org.org_name)
        await steps.apps_page.verify_ui_page_displayed()

        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_select_org(org_name=org2.org_name)
        await steps.main_page.verify_ui_create_project_message_displayed(
            org_name=org2.org_name
        )
        await steps.main_page.verify_ui_create_project_button_displayed()

    @async_title("Set default organization credits via UI")
    async def test_set_default_credits_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        Verify that:
            User can set default organization credits.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization

        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_click_settings_btn()
        await steps.org_settings_page.verify_ui_page_displayed()

        await steps.org_settings_page.ui_enter_credits_amount(value="126")
        await steps.org_settings_page.ui_click_save_button()

        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        await u2_steps.ui_reload_page()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_click_people_button()
        await steps.org_people_page.verify_ui_valid_user_credits_displayed(
            email=second_user.email, credits="126"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_valid_user_credits_displayed(
            email=second_user.email, credits="126"
        )

    @async_title("Search Member of organization via UI")
    async def test_search_org_member_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization via API.
        -Signup third user.
        -Invite third user to organization via API.
        Verify that:
            User can search organization members using Search field.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)
        u3_steps = await self.init_ui_test_steps()
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization

        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_click_settings_btn()
        await steps.org_settings_page.verify_ui_page_displayed()

        await steps.org_settings_page.ui_enter_credits_amount(value="126")
        await steps.org_settings_page.ui_click_save_button()

        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )
        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=third_user.email
        )

        await u2_steps.ui_reload_page()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u3_steps.ui_reload_page()
        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.main_page.ui_click_organization_settings_button(email=user.email)
        await steps.org_settings_popup.ui_click_people_button()
        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            email=second_user.email
        )
        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            email=third_user.email
        )

        await steps.org_people_page.ui_enter_search_input_value(second_user.email)
        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            email=second_user.email
        )
        await steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=third_user.email
        )

        await steps.org_people_page.ui_enter_search_input_value(third_user.email)
        await steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=second_user.email
        )
        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            email=third_user.email
        )

    @async_title("Invite registered user without organization to organization via UI")
    async def test_invite_registered_user_without_org_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        Verify that:
            User can invite to organization another user that is registered but doesn't have an organization.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        await u2_steps.main_page.verify_ui_create_project_button_displayed()

    @async_title(
        "Invite registered user without organization to organization with default project via UI"
    )
    async def test_invite_registered_user_without_org_default_proj_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project with 'default' option.
        -Signup second user.
        Verify that:
            - User can invite to organization another user that is registered but doesn't have organization.
            - Newly invited user is member of the default project.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.default_organization
        proj = org.add_project("First-project")
        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="Reader",
            make_default=True,
        )

        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        await u2_steps.ui_reload_page()

        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.apps_page.verify_ui_page_displayed()

    @async_title("Invite user with organization to organization via UI")
    async def test_invite_registered_user_with_org_via_ui(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Pass onboarding for second user and create organization via UI.
        Verify that:
            - User can invite to organization another user that already has organization.'
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()

        self.log("User1 pass new user onboarding and create organization")
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        self.log("User2 Login")
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        self.log("User2 password new user onboarding and create organization")
        await u2_steps.ui_pass_new_user_onboarding(
            user=second_user,
            gherkin_name="new-organization",
        )

        self.log("User1 invite User2 to organization")
        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        self.log("User2 reload page")
        await u2_steps.ui_reload_page()
        org = self._data_manager.get_organization_by_gherkin_name(
            gherkin_name="Default-organization"
        )
        self.log("User2 verify that invite to organization button displayed")
        await u2_steps.main_page.verify_ui_invite_to_org_displayed(
            org_name=org.org_name
        )
        self.log("User2 click invite to organization button")
        await u2_steps.main_page.ui_click_invite_to_org_button(org_name=org.org_name)

        self.log("User2 verify that invite row displayed on the main page")
        await u2_steps.main_page.verify_ui_invite_org_info_displayed(
            org_name=org.org_name
        )
        self.log("User2 verify that user role is valid")
        await u2_steps.main_page.verify_ui_invite_to_org_role_is_valid(
            org_name=org.org_name, role="user"
        )
        self.log("User2 click accept button")
        await u2_steps.main_page.ui_click_accept_invite_to_org(org_name=org.org_name)

        self.log("User2 click organization settings button")
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        self.log("User2 verify that second organization displayed")
        await u2_steps.org_settings_popup.verify_ui_select_org_button_displayed(
            org_name=org.org_name
        )
