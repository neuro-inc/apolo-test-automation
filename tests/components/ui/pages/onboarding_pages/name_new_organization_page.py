from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class NameNewOrganizationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.__name_your_organization_title = BaseElement(self.page, 'h5', has_text="Name your Organization:")
        self.__organization_name_input = BaseElement(self.page, 'input[name="name"]')
        self.__next_button = BaseElement(self.page, 'button[type="submit"]', has_text="Next")

    def is_loaded(self):
        """Returns True if the page is considered loaded (key elements are visible)."""
        return (
            self.__name_your_organization_title.expect_to_be_loaded()
            and self.__organization_name_input.expect_to_be_loaded()
            and self.__next_button.expect_to_be_loaded()
        )

    def type_text_to_organization_name_input(self, value):
        self.__organization_name_input.fill(value)

    def click_next_button(self):
        self.__next_button.click()

