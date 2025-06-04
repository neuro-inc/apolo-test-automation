from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage

class MainPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def is_loaded(self, organization=None):
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
                await self.__get_apps_button().expect_to_be_loaded() and
                await self.__get_jobs_button().expect_to_be_loaded()
        )

    def __get_apps_button(self):
        return BaseElement(self.page, 'a[href="/apps"]')

    def __get_create_first_project_text_field(self, org_name):
        return BaseElement(self.page, f'p:text("Create project for{org_name}organization")')

    async def is_create_first_project_text_field_displayed(self, org_name):
        self.log("Check if create project text field displayed")
        return await self.__get_create_first_project_text_field(org_name).is_visible()

    def _get_create_first_project_button(self):
        return BaseElement(self.page, 'button', has_text="Create project")

    async def is_create_first_project_button_displayed(self):
        self.log("Check if create project button displayed")
        return await self._get_create_first_project_button().is_visible()

    async def click_apps_button(self):
        self.log("Click apps button")
        await self.__get_apps_button().click()

    def __get_jobs_button(self):
        return BaseElement(self.page, 'a[href^="/jobs"]')

    async def click_jobs_button(self):
        self.log("Click jobs button")
        await self.__get_jobs_button().click()
