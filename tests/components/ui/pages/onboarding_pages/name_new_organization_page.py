from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class NameNewOrganizationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._name_your_organization_title = BaseElement(
            self.page, "h5", has_text="Name your Organization:"
        )
        self._organization_name_input = BaseElement(self.page, 'input[name="name"]')
        self._next_button = BaseElement(
            self.page, 'button[type="submit"]', has_text="Next"
        )

    async def is_loaded(self):
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._name_your_organization_title.expect_to_be_loaded()
            and await self._organization_name_input.expect_to_be_loaded()
            and await self._next_button.expect_to_be_loaded()
        )

    async def enter_organization_name(self, value):
        self.log(f"Enter {value} organization name")
        await self._organization_name_input.fill(value)

    async def click_next_button(self):
        self.log("Click next button")
        await self._next_button.click()
