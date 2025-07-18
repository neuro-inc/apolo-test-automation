from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ProjectPeoplePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return await self._get_invite_people_btn().expect_to_be_loaded()

    def _get_invite_people_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Invite people")

    async def click_invite_people_btn(self) -> None:
        self.log("Click Invite People button")
        await self._get_invite_people_btn().click()
        await self.page.wait_for_timeout(300)

    def _get_row_by_username(self, username: str) -> BaseElement:
        return BaseElement(self.page, f'tr:has(td:nth-child(1):has-text("{username}"))')

    async def is_user_row_displayed(self, username: str) -> bool:
        self.log(f"Check if user {username} row displayed")
        return await self._get_row_by_username(username).is_visible()

    def _get_row_role_td(self, username: str) -> BaseElement:
        return BaseElement(
            self.page, f'tr:has(td:nth-child(1):has-text("{username}")) td:nth-child(2)'
        )

    async def get_row_role(self, username: str) -> str:
        return await self._get_row_role_td(username).text_content()

    def _get_row_email_td(self, username: str) -> BaseElement:
        return BaseElement(
            self.page, f'tr:has(td:nth-child(1):has-text("{username}")) td:nth-child(3)'
        )

    async def get_row_email(self, username: str) -> str:
        return await self._get_row_email_td(username).text_content()

    def _get_row_edit_btn(self, username: str) -> BaseElement:
        return BaseElement(
            self.page,
            f'tr:has(td:nth-child(1):has-text("{username}")) td:nth-child(5) button >> nth=0',
        )

    async def is_row_edit_btn_enabled(self, username: str) -> bool:
        self.log(f"Check if user {username} row edit btn enabled")
        return await self._get_row_edit_btn(username).is_enabled()

    async def click_row_edit_btn(self, username: str) -> None:
        self.log(f"Click {username} row edit button")
        await self._get_row_edit_btn(username).click()

    def _get_row_delete_btn(self, username: str) -> BaseElement:
        return BaseElement(
            self.page,
            f'tr:has(td:nth-child(1):has-text("{username}")) td:nth-child(5) button >> nth=1',
        )

    async def is_row_delete_btn_enabled(self, username: str) -> bool:
        self.log(f"Check if user {username} row delete button enabled")
        return await self._get_row_delete_btn(username).is_enabled()

    async def click_row_delete_btn(self, username: str) -> None:
        self.log(f"Click {username} row delete button")
        await self._get_row_delete_btn(username).click()
