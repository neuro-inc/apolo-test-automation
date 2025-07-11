import pytest

from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Login", parent="UI Tests")
class TestUILogin(BaseUITest):
    @pytest.fixture(autouse=True)
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps
        user = await steps.ui_signup_new_user_ver_link()

        self._email = user.email
        self._password = user.password

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
