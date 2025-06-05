from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._email_input = BaseElement(self.page, "input[name='username']")
        self._password_input = BaseElement(self.page, "input[name='password']")
        self._continue_button = BaseElement(
            self.page, "button[type='submit'][name='action'][value='default']"
        )

    async def is_loaded(self):
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page is loaded")
        return (
            await self._email_input.expect_to_be_loaded()
            and await self._password_input.expect_to_be_loaded()
            and await self._continue_button.expect_to_be_loaded()
        )

    async def enter_email(self, text: str):
        self.log(f"Enter {text} email")
        await self._email_input.fill(text)

    async def enter_password(self, text: str):
        self.log("Enter ********* password")
        await self._password_input.fill(text)

    async def login(self, test_config, email=None, password=None):
        email = email if email else test_config.auth.email
        password = password if password else test_config.auth.password
        await self._email_input.fill(email)
        await self._password_input.fill(password)
        await self.click_continue_button()

    async def click_continue_button(self):
        self.log("Click continue button")
        await self._continue_button.click()
