from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ThatsItPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.__thats_it_title = BaseElement(self.page, 'h3', has_text="That's it")
        self.__nice_text_field = BaseElement(self.page, 'p',
                                             has_text="Now go and change the world! And don't forget to have fun")
        self.__lets_do_it_button = BaseElement(self.page, 'button', has_text="Let's do it!")

    def is_loaded(self):
        """Returns True if the page is considered loaded (key elements are visible)."""
        return (
            self.__thats_it_title.expect_to_be_loaded()
            and self.__nice_text_field.expect_to_be_loaded()
            and self.__lets_do_it_button.expect_to_be_loaded()
        )

    def click_lets_do_it_button(self):
        self.__lets_do_it_button.click()
