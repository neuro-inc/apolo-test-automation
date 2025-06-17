import pytest
from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.components.ui.page_manager import PageManager
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
        data_manager: DataManager,
        test_config: ConfigManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._page_manager = page_manager
        self._data_manager = data_manager
        self._test_config = test_config
        self._users_manager = users_manager
        self._api_helper = api_helper
        self.ui_common_steps = UICommonSteps(
            self._page_manager,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )
        self._user = self._users_manager.generate_user()

    @async_title("New user successful signup")
    async def test_new_user_signup(self) -> None:
        await self.ui_click_signup_button()
        await self.ui_enter_email(self._user.email)
        await self.ui_enter_password(self._user.password)
        await self.ui_click_continue_button()
        await self.verify_ui_email_message_displayed()
        await self.activate_email_verification_link(self._user.email)
        await self.ui_open_product_base_page()
        await self.verify_ui_auth_page_displayed()
        await self.ui_click_login_button()
        await self.verify_ui_signup_username_page_displayed()
        await self.ui_enter_username(self._user.username)
        await self.ui_usr_click_signup_button()
        await self.verify_ui_terms_of_agreement_displayed()
        await self.ui_check_agreement_checkbox()
        await self.ui_click_i_agree_button()

        await self.verify_ui_welcome_page_displayed()

    @async_step("Click signup button")
    async def ui_click_signup_button(self) -> None:
        await self._page_manager.auth_page.click_sign_up_button()

    @async_step("Enter email")
    async def ui_enter_email(self, email: str) -> None:
        await self._page_manager.signup_page.enter_email(email)

    @async_step("Enter password")
    async def ui_enter_password(self, password: str) -> None:
        await self._page_manager.signup_page.enter_password(password)

    @async_step("Click continue button")
    async def ui_click_continue_button(self) -> None:
        await self._page_manager.signup_page.click_continue_button()

    @async_step("Verify that Verify email message displayed")
    async def verify_ui_email_message_displayed(self) -> None:
        assert await self._page_manager.main_page.is_verify_email_message_displayed()

    @async_step("Verify user email with the activation link")
    async def activate_email_verification_link(self, email: str) -> None:
        needs_verification, url = await self._api_helper.check_user_needs_verification(
            email
        )
        assert needs_verification, f"User {email} does not need verification!!!!"

        await self._page_manager.page.goto(url)

    @async_step("Open product base page")
    async def ui_open_product_base_page(self) -> None:
        base_url = self._test_config.base_url
        await self._page_manager.page.goto(base_url)

    @async_step("Verify that Welcome new user page displayed")
    async def verify_ui_welcome_page_displayed(self) -> None:
        assert await self._page_manager.welcome_new_user_page.is_loaded(
            email=self._user.email
        )

    @async_step("Verify that Auth page displayed")
    async def verify_ui_auth_page_displayed(self) -> None:
        assert await self._page_manager.auth_page.is_loaded()

    @async_step("Click login button")
    async def ui_click_login_button(self) -> None:
        await self._page_manager.auth_page.click_log_in_button()

    @async_step("Verify that Signup username page displayed")
    async def verify_ui_signup_username_page_displayed(self) -> None:
        assert await self._page_manager.signup_username_page.is_loaded()

    @async_step("Enter username")
    async def ui_enter_username(self, username: str) -> None:
        await self._page_manager.signup_username_page.enter_username(username)

    @async_step("Click signup button on Signup username page")
    async def ui_usr_click_signup_button(self) -> None:
        await self._page_manager.signup_username_page.click_signup_button()

    @async_step("Verify that User agreement pop up displayed")
    async def verify_ui_terms_of_agreement_displayed(self) -> None:
        assert await self._page_manager.main_page.is_user_agreement_title_displayed()

    @async_step("Check agreement checkbox")
    async def ui_check_agreement_checkbox(self) -> None:
        await self._page_manager.main_page.check_user_agreement_checkbox()

    @async_step("Click i Agree button")
    async def ui_click_i_agree_button(self) -> None:
        await self._page_manager.main_page.click_user_agreement_agree_button()
