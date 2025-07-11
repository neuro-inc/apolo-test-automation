from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class MainPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
    ) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

    @async_step("Open url in browser")
    async def ui_open_url_in_browser(self, url: str) -> None:
        await self._pm.main_page.open_url(url)

    @async_step("Verify that Verify email message displayed")
    async def verify_ui_email_message_displayed(self) -> None:
        assert await self._pm.main_page.is_verify_email_message_displayed(), (
            "Verify email message should be displayed!"
        )

    @async_step("Verify that User agreement pop up displayed")
    async def verify_ui_terms_of_agreement_displayed(self) -> None:
        assert await self._pm.main_page.is_user_agreement_title_displayed(), (
            "User agreement popup should be displayed!"
        )

    @async_step("Wait for User Agreement popup to disappear")
    async def ui_wait_user_agreement_disappear(self) -> None:
        await self._pm.main_page.wait_for_agreement_popup_to_disappear()

    @async_step("Check agreement checkbox")
    async def ui_check_agreement_checkbox(self) -> None:
        await self._pm.main_page.check_user_agreement_checkbox()

    @async_step("Click I Agree button")
    async def ui_click_i_agree_button(self) -> None:
        await self._pm.main_page.click_user_agreement_agree_button()

    @async_step("Click User Organization settings button")
    async def ui_click_organization_settings_button(self, email: str) -> None:
        await self._pm.main_page.click_organization_settings_button(email)

    @async_step("Verify project creation message is displayed")
    async def verify_ui_create_project_message_displayed(self, org_name: str) -> None:
        page = self._pm.main_page
        assert await page.is_create_first_project_text_field_displayed(org_name), (
            f"Organization {org_name} does not have a project creation message"
        )

    @async_step("Verify create project button displayed")
    async def verify_ui_create_project_button_displayed(self) -> None:
        assert await self._pm.main_page.is_create_first_project_button_displayed(), (
            "Create project button should be displayed!"
        )

    @async_step("Verify Main page is displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.main_page.is_loaded(), "Main page should be loaded!"

    @async_step("Verify that invitation to organization displayed on the left pane")
    async def verify_ui_invite_to_org_displayed(self, org_name: str) -> None:
        assert await self._pm.main_page.is_invite_to_org_button_displayed(
            org_name=org_name
        ), f"Invitation button to organization {org_name} should be displayed!"

    @async_step("Click invite to organization button on the left pane")
    async def ui_click_invite_to_org_button(self, org_name: str) -> None:
        await self._pm.main_page.click_invite_to_org_button(org_name=org_name)

    @async_step("Verify invite to organization info displayed on the main page")
    async def verify_ui_invite_org_info_displayed(self, org_name: str) -> None:
        await self._pm.main_page.is_invite_to_org_row_displayed(org_name=org_name)

    @async_step("Verify invite to organization role is valid")
    async def verify_ui_invite_to_org_role_is_valid(
        self, org_name: str, role: str
    ) -> None:
        value = await self._pm.main_page.get_invite_to_org_role(org_name=org_name)
        assert value.lower() == role.lower(), (
            f"Wrong user role in invite to the organization {org_name}"
        )

    @async_step("Click Accept button for invitation to the organization")
    async def ui_click_accept_invite_to_org(self, org_name: str) -> None:
        await self._pm.main_page.click_accept_invite_to_org(org_name=org_name)

    @async_step("Click Create project button on the main page")
    async def ui_click_create_proj_button_main_page(self) -> None:
        await self._pm.main_page.click_create_first_project_button()

    @async_step("Click Project button on the top pane of the main page")
    async def ui_click_proj_button_top_pane(self) -> None:
        await self._pm.main_page.click_top_pane_proj_button()

    @async_step("Click Files button on the left pane on the main page")
    async def ui_click_files_btn(self) -> None:
        await self._pm.main_page.click_files_button()
