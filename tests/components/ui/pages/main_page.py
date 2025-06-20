from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_apps_button().expect_to_be_loaded()
            and await self._get_jobs_button().expect_to_be_loaded()
        )

    def _get_apps_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href="/apps"]')

    def _get_create_first_project_text_field(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page, f'p:text("Create project for{org_name}organization")'
        )

    async def is_create_first_project_text_field_displayed(self, org_name: str) -> bool:
        self.log("Check if create project text field displayed")
        return await self._get_create_first_project_text_field(org_name).is_visible()

    def _get_create_first_project_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create project")

    async def is_create_first_project_button_displayed(self) -> bool:
        self.log("Check if create project button displayed")
        return await self._get_create_first_project_button().is_visible()

    async def click_apps_button(self) -> None:
        self.log("Click apps button")
        await self._get_apps_button().click()

    def _get_jobs_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href^="/jobs"]')

    async def click_jobs_button(self) -> None:
        self.log("Click jobs button")
        await self._get_jobs_button().click()

    def _get_verify_email_message(self) -> BaseElement:
        return BaseElement(
            self.page, "p", has_text="Please verify your email before continuing."
        )

    async def is_verify_email_message_displayed(self) -> Any:
        self.log("Check if verify email message displayed")
        return await self._get_verify_email_message().is_visible()

    def _get_user_agreement_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Terms of Use Agreement")

    async def is_user_agreement_title_displayed(self) -> bool:
        self.log("Check if user_agreement pop up displayed")
        return await self._get_user_agreement_title().is_visible()

    def _get_user_agreement_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page, "label:has-text('I have read and agree to the Terms of Use')"
        )

    async def check_user_agreement_checkbox(self) -> None:
        self.log("Check user agreement checkbox")
        await self._get_user_agreement_checkbox().click()

    def _get_user_agreement_agree_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="I agree")

    async def click_user_agreement_agree_button(self) -> None:
        self.log("Click user agreement I Agree button")
        await self._get_user_agreement_agree_button().click()
