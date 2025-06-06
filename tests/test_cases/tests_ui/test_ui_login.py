import pytest

from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


@async_suite("UI Login")
class TestUILogin:
    @pytest.fixture(autouse=True)
    async def setup(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
        test_config: ConfigManager,
    ) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._page_manager = page_manager
        self._data_manager = data_manager
        self._test_config = test_config
        self.ui_common_steps = UICommonSteps(
            self._page_manager, self._test_config, self._data_manager
        )

    @async_title("New user successful login")
    async def test_new_user_login(self) -> None:
        await self.ui_click_login_button()
        await self.ui_enter_valid_credentials()
        await self.ui_click_continue_button()
        await self.verify_ui_welcome_page_displayed()

    @async_step("Click login button")
    async def ui_click_login_button(self) -> None:
        await self._page_manager.auth_page.click_log_in_button()

    @async_step("Enter valid credentials")
    async def ui_enter_valid_credentials(self) -> None:
        await self._page_manager.login_page.enter_email(self._test_config.auth.email)
        await self._page_manager.login_page.enter_password(
            self._test_config.auth.password
        )

    @async_step("Click continue button")
    async def ui_click_continue_button(self) -> None:
        await self._page_manager.login_page.click_continue_button()

    @async_step("Verify that Welcome new user page displayed")
    async def verify_ui_welcome_page_displayed(self) -> None:
        await self._page_manager.welcome_new_user_page.is_loaded()
