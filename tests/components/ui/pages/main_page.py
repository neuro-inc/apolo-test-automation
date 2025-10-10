import re
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
        await self.wait_for_spinner()
        return (
            await self._get_apps_button().expect_to_be_loaded()
            and await self._get_jobs_button().expect_to_be_loaded()
        )

    async def open_url(self, url: str) -> None:
        await self.page.goto(url)
        self.log(f"Navigated to: {url}")

        await self.page.wait_for_timeout(500)

        self.log("Waiting for network idle...")
        await self.page.wait_for_load_state("networkidle", timeout=10000)
        self.log("Page is idle (networkidle state reached)")

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

    async def click_create_first_project_button(self) -> None:
        self.log("Click create first project button on the main page")
        await self._get_create_first_project_button().click()
        await self.page.wait_for_timeout(300)

    # ******************************  TOP PANE  **************************************************
    def _get_top_pane_proj_button(self) -> BaseElement:
        return BaseElement(self.page, "button.bg-rebecca", has_text="Project")

    async def click_top_pane_proj_button(self) -> None:
        self.log("Click create project button on the top pane")
        await self._get_top_pane_proj_button().click()
        await self.page.wait_for_timeout(300)

    def _get_credits_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Credits")

    def _get_credit_amount_field(self) -> BaseElement:
        return BaseElement(
            self.page, 'button:has-text("Credits") p.truncate.capitalize'
        )

    async def is_credits_btn_enabled(self) -> bool:
        self.log("Check if Credits button on the top pane enabled")
        return await self._get_credits_btn().is_enabled()

    async def click_credits_btn(self) -> None:
        self.log("Click Credits button on the top pane")
        await self._get_credits_btn().click()

    async def get_current_credits_amount(self) -> float:
        self.log("Get current credits amount")
        amount_str = await self._get_credit_amount_field().text_content()

        def assert_float(value: str) -> float:
            try:
                return float(value)
            except ValueError:
                raise AssertionError(f'Value "{value}" cannot be converted to float')

        return assert_float(amount_str)

    # ******************************  LEFT PANE  **************************************************

    def _get_apps_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href^="/apps?"]', has_text="Apps")

    async def click_apps_button(self) -> None:
        self.log("Click Apps button")
        await self._get_apps_button().click()

    def _get_files_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href*="/files?"]', has_text="Files")

    async def click_files_button(self) -> None:
        self.log("Click Files button")
        await self._get_files_button().click()

    def _get_jobs_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href^="/jobs?cluster="]', has_text="Jobs")

    async def click_jobs_button(self) -> None:
        self.log("Click Jobs button")
        await self._get_jobs_button().click()

    def _get_secrets_button(self) -> BaseElement:
        return BaseElement(
            self.page, 'a[href^="/secrets?cluster="]', has_text="Secrets"
        )

    async def click_secrets_button(self) -> None:
        self.log("Click Secrets button")
        await self._get_secrets_button().click()

    def _get_disks_button(self) -> BaseElement:
        return BaseElement(self.page, 'a[href^="/disks?"]', has_text="Disks")

    async def click_disks_button(self) -> None:
        self.log("Click Disks button")
        await self._get_disks_button().click()

    def _get_organization_settings_button(self, email: str) -> BaseElement:
        return BaseElement(self.page, "div[slot='trigger']", has_text=email)

    async def click_organization_settings_button(self, email: str) -> None:
        self.log("Click organization settings button")
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

    async def wait_for_agreement_popup_to_disappear(self) -> None:
        await self._get_user_agreement_title().locator.wait_for(state="detached")

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

    # ******************************  APPS  **************************************************

    def _get_installed_apps_btn(self) -> BaseElement:
        return BaseElement(
            self.page,
            "a[href='/apps/installed']",
        )

    async def click_installed_apps_btn(self) -> None:
        self.log("Click Installed Apps button")
        await self._get_installed_apps_btn().click()

    async def _get_app_container(self, app_name: str) -> BaseElement:
        elements = await BaseElement.find_all(
            self.page,
            "div.peer",
            has=self.page.get_by_role("link", name=app_name),
        )
        if not elements:
            return BaseElement(
                self.page, "div.peer", has=self.page.get_by_role("link", name=app_name)
            )
        return elements[-1]

    async def verify_app_container_displayed(self, app_name: str) -> bool:
        self.log(f"Verify app container {app_name} displayed")

        container_area = self.page.locator("div.min-h-0.min-w-0.overflow-auto")

        try:
            for _ in range(10):  # limit to avoid infinite loop
                container = await self._get_app_container(app_name)
                if await container.is_visible():
                    return True

                # scroll a bit down
                await container_area.evaluate("el => el.scrollBy(0, 300)")
                self.log(f"Scroll to {app_name} container...")
                await self.page.wait_for_timeout(100)  # give UI some time to render

            self.log(f"App container {app_name} not found after scrolling")
            return False

        except Exception as e:
            self.log(f"App container {app_name} not found: {e}")
            return False

    async def _get_app_install_btn(self, app_name: str) -> BaseElement:
        container = await self._get_app_container(app_name)
        if not container:
            raise ValueError(f"App container not found for {app_name}")

        locator = container.locator.locator("a", has_text=re.compile(r"^Install$"))
        return BaseElement(self.page, locator=locator)

    async def click_install_btn_app_container(self, app_name: str) -> None:
        element = await self._get_app_install_btn(app_name)
        await element.click()
        await self.page.wait_for_timeout(2000)

    def _get_container_installed_label(self, app_name: str) -> BaseElement:
        return BaseElement(
            self.page, f'a[href="/apps/installed/{app_name}"]:has-text("Installed")'
        )

    async def is_container_installed_label_visible(self, app_name: str) -> bool:
        self.log(f"Verify installed label on {app_name} container is visible")
        element = self._get_container_installed_label(app_name)
        return await element.is_visible()

    async def click_container_installed_label(self, app_name: str) -> None:
        self.log(f"Click installed label on {app_name} container")
        element = self._get_container_installed_label(app_name)
        await element.click()

    def _get_container_show_all_btn(self, app_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            f'a[href="/apps/installed/{app_name}"].inline-flex:has-text("Show All")',
        )

    async def is_container_show_all_btn_visible(self, app_name: str) -> bool:
        element = self._get_container_show_all_btn(app_name)
        return await element.is_visible()

    async def click_container_show_all_btn(self, app_name: str) -> None:
        element = self._get_container_show_all_btn(app_name)
        await element.click()
        await self.wait_for_spinner()

    def _get_installed_app_container(self, app_name: str, owner: str) -> BaseElement:
        locator = (
            "div.rounded-xl.bg-white.p-6"
            f":has(p.text-h6:has-text('{app_name}'))"
            f":has(div:has(p.text-footnote:has-text('Owner')) p.truncate:has-text('{owner}'))"
        )
        return BaseElement(self.page, locator)

    async def is_installed_app_displayed(self, app_name: str, owner: str) -> bool:
        self.log(f"Check if installed app container {app_name} displayed")
        return await self._get_installed_app_container(app_name, owner).is_visible()

    def _get_app_details_button(self, app_name: str, owner: str) -> BaseElement:
        locator = (
            "div.rounded-xl.bg-white.p-6"
            f":has(p.text-h6:has-text('{app_name}'))"
            f":has(div:has(p.text-footnote:has-text('Owner')) p.truncate:has-text('{owner}')) "
            "a:has-text('Details')"
        )
        return BaseElement(self.page, locator)

    async def is_app_details_btn_displayed(self, app_name: str, owner: str) -> bool:
        self.log(f"Check if App Details button in {app_name} container displayed")
        return await self._get_app_details_button(app_name, owner).is_visible()

    async def click_app_details_btn(self, app_name: str, owner: str) -> None:
        self.log(f"Click App Details button in {app_name} container")
        await self._get_app_details_button(app_name, owner).click()
        await self.wait_for_spinner()
