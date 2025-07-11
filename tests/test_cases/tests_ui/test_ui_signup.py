from __future__ import annotations


import pytest
from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Signup", parent="UI Tests")
class TestUISignup(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("New user successful signup")
    async def test_new_user_signup(self) -> None:
        user = self._users_manager.generate_user()
        steps = self._steps
        await steps.auth_page.ui_click_signup_button()
        await steps.signup_page.ui_enter_email(user.email)
        await steps.signup_page.ui_enter_password(user.password)
        await steps.signup_page.ui_click_continue_button()
        await steps.main_page.verify_ui_email_message_displayed()

        await steps.activate_email_verification_link(user.email)
        await steps.ui_open_product_base_page()
        await steps.auth_page.verify_ui_page_displayed()

        await steps.auth_page.ui_click_login_button()
        await steps.signup_username_page.verify_ui_page_displayed()

        await steps.signup_username_page.ui_enter_username(user.username)
        await steps.signup_username_page.ui_click_signup_button()
        await steps.main_page.verify_ui_terms_of_agreement_displayed()

        await steps.main_page.ui_check_agreement_checkbox()
        await steps.main_page.ui_click_i_agree_button()
        await steps.welcome_new_user_page.verify_ui_page_displayed(user.email)

    @async_title("Invite not registered user as user to organization")
    async def test_invite_not_registered_user_to_org(self) -> None:
        steps = self._steps
        u2_steps = await self.init_test_steps()
        user = await steps.ui_signup_new_user_ver_link()
        second_user = self._users_manager.generate_user()

        self.log("User1 login")
        await steps.ui_login(user.email, user.password)
        self.log("User1 pass onboarding and create organization")
        await steps.ui_pass_new_user_onboarding("default_organization")
        org = self._data_manager.get_organization_by_gherkin_name(
            gherkin_name="default_organization"
        )

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            second_user.email
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            second_user.email, "user"
        )
        await steps.org_people_page.verify_ui_valid_user_status_displayed(
            second_user.email, "Invited"
        )

        await u2_steps.auth_page.ui_click_signup_button()
        await u2_steps.signup_page.ui_enter_email(second_user.email)
        await u2_steps.signup_page.ui_enter_password(second_user.password)
        await u2_steps.signup_page.ui_click_continue_button()
        await u2_steps.activate_email_verification_link(second_user.email)
        await u2_steps.ui_open_product_base_page()
        await u2_steps.auth_page.verify_ui_page_displayed()

        await u2_steps.auth_page.ui_click_login_button()
        await u2_steps.signup_username_page.verify_ui_page_displayed()

        await u2_steps.signup_username_page.ui_enter_username(second_user.username)
        await u2_steps.signup_username_page.ui_click_signup_button()
        await u2_steps.main_page.verify_ui_terms_of_agreement_displayed()

        await u2_steps.main_page.ui_check_agreement_checkbox()
        await u2_steps.main_page.ui_click_i_agree_button()
        await u2_steps.welcome_new_user_page.verify_ui_page_displayed(second_user.email)

        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )

        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        await u2_steps.main_page.verify_ui_create_project_button_displayed()

    @async_title(
        "Invite not registered user to organization with default project via UI"
    )
    async def test_invite_not_registered_user_to_org_with_default_proj(self) -> None:
        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = self._users_manager.generate_user()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
            gherkin_name="Default-organization",
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            gherkin_name="Default-organization"
        )
        proj = org.add_project("First-project")
        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="Reader",
            make_default=True,
        )

        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        await u2_steps.auth_page.ui_click_signup_button()
        await u2_steps.signup_page.ui_enter_email(second_user.email)
        await u2_steps.signup_page.ui_enter_password(second_user.password)
        await u2_steps.signup_page.ui_click_continue_button()
        await u2_steps.activate_email_verification_link(second_user.email)
        await u2_steps.ui_open_product_base_page()
        await u2_steps.auth_page.verify_ui_page_displayed()

        await u2_steps.auth_page.ui_click_login_button()
        await u2_steps.signup_username_page.verify_ui_page_displayed()

        await u2_steps.signup_username_page.ui_enter_username(second_user.username)
        await u2_steps.signup_username_page.ui_click_signup_button()
        await u2_steps.main_page.verify_ui_terms_of_agreement_displayed()

        await u2_steps.main_page.ui_check_agreement_checkbox()
        await u2_steps.main_page.ui_click_i_agree_button()
        await u2_steps.welcome_new_user_page.verify_ui_page_displayed(second_user.email)

        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )

        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.apps_page.verify_ui_page_displayed()
