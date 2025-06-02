from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class AuthPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.__log_in_button = BaseElement(self.page, "button:text('Log in')")
        self.__sign_up_button = BaseElement(self.page, "button:text('Sign up')")

    def is_loaded(self):
        """Returns True if the page is considered loaded (key elements are visible)."""
        return (
            self.__log_in_button.expect_to_be_loaded()
            and self.__sign_up_button.expect_to_be_loaded()
        )

    def click_log_in_button(self):
        self.__log_in_button.click()

    def click_sign_up_button(self):
        self.__sign_up_button.click()
