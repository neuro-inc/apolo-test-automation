from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class WelcomeNewUserPage(BasePage):
    def __init__(self, page, email):
        super().__init__(page)
        self.__email = email
        self.__journey_text_field = BaseElement(self.page, "p:has-text('Ready to begin your journey?')")
        self.__lets_do_it_button = BaseElement(self.page, "button:has-text(\"Let's do it!\")")

    def is_loaded(self):
        """Returns True if the page is considered loaded (key elements are visible)."""
        return (
            self._get_welcome_user_message().expect_to_be_loaded()
            and self.__journey_text_field.expect_to_be_loaded()
            and self.__lets_do_it_button.expect_to_be_loaded()
        )

    def _get_welcome_user_message(self):
        return BaseElement(self.page, "h3.truncate.text-h3", has_text=f"Welcome, {self.__email}")

    def click_lets_do_it_button(self):
        self.__lets_do_it_button.click()
