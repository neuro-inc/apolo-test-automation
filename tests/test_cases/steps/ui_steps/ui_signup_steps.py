from tests.reporting_hooks.reporting import async_step
from tests.utils.api_helper import APIHelper
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager


class UISignupSteps:
    def __init__(
        self,
        page_manager: PageManager,
        test_config: ConfigManager,
        data_manager: DataManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        self._pm = page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper

    # ********************   Auth page steps   ****************************
    @async_step("Click signup button")
    async def ui_click_signup_button(self) -> None:
        await self._pm.auth_page.click_sign_up_button()

    @async_step("Verify that Auth page displayed")
    async def verify_ui_auth_page_displayed(self) -> None:
        assert await self._pm.auth_page.is_loaded(), "Auth page should be displayed!"

    @async_step("Click login button")
    async def ui_click_login_button(self) -> None:
        await self._pm.auth_page.click_log_in_button()

    # ********************   Signup page steps   ****************************
    @async_step("Enter email")
    async def ui_enter_email(self, email: str) -> None:
        await self._pm.signup_page.enter_email(email)

    @async_step("Enter password")
    async def ui_enter_password(self, password: str) -> None:
        await self._pm.signup_page.enter_password(password)

    @async_step("Click continue button")
    async def ui_click_continue_button(self) -> None:
        await self._pm.signup_page.click_continue_button()

    # ********************   Main page steps   ****************************

    @async_step("Verify that Verify email message displayed")
    async def verify_ui_email_message_displayed(self) -> None:
        assert await self._pm.main_page.is_verify_email_message_displayed(), (
            "Verify email message should be displayed!"
        )

    @async_step("Verify that User agreement pop up displayed")
    async def verify_ui_terms_of_agreement_displayed(self) -> None:
        assert await self._pm.main_page.is_user_agreement_title_displayed(), (
            "User agreement popup should be displayed!"
        )

    @async_step("Check agreement checkbox")
    async def ui_check_agreement_checkbox(self) -> None:
        await self._pm.main_page.check_user_agreement_checkbox()

    @async_step("Click I Agree button")
    async def ui_click_i_agree_button(self) -> None:
        await self._pm.main_page.click_user_agreement_agree_button()

    @async_step("Click User Organization settings button")
    async def ui_click_organization_settings_button(self, email: str) -> None:
        await self._pm.main_page.click_organization_settings_button(email)

    @async_step("Verify project creation message is displayed")
    async def verify_ui_create_project_message_displayed(
        self, gherkin_name: str
    ) -> None:
        organization = self._data_manager.get_organization_by_gherkin_name(gherkin_name)
        assert organization, f"Organization {gherkin_name} not found"
        page = self._pm.main_page
        assert await page.is_create_first_project_text_field_displayed(
            organization.org_name
        ), f"Organization {gherkin_name} does not have a project creation message"

    @async_step("Verify create project button displayed")
    async def verify_ui_create_project_button_displayed(self) -> None:
        assert await self._pm.main_page.is_create_first_project_button_displayed(), (
            "Create project button should be displayed!"
        )

    # ********************   Welcome new user page steps   ****************************

    @async_step("Verify that Welcome new user page displayed")
    async def verify_ui_welcome_page_displayed(self, email: str) -> None:
        assert await self._pm.welcome_new_user_page.is_loaded(email=email), (
            "Welcome new user page should be displayed!"
        )

    @async_step("Click the let's do it button on Welcome page")
    async def ui_click_welcome_lets_do_it_button(self) -> None:
        await self._pm.welcome_new_user_page.click_lets_do_it_button()

    # ********************   invited to organization page steps   ****************************

    @async_step("Verify that Invited to organization page displayed")
    async def verify_ui_invite_to_org_page_displayed(
        self, org_name: str, user_role: str
    ) -> None:
        assert await self._pm.invited_to_org_page.is_loaded(
            org_name=org_name, user_role=user_role
        ), "Invited to organization page should be displayed!"

    @async_step("Click Accept and Go button")
    async def ui_click_accept_and_go_button(self) -> None:
        await self._pm.invited_to_org_page.click_accept_and_go_button()

    # ********************   Signup username page steps   ****************************

    @async_step("Verify that Signup username page displayed")
    async def verify_ui_signup_username_page_displayed(self) -> None:
        assert await self._pm.signup_username_page.is_loaded(), (
            "Signup username page should be displayed!"
        )

    @async_step("Enter username")
    async def ui_enter_username(self, username: str) -> None:
        await self._pm.signup_username_page.enter_username(username)

    @async_step("Click signup button on Signup username page")
    async def ui_usr_click_signup_button(self) -> None:
        await self._pm.signup_username_page.click_signup_button()

    # ********************   Organization settings popup steps   ****************************

    @async_step("Verify that Organization settings pop up displayed")
    async def verify_ui_org_settings_popup_displayed(
        self, email: str, username: str
    ) -> None:
        assert await self._pm.organization_settings_popup.is_loaded(
            email=email, username=username
        ), "Organization settings popup should be displayed!"

    @async_step("Click People button")
    async def ui_click_people_button(self) -> None:
        await self._pm.organization_settings_popup.click_people_button()

    # ********************   Organization people page steps   ****************************

    @async_step("Verify that Organization people page displayed")
    async def verify_ui_org_people_page_displayed(self) -> None:
        assert await self._pm.organization_people_page.is_loaded(), (
            "Organization people page should be displayed!"
        )

    @async_step("Click Invite people button")
    async def ui_click_invite_people_button(self) -> None:
        await self._pm.organization_people_page.click_invite_people_button()

    @async_step("Verify that invited user displayed in users list")
    async def verify_ui_user_displayed_in_users_list(self, email: str) -> None:
        assert await self._pm.organization_people_page.is_org_user_row_displayed(
            email
        ), "Invited user should be displayed in organization users list!"

    @async_step("Verify that invited user role is valid")
    async def verify_ui_valid_user_role_displayed(self, email: str, role: str) -> None:
        user_role = await self._pm.organization_people_page.get_org_user_role(email)
        assert user_role.lower() == role.lower(), f"Invited user role should be {role}!"

    @async_step("Verify that invited user status is valid")
    async def verify_ui_valid_user_status_displayed(
        self, email: str, status: str
    ) -> None:
        user_status = await self._pm.organization_people_page.get_org_user_status(email)
        assert status.lower() in user_status.lower(), (
            f"Invited user status should be {user_status}!"
        )

    # ********************   Invite member popup steps   ****************************

    @async_step("Verify that Invite member popup displayed")
    async def verify_ui_invite_member_popup_displayed(self) -> None:
        assert await self._pm.invite_member_popup.is_loaded(), (
            "Invite member popup should be displayed!"
        )

    @async_step("Enter email")
    async def ui_enter_invite_email(self, email: str) -> None:
        await self._pm.invite_member_popup.enter_user_data(email=email)

    @async_step("Select 'User' role")
    async def ui_select_user_role(self) -> None:
        await self._pm.invite_member_popup.select_user_role()

    @async_step("Verify that Invite user button appeared")
    async def verify_ui_invite_user_button_displayed(self, email: str) -> None:
        assert await self._pm.invite_member_popup.is_invite_user_displayed(
            email=email
        ), "Invite user button should be displayed!"

    @async_step("Click Invite user button")
    async def ui_click_invite_user_button(self, email: str) -> None:
        await self._pm.invite_member_popup.click_invite_user_button(email=email)

    @async_step("Verify that Send invite button disabled")
    async def verify_ui_send_invite_button_disabled(self) -> None:
        assert not await self._pm.invite_member_popup.is_send_invite_button_enabled(), (
            "Send invite button should be disabled!"
        )

    @async_step("Verify that Send invite button enabled")
    async def verify_ui_send_invite_button_enabled(self) -> None:
        assert await self._pm.invite_member_popup.is_send_invite_button_enabled(), (
            "Send invite button should be enabled!"
        )

    @async_step("Click Send invite button")
    async def ui_click_send_invite_button(self) -> None:
        await self._pm.invite_member_popup.click_send_invite_button()

    # ********************   Verification link steps   ****************************

    @async_step("Verify user email with the activation link")
    async def activate_email_verification_link(self, email: str) -> None:
        needs_verification, url = await self._api_helper.check_user_needs_verification(
            email
        )
        assert needs_verification, f"User {email} does not need verification!!!!"

        await self._pm.page.goto(url)

    @async_step("Open product base page")
    async def ui_open_product_base_page(self) -> None:
        base_url = self._test_config.base_url
        await self._pm.page.goto(base_url)
        await self._pm.page.wait_for_load_state("networkidle")

