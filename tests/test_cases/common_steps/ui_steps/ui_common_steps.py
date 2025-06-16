from tests.reporting_hooks.reporting import async_step
from tests.utils.api_helper import APIHelper
from tests.utils.browser_helper import extract_access_token_from_local_storage
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager


class UICommonSteps:
    def __init__(
        self,
        page_manager: PageManager,
        test_config: ConfigManager,
        data_manager: DataManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        self._page_manager = page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper

    @async_step("Login via UI")
    async def ui_login(self, email: str, password: str) -> None:
        await self._page_manager.auth_page.click_log_in_button()
        await self._page_manager.login_page.login(email, password)
        assert await self._page_manager.welcome_new_user_page.is_loaded(email=email)
        token = await extract_access_token_from_local_storage(
            self._page_manager.login_page.page
        )
        self._test_config.token = token

    @async_step("Pass new user onboarding and create first organization via UI")
    async def ui_pass_new_user_onboarding(
        self, email: str, password: str, gherkin_name: str
    ) -> None:
        await self._page_manager.auth_page.click_log_in_button()
        await self._page_manager.login_page.login(email, password)
        assert await self._page_manager.welcome_new_user_page.is_loaded(email=email)
        token = await extract_access_token_from_local_storage(
            self._page_manager.login_page.page
        )
        self._test_config.token = token

        await self._page_manager.page.wait_for_timeout(500)
        await self._page_manager.welcome_new_user_page.click_lets_do_it_button()
        await (
            self._page_manager.join_organization_page.click_create_organization_button()
        )

        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        organization_name = organization.org_name
        page = self._page_manager.name_your_organization_page
        await page.enter_organization_name(organization_name)
        await self._page_manager.name_your_organization_page.click_next_button()

        await self._page_manager.page.wait_for_timeout(500)
        await self._page_manager.welcome_new_user_page.click_lets_do_it_button()

    @async_step("Signup new user via UI and activate email verification link")
    async def ui_signup_new_user_ver_link(self) -> None:
        user = self._users_manager.generate_user()
        await self._page_manager.auth_page.click_sign_up_button()
        await self._page_manager.signup_page.enter_email(user.email)
        await self._page_manager.signup_page.enter_password(user.password)
        await self._page_manager.signup_page.click_continue_button()
        assert await self._page_manager.main_page.is_verify_email_message_displayed(), (
            "Verify email message is not displayed!!!"
        )

        needs_verification, url = await self._api_helper.check_user_needs_verification(
            user.email,
        )
        assert needs_verification, f"User {user.email} does not need verification!!!!"

        await self._page_manager.page.goto(url)

        base_url = self._test_config.base_url
        await self._page_manager.page.goto(base_url)
        assert await self._page_manager.auth_page.is_loaded()

        await self._page_manager.auth_page.click_log_in_button()
        assert await self._page_manager.signup_username_page.is_loaded()

        await self._page_manager.signup_username_page.enter_username(user.username)
        await self._page_manager.signup_username_page.click_signup_button()
        assert await self._page_manager.main_page.is_user_agreement_title_displayed()

        await self._page_manager.main_page.check_user_agreement_checkbox()
        await self._page_manager.main_page.click_user_agreement_agree_button()
        assert await self._page_manager.welcome_new_user_page.is_loaded(
            email=user.email
        )
