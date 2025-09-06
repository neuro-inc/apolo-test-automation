import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Login", parent="UI Tests")
class TestUILogin(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps
        user = await steps.ui_signup_new_user_ver_link()

        self._email = user.email
        self._password = user.password

    @async_title("New user successful login")
    async def test_new_user_login(self) -> None:
        """
        ### Verify that:

        - User can login with valid credentials.
        """
        add_steps = await self.init_ui_test_steps()
        await add_steps.auth_page.ui_click_login_button()
        await add_steps.login_page.ui_enter_email(self._email)
        await add_steps.login_page.ui_enter_password(self._password)
        await add_steps.login_page.ui_click_continue_button()
        await add_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=self._email
        )
