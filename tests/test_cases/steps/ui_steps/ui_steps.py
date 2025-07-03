from tests.reporting_hooks.reporting import async_step
from tests.test_cases.steps.ui_steps.page_steps import PageSteps
from tests.utils.api_helper import APIHelper
from tests.utils.browser_helper import extract_access_token_from_local_storage
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager, UserData


class UISteps(PageSteps):
    def __init__(
        self,
        page_manager: PageManager,
        test_config: ConfigManager,
        data_manager: DataManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        super().__init__(page_manager, data_manager)
        self._pm = page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper

    @async_step("Reload page")
    async def ui_reload_page(self) -> None:
        await self._pm.page.reload()

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

    @async_step("Login via UI")
    async def ui_login(self, email: str, password: str, admin: bool = False) -> None:
        if admin:
            await self.auth_page.ui_click_login_button()
            await self._pm.login_page.login(email, password)
            await self.main_page.verify_ui_main_page_displayed()
            token = await extract_access_token_from_local_storage(
                self._pm.login_page.page
            )
            self._test_config.cleanup_token = token
        else:
            await self.auth_page.ui_click_login_button()
            await self._pm.login_page.login(email, password)
            await self.welcome_new_user_page.verify_ui_welcome_page_displayed(
                email=email
            )
            token = await extract_access_token_from_local_storage(
                self._pm.login_page.page
            )
            self._test_config.token = token

    # ********************   Onboarding steps   ****************************

    @async_step("Pass new user onboarding and create first organization via UI")
    async def ui_pass_new_user_onboarding(self, gherkin_name: str) -> None:
        token = await extract_access_token_from_local_storage(self._pm.login_page.page)
        self._test_config.token = token

        await self.welcome_new_user_page.ui_click_welcome_lets_do_it_button()
        await self.join_org_page.ui_click_create_organization_button()

        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        org_name = organization.org_name

        await self.name_org_page.ui_enter_organization_name(org_name)
        await self.name_org_page.ui_click_next_button()

        await self.thats_it_page.ui_click_thats_it_lets_do_it_button()

        await self.main_page.verify_ui_main_page_displayed()

    # ********************   New user signup steps   ****************************
    @async_step("Signup new user via UI and activate email verification link")
    async def ui_signup_new_user_ver_link(self) -> UserData:
        user = self._users_manager.generate_user()
        await self._pm.auth_page.click_sign_up_button()
        await self._pm.signup_page.enter_email(user.email)
        await self._pm.signup_page.enter_password(user.password)
        await self._pm.signup_page.click_continue_button()
        assert await self._pm.main_page.is_verify_email_message_displayed(), (
            "Verify email message is not displayed!!!"
        )

        needs_verification, url = await self._api_helper.check_user_needs_verification(
            user.email,
        )
        assert needs_verification, f"User {user.email} does not need verification!!!!"

        await self._pm.page.goto(url)

        (
            needs_verification,
            response,
        ) = await self._api_helper.check_user_needs_verification(
            user.email,
        )
        assert not needs_verification, f"User {user.email} still needs verification!!!!"
        assert response == "Email already verified", (
            f"User {user.email} still needs verification!!!!"
        )

        base_url = self._test_config.base_url
        await self._pm.page.goto(base_url)
        await self.auth_page.verify_ui_auth_page_displayed()

        await self.auth_page.ui_click_login_button()
        await self.signup_username_page.verify_ui_signup_username_page_displayed()

        await self.signup_username_page.ui_enter_username(user.username)
        await self.signup_username_page.ui_click_signup_button()
        await self.main_page.verify_ui_terms_of_agreement_displayed()

        await self.main_page.ui_check_agreement_checkbox()
        await self.main_page.ui_click_i_agree_button()
        await self.welcome_new_user_page.verify_ui_welcome_page_displayed(
            email=user.email
        )

        return user

    # ********************   invite user to organization steps   ****************************
    @async_step("Invite user to organization via UI")
    async def ui_invite_user_to_org(
        self, email: str, username: str, add_user_email: str
    ) -> None:
        await self.main_page.ui_click_organization_settings_button(email)
        await self.org_settings_popup.verify_ui_org_settings_popup_displayed(
            email=email, username=username
        )

        await self.org_settings_popup.ui_click_people_button()
        await self.org_people_page.verify_ui_org_people_page_displayed()

        await self.org_people_page.ui_click_invite_people_button()
        await self.invite_org_member_popup.verify_ui_invite_member_popup_displayed()

        await self.invite_org_member_popup.ui_enter_invite_email(email=add_user_email)
        await self.invite_org_member_popup.ui_select_user_role()
        await self.invite_org_member_popup.verify_ui_invite_user_button_displayed(
            email=add_user_email
        )

        await self.invite_org_member_popup.ui_click_invite_user_button(
            email=add_user_email
        )
        await self.invite_org_member_popup.ui_click_send_invite_button()

    # ********************   Accept invite to organization steps   ****************************
    @async_step("Accept invite to organization via UI")
    async def ui_accept_invite_to_org(
        self, org_name: str, email: str, role: str
    ) -> None:
        await self.main_page.verify_ui_invite_to_org_displayed(org_name=org_name)

        await self.main_page.ui_click_invite_to_org_button(org_name=org_name)
        await self.main_page.verify_ui_invite_org_info_displayed(org_name=org_name)
        await self.main_page.verify_ui_invite_to_org_role_is_valid(
            org_name=org_name, role=role
        )

        await self.main_page.ui_click_accept_invite_to_org(org_name=org_name)
        await self.main_page.ui_click_organization_settings_button(email=email)
        await self.org_settings_popup.verify_ui_select_org_button_displayed(
            org_name=org_name
        )

        await self.ui_reload_page()

    # ********************   Create project steps   ****************************
    @async_step("Create first project from main page")
    async def ui_create_first_proj_from_main_page(
        self,
        org_name: str,
        proj_name: str,
        default_role: str,
        make_default: bool = False,
    ) -> None:
        await self.main_page.ui_click_create_proj_button_main_page()
        await self.create_proj_popup.verify_ui_create_proj_popup_displayed(org_name)

        await self.create_proj_popup.ui_enter_proj_name(proj_name)
        await self.create_proj_popup.ui_select_role(default_role)
        if make_default:
            await self.create_proj_popup.ui_click_make_default_checkbox()
        await self.create_proj_popup.ui_click_create_button()

        await self.apps_page.verify_ui_apps_page_displayed()
