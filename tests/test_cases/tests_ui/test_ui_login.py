import pytest

from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.components.ui.page_manager import PageManager
from tests.utils.api_helper import APIHelper
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager


@async_suite("UI Login")
class TestUILogin:
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
        self._pm = page_manager
        self._data_manager = data_manager
        self._test_config = test_config
        self._users_manager = users_manager
        self._api_helper = api_helper

        self._email = self._users_manager.default_user.email
        self._password = self._users_manager.default_user.password

    @async_title("New user successful login")
    async def test_new_user_login(self) -> None:
        await self.ui_click_login_button()
        await self.ui_enter_valid_credentials()
        await self.ui_click_continue_button()
        await self.verify_ui_welcome_page_displayed()

    @async_step("Click login button")
    async def ui_click_login_button(self) -> None:
        await self._pm.auth_page.click_log_in_button()

    @async_step("Enter valid credentials")
    async def ui_enter_valid_credentials(self) -> None:
        await self._pm.login_page.enter_email(self._email)
        await self._pm.login_page.enter_password(self._password)

    @async_step("Click continue button")
    async def ui_click_continue_button(self) -> None:
        await self._pm.login_page.click_continue_button()

    @async_step("Verify that Welcome new user page displayed")
    async def verify_ui_welcome_page_displayed(self) -> None:
        await self._pm.welcome_new_user_page.is_loaded(email=self._email)
