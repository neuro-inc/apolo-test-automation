from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ProjectsInfoPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        proj_name = kwargs.get("proj_name")
        if not isinstance(proj_name, str):
            raise ValueError("Expected 'proj_name' to be a non-empty string in kwargs")

        return (
            await self._get_projects_title().expect_to_be_loaded()
            and await self._get_current_proj_label(proj_name).expect_to_be_loaded()
        )

    def _get_projects_title(self) -> BaseElement:
        return BaseElement(
            self.page, "p.p-5.text-caption.uppercase", has_text="Projects"
        )

    def _get_current_proj_label(self, proj_name: str) -> BaseElement:
        return BaseElement(self.page, "p.word-break-case", has_text=proj_name)

    def _get_create_new_proj_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create new project")

    async def click_create_new_proj_btn(self) -> None:
        self.log("Click Create new project button")
        await self._get_create_new_proj_btn().click()
        await self.page.wait_for_timeout(200)

    def _get_select_proj_btn(self, proj_name: str) -> BaseElement:
        return BaseElement(self.page, "button", has_text=proj_name)

    async def is_select_proj_button_displayed(self, proj_name: str) -> bool:
        self.log(f"Check if select project {proj_name} button displayed")
        return await self._get_select_proj_btn(proj_name).is_visible()

    def _get_people_btn(self) -> BaseElement:
        return BaseElement(
            self.page, 'a[href^="/project-settings/users"]', has_text="People"
        )

    async def click_people_btn(self) -> None:
        self.log("Click People button")
        await self._get_people_btn().click()
