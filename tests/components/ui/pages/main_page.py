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

    # **************************  NO PROJECT CREATED  *********************************************

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

    # ******************************  LEFT PANE  **************************************************

    def _get_apps_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href="/apps"]')

    async def click_apps_button(self) -> None:
        self.log("Click apps button")
        await self._get_apps_button().click()

    def _get_jobs_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href^="/jobs"]')

    async def click_jobs_button(self) -> None:
        self.log("Click jobs button")
        await self._get_jobs_button().click()

    def _get_organization_settings_button(self, email: str) -> BaseElement:
        return BaseElement(self.page, "div[slot='trigger']", has_text=email)

    async def click_organization_settings_button(self, email: str) -> None:
        self.log("Click organization settings button")
        await self.page.wait_for_timeout(200)
        await self._get_organization_settings_button(email).click()

    # *************************  ORGANIZATION SETTING POPUP  *******************************************
    def _get_select_organization_button(self, org_name: str) -> BaseElement:
        return BaseElement(self.page, "p.truncate", has_text=org_name)

    async def click_select_organization_button(self, org_name: str) -> None:
        self.log(f"Select {org_name} organization")
        await self._get_select_organization_button(org_name).click()

    # *****************************  NOT VERIFIED USER  ************************************************

    def _get_verify_email_message(self) -> BaseElement:
        return BaseElement(
            self.page, "p", has_text="Please verify your email before continuing."
        )

    async def is_verify_email_message_displayed(self) -> Any:
        self.log("Check if verify email message displayed")
        return await self._get_verify_email_message().is_visible()

    # ******************************  USER AGREEMENT  **************************************************

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

    def _get_invite_to_org_button(self, org_name: str) -> BaseElement:
        return BaseElement(self.page, 'a[href="/invites"]', has_text=org_name)

    async def is_invite_to_org_button_displayed(self, org_name: str) -> bool:
        self.log(f"Check if invite to organization {org_name} displayed")
        return await self._get_invite_to_org_button(org_name).is_visible()

    async def click_invite_to_org_button(self, org_name: str) -> None:
        self.log(f"Click invite to organization {org_name} button")
        await self._get_invite_to_org_button(org_name).click()

    def _get_invite_to_org_row(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page, f'tr.contents:has(td:nth-child(1):text-is("{org_name}"))'
        )

    def _get_invite_row_role_td(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            f'tr.contents:has(td:nth-child(1):text-is("{org_name}")) >> td:nth-child(2)',
        )

    def _get_invite_row_accept_button(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            f'''
            tr.contents:has(td:nth-child(1):text-is("{org_name}"))
            >> td:nth-child(5)
            >> button:has-text("Accept")
            ''',
        )

    def _get_invite_row_decline_button(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            f'''
            tr.contents:has(td:nth-child(1):text-is("{org_name}"))
            >> td:nth-child(5)
            >> button:has-text("Decline")
            ''',
        )

    async def is_invite_to_org_row_displayed(self, org_name: str) -> bool:
        self.log(f"Check if invite row to organization {org_name} displayed")
        row = self._get_invite_to_org_row(org_name)
        accept_btn = self._get_invite_row_accept_button(org_name)
        decline_btn = self._get_invite_row_decline_button(org_name)

        return (
            await row.is_visible()
            and await accept_btn.is_visible()
            and await decline_btn.is_visible()
        )

    async def get_invite_to_org_role(self, org_name: str) -> str:
        self.log(f"Get user role in invite to organization {org_name}")
        role_td = self._get_invite_row_role_td(org_name)
        return await role_td.text_content()

    async def click_accept_invite_to_org(self, org_name: str) -> None:
        self.log(f"Click accept invite to organization {org_name} button")
        await self._get_invite_row_accept_button(org_name).click()
