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
    async def reload_page(self) -> None:
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

    @async_step("Pass new user onboarding and create first organization via UI")
    async def ui_pass_new_user_onboarding(
        self, email: str, password: str, gherkin_name: str
    ) -> None:
        await self._pm.auth_page.click_log_in_button()
        await self._pm.login_page.login(email, password)
        assert await self._pm.welcome_new_user_page.is_loaded(email=email), (
            "Welcome new user page should be displayed!"
        )
        token = await extract_access_token_from_local_storage(self._pm.login_page.page)
        self._test_config.token = token

        await self._pm.page.wait_for_timeout(500)
        await self._pm.welcome_new_user_page.click_lets_do_it_button()
        await self._pm.join_organization_page.click_create_organization_button()

        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        organization_name = organization.org_name
        page = self._pm.name_your_organization_page
        await page.enter_organization_name(organization_name)
        await self._pm.name_your_organization_page.click_next_button()

        await self._pm.page.wait_for_timeout(500)
        await self._pm.thats_it_page.click_lets_do_it_button()

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
        assert await self._pm.invite_member_popup.is_loaded(), (
            "Invite member popup should be displayed!"
        )

        await self._pm.invite_member_popup.enter_user_data(email=add_user_email)
        await self._pm.invite_member_popup.select_user_role()
        assert await self._pm.invite_member_popup.is_invite_user_displayed(
            email=add_user_email
        ), f"Invite user {add_user_email} button should be displayed!"

        await self._pm.invite_member_popup.click_invite_user_button(
            email=add_user_email
        )
        await self._pm.invite_member_popup.click_send_invite_button()
