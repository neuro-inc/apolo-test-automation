from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class JoinOrganizationPage(BasePage):
    def __init__(self, page, username):
        super().__init__(page)
        self._username = username
        self._join_organization_title = BaseElement(
            self.page, "h5.text-h3", has_text="Join Organization"
        )
        self._pass_username_text_field = BaseElement(
            self.page,
            "p",
            has_text="Pass your username to the organization manager to join existing organization",
        )
        self._establish_new_organization_text_field = BaseElement(
            self.page, "p", has_text="Or establish a new organization"
        )
        self._create_organization_button = BaseElement(
            self.page, "button", has_text="Create organization"
        )

    async def is_loaded(self):
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._join_organization_title.expect_to_be_loaded()
            and await self._pass_username_text_field.expect_to_be_loaded()
            and await self.__get_username_input().expect_to_be_loaded()
            and await self._establish_new_organization_text_field.expect_to_be_loaded()
            and await self._create_organization_button.expect_to_be_loaded()
        )

    def __get_username_input(self):
        return BaseElement(
            self.page, f'div:has(span:text("{self._username}")) > button'
        )

    async def click_create_organization_button(self):
        self.log("Click create organization button")
        await self._create_organization_button.click()
