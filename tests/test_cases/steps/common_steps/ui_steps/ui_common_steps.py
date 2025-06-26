from tests.reporting_hooks.reporting import async_step
from tests.utils.api_helper import APIHelper
from tests.utils.browser_helper import extract_access_token_from_local_storage
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager, UserData


class UICommonSteps:
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

    @async_step("Reload page")
    async def ui_reload_page(self) -> None:
        await self._pm.page.reload()

    @async_step("Login via UI")
    async def ui_login(self, email: str, password: str) -> None:
        await self._pm.auth_page.click_log_in_button()
        await self._pm.login_page.login(email, password)
        assert await self._pm.welcome_new_user_page.is_loaded(email=email), (
            "Welcome new user page should be displayed!"
        )
        token = await extract_access_token_from_local_storage(self._pm.login_page.page)
        self._test_config.token = token

    # ********************   Onboarding steps   ****************************

    @async_step("Pass new user onboarding and create first organization via UI")
    async def ui_pass_new_user_onboarding(self, gherkin_name: str) -> None:
        token = await extract_access_token_from_local_storage(self._pm.login_page.page)
        self._test_config.token = token

        await self.ui_click_welcome_page_lets_do_it_button()
        await self.ui_click_create_org_button()

        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        org_name = organization.org_name
        await self.ui_enter_organization_name(org_name)
        await self.ui_click_name_org_next_button()

        await self.ui_thats_it_p_lets_do_it_button()

        await self.verify_ui_main_page_displayed()

    @async_step("Click Let's do it button on a Welcome page")
    async def ui_click_welcome_page_lets_do_it_button(self) -> None:
        await self._pm.welcome_new_user_page.click_lets_do_it_button()

    @async_step("Click Create organization button on a join organization page")
    async def ui_click_create_org_button(self) -> None:
        await self._pm.join_organization_page.click_create_organization_button()

    @async_step("Enter organization name")
    async def ui_enter_organization_name(self, org_name: str) -> None:
        await self._pm.name_your_organization_page.enter_organization_name(org_name)

    @async_step("Click Next button on a name organization page")
    async def ui_click_name_org_next_button(self) -> None:
        await self._pm.name_your_organization_page.click_next_button()

    @async_step("Click Let's do it button on a That's it page")
    async def ui_thats_it_p_lets_do_it_button(self) -> None:
        await self._pm.thats_it_page.click_lets_do_it_button()

    @async_step("Verify that main page is loaded")
    async def verify_ui_main_page_displayed(self) -> None:
        assert await self._pm.main_page.is_loaded(), "Main page should be loaded!"

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
        assert await self._pm.auth_page.is_loaded(), "Auth page should be displayed!"

        await self._pm.auth_page.click_log_in_button()
        assert await self._pm.signup_username_page.is_loaded(), (
            "Signup username page should be displayed!"
        )

        await self._pm.signup_username_page.enter_username(user.username)
        await self._pm.signup_username_page.click_signup_button()
        assert await self._pm.main_page.is_user_agreement_title_displayed(), (
            "User agreement popup should be displayed!"
        )

        await self._pm.main_page.check_user_agreement_checkbox()
        await self._pm.main_page.click_user_agreement_agree_button()
        assert await self._pm.welcome_new_user_page.is_loaded(email=user.email), (
            "Welcome new user page should be displayed!"
        )

        return user

    # ********************   invite user to organization steps   ****************************
    @async_step("Invite user to organization via UI")
    async def ui_invite_user_to_org(
        self, email: str, username: str, add_user_email: str
    ) -> None:
        await self._pm.main_page.click_organization_settings_button(email)
        assert await self._pm.organization_settings_popup.is_loaded(
            email=email, username=username
        ), "Organization settings popup should be displayed!"

        await self._pm.organization_settings_popup.click_people_button()
        assert await self._pm.organization_people_page.is_loaded(), (
            "Organization people page should be displayed!"
        )

        await self._pm.organization_people_page.click_invite_people_button()
        assert await self._pm.invite_org_member_popup.is_loaded(), (
            "Invite member popup should be displayed!"
        )

        await self._pm.invite_org_member_popup.enter_user_data(email=add_user_email)
        await self._pm.invite_org_member_popup.select_user_role()
        assert await self._pm.invite_org_member_popup.is_invite_user_displayed(
            email=add_user_email
        ), f"Invite user {add_user_email} button should be displayed!"

        await self._pm.invite_org_member_popup.click_invite_user_button(
            email=add_user_email
        )
        await self._pm.invite_org_member_popup.click_send_invite_button()

    # ********************   Create project steps   ****************************
    @async_step("Create first project from main page")
    async def ui_create_first_proj_from_main_page(
        self,
        org_name: str,
        proj_name: str,
        default_role: str,
        make_default: bool = False,
    ) -> None:
        await self.ui_click_create_proj_button_main_page()
        await self.verify_ui_create_proj_popup_displayed(org_name)

        await self.ui_enter_proj_name(proj_name)
        await self.ui_select_role(default_role)
        if make_default:
            await self.ui_click_make_default_checkbox()
        await self.ui_click_create_button()

        await self.verify_ui_apps_page_displayed()

    @async_step("Click Create project button on the main page")
    async def ui_click_create_proj_button_main_page(self) -> None:
        await self._pm.main_page.click_create_first_project_button()

    @async_step("Verify Create project popup displayed")
    async def verify_ui_create_proj_popup_displayed(self, org_name: str) -> None:
        assert await self._pm.create_proj_popup.is_loaded(org_name=org_name), (
            "Create project popup should be displayed!"
        )

    @async_step("Enter project name")
    async def ui_enter_proj_name(self, proj_name: str) -> None:
        await self._pm.create_proj_popup.enter_proj_name(proj_name=proj_name)

    @async_step("Select user role")
    async def ui_select_role(self, role: str) -> None:
        await self._pm.create_proj_popup.select_default_role(role=role)

    @async_step("Click project default checkbox")
    async def ui_click_make_default_checkbox(self) -> None:
        await self._pm.create_proj_popup.click_proj_default_checkbox()

    @async_step("Click Create button")
    async def ui_click_create_button(self) -> None:
        await self._pm.create_proj_popup.click_create_button()

    @async_step("Verify Apps page displayed")
    async def verify_ui_apps_page_displayed(self) -> None:
        assert await self._pm.apps_page.is_loaded(), "Apps page should be displayed!"
