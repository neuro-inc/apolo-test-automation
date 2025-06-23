from __future__ import annotations

from collections.abc import Callable
from collections.abc import Awaitable

import pytest
from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.components.ui.page_manager import PageManager
from tests.test_cases.steps.ui_steps.ui_signup_steps import UISignupSteps
from tests.utils.api_helper import APIHelper
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager


@async_suite("UI Signup")
class TestUISignup:
    @pytest.fixture(autouse=True)
    async def setup(
        self,
        page_manager: PageManager,
        add_page_manager: Callable[[], Awaitable[PageManager]],
        data_manager: DataManager,
        test_config: ConfigManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._pm = page_manager
        self._add_pm = await add_page_manager()
        self._data_manager = data_manager
        self._test_config = test_config
        self._users_manager = users_manager
        self._api_helper = api_helper
        self.ui_common_steps = UICommonSteps(
            self._pm,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )
        self.steps = UISignupSteps(
            self._pm,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )
        self.add_steps = UISignupSteps(
            self._add_pm,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )

    @async_title("New user successful signup")
    async def test_new_user_signup(self) -> None:
        user = self._users_manager.generate_user()
        steps = self.steps
        await steps.ui_click_signup_button()
        await steps.ui_enter_email(user.email)
        await steps.ui_enter_password(user.password)
        await steps.ui_click_continue_button()
        await steps.verify_ui_email_message_displayed()

        await steps.activate_email_verification_link(user.email)
        await steps.ui_open_product_base_page()
        await steps.verify_ui_auth_page_displayed()

        await steps.ui_click_login_button()
        await steps.verify_ui_signup_username_page_displayed()

        await steps.ui_enter_username(user.username)
        await steps.ui_usr_click_signup_button()
        await steps.verify_ui_terms_of_agreement_displayed()

        await steps.ui_check_agreement_checkbox()
        await steps.ui_click_i_agree_button()
        await steps.verify_ui_welcome_page_displayed(user.email)

    @async_title("Invite not registered user as user to organization")
    async def test_invite_not_registered_user_to_org(self) -> None:
        steps = self.steps
        add_steps = self.add_steps
        main_user = self._users_manager.default_user
        add_user = self._users_manager.generate_user()

        await self.ui_common_steps.ui_pass_new_user_onboarding(
            main_user.email, main_user.password, "default_organization"
        )
        organization = self._data_manager.default_organization
        await steps.ui_click_organization_settings_button(main_user.email)
        await steps.verify_ui_org_settings_popup_displayed(
            main_user.email, main_user.username
        )

        await steps.ui_click_people_button()
        await steps.verify_ui_org_people_page_displayed()

        await steps.ui_click_invite_people_button()
        await steps.verify_ui_invite_member_popup_displayed()

        await steps.ui_enter_invite_email(add_user.email)
        await steps.ui_select_user_role()
        await steps.verify_ui_invite_user_button_displayed(add_user.email)
        await steps.verify_ui_send_invite_button_disabled()

        await steps.ui_click_invite_user_button(add_user.email)
        await steps.verify_ui_send_invite_button_enabled()

        await steps.ui_click_send_invite_button()
        await steps.verify_ui_user_displayed_in_users_list(add_user.email)
        await steps.verify_ui_valid_user_role_displayed(add_user.email, "user")
        await steps.verify_ui_valid_user_status_displayed(add_user.email, "Invited")

        await add_steps.ui_click_signup_button()
        await add_steps.ui_enter_email(add_user.email)
        await add_steps.ui_enter_password(add_user.password)
        await add_steps.ui_click_continue_button()
        await add_steps.activate_email_verification_link(add_user.email)
        await add_steps.ui_open_product_base_page()
        await add_steps.verify_ui_auth_page_displayed()

        await add_steps.ui_click_login_button()
        await add_steps.verify_ui_signup_username_page_displayed()

        await add_steps.ui_enter_username(add_user.username)
        await add_steps.ui_usr_click_signup_button()
        await add_steps.verify_ui_terms_of_agreement_displayed()

        await add_steps.ui_check_agreement_checkbox()
        await add_steps.ui_click_i_agree_button()
        await add_steps.verify_ui_welcome_page_displayed(add_user.email)

        await add_steps.ui_click_welcome_lets_do_it_button()
        await add_steps.verify_ui_invite_to_org_page_displayed(
            organization.org_name, "user"
        )

        await add_steps.ui_click_accept_and_go_button()
        await add_steps.verify_ui_create_project_message_displayed(
            organization.gherkin_name
        )
        await add_steps.verify_ui_create_project_button_displayed()
