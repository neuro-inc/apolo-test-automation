from typing import Any, cast
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class OrganizationPeoplePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return await self._get_invite_people_button().expect_to_be_loaded()

    def _get_invite_people_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Invite people")

    async def is_invite_people_button_displayed(self) -> bool:
        self.log("Check if Invite people button displayed")
        return await self._get_invite_people_button().is_visible()

    async def is_invite_people_button_enabled(self) -> bool:
        self.log("Check if Invite people button enabled")
        return await self._get_invite_people_button().is_enabled()

    async def click_invite_people_button(self) -> None:
        self.log("Click Invite people button")
        await self._get_invite_people_button().click()

    def _get_org_user_row(self, email: str) -> BaseElement:
        return BaseElement(self.page, f'tr:has(td:nth-child(1):text("{email}"))')

    async def is_org_user_row_displayed(self, email: str) -> bool:
        self.log(f"Check if Org user {email} row displayed")
        return await self._get_org_user_row(email).is_visible()

    def _get_role_user_row_field(self, email: str, field: int) -> BaseElement:
        return BaseElement(
            self.page,
            selector=f'tr:has(td:nth-child(1):text("{email}")) td:nth-child({field})',
        )

    async def get_org_user_role(self, email: str) -> str:
        self.log(f"Get Org user {email} role")
        element = self._get_role_user_row_field(email, 2)
        return await element.text_content()

    def _get_row_three_dots_btn(self, email: str) -> BaseElement:
        return BaseElement(
            self.page,
            f"tr:has(td:text('{email}')) button:has(svg[data-icon='ellipsis-vertical'])",
        )

    async def click_three_dots_btn(self, email: str) -> None:
        self.log(f"Click Three dots button in row {email}")
        await self._get_row_three_dots_btn(email).click()
        await self.page.wait_for_timeout(300)

    def _get_edit_user_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Edit user")

    async def is_edit_user_btn_displayed(self) -> bool:
        self.log("Check if Edit user button displayed")
        return await self._get_edit_user_btn().is_visible()

    async def is_edit_user_btn_enabled(self) -> bool:
        self.log("Check if Edit user button enabled")
        locator = self._get_edit_user_btn().locator
        pointer_events = await locator.evaluate(
            "el => getComputedStyle(el).pointerEvents"
        )
        return cast(str, pointer_events) != "none"

    async def click_edit_user_btn(self) -> None:
        self.log("Click Edit user button")
        await self._get_edit_user_btn().click()

    def _get_remove_user_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Remove user")

    async def is_remove_user_btn_displayed(self) -> bool:
        self.log("Check if Remove user button displayed")
        return await self._get_remove_user_btn().is_visible()

    async def is_remove_user_btn_enabled(self) -> bool:
        self.log("Check if Remove user button enabled")
        locator = self._get_remove_user_btn().locator
        pointer_events = await locator.evaluate(
            "el => getComputedStyle(el).pointerEvents"
        )
        return cast(str, pointer_events) != "none"

    async def click_remove_user_btn(self) -> None:
        self.log("Click Remove user button")
        await self._get_remove_user_btn().click()

    async def get_org_user_status(self, email: str) -> str:
        self.log(f"Get Org user {email} status")
        element = self._get_role_user_row_field(email, 4)
        return await element.text_content()

    async def get_org_user_credits(self, email: str) -> str:
        self.log(f"Get Org user {email} credits")
        element = self._get_role_user_row_field(email, 5)
        return await element.text_content()

    def _get_search_input(self) -> BaseElement:
        return BaseElement(self.page, "input[autocomplete='off'][placeholder=' ']")

    async def enter_search_value(self, value: str) -> None:
        self.log(f"Entering Search input: {value}")
        await self._get_search_input().fill(value)
        await self.page.wait_for_timeout(300)
