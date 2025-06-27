from tests.reporting_hooks.reporting import async_step
from tests.utils.api_helper import APIHelper
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager


class UIProjectStructureSetupSteps:
    def __init__(
        self,
        page_manager: PageManager,
        test_config: ConfigManager,
        data_manager: DataManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        self._pm = page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper

    # ********************   invited to organization page steps   ****************************

    @async_step("Verify that Invite to organization page displayed")
    async def verify_ui_invite_to_org_page_displayed(
        self, org_name: str, user_role: str
    ) -> None:
        assert await self._pm.invited_to_org_page.is_loaded(
            org_name=org_name, user_role=user_role
        ), "Invite to organization page should be displayed!"

    @async_step("Click Accept and Go button")
    async def ui_click_accept_and_go_button(self) -> None:
        await self._pm.invited_to_org_page.click_accept_and_go_button()

    # ********************   Main page steps   ****************************
    @async_step("Verify project creation message is displayed")
    async def verify_ui_create_project_message_displayed(
        self, gherkin_name: str
    ) -> None:
        organization = self._data_manager.get_organization_by_gherkin_name(gherkin_name)
        assert organization, f"Organization {gherkin_name} not found"
        page = self._pm.main_page
        assert await page.is_create_first_project_text_field_displayed(
            organization.org_name
        ), f"Organization {gherkin_name} does not have a project creation message"

    @async_step("Verify create project button displayed")
    async def verify_ui_create_project_button_displayed(self) -> None:
        assert await self._pm.main_page.is_create_first_project_button_displayed(), (
            "Create project button should be displayed!"
        )

    @async_step("Click Create project button on the main page")
    async def ui_click_create_proj_button_main_page(self) -> None:
        await self._pm.main_page.click_create_first_project_button()

    @async_step("Click Project button on the top pane of the main page")
    async def ui_click_proj_button_top_pane(self) -> None:
        await self._pm.main_page.click_top_pane_proj_button()

    # ********************   No project popup steps   ******************
    @async_step("Verify No project popup displayed")
    async def verify_ui_no_proj_popup_displayed(self, org_name: str) -> None:
        assert await self._pm.no_proj_popup.is_loaded(org_name=org_name), (
            "No project popup should be displayed!"
        )

    @async_step("Click Create new project button")
    async def ui_click_create_new_proj_button(self) -> None:
        await self._pm.no_proj_popup.click_create_proj_button()

    # ********************   Projects info popup steps   ******************
    @async_step("Verify Projects info popup displayed")
    async def verify_ui_projects_info_popup_displayed(self, proj_name: str) -> None:
        assert await self._pm.projects_info_popup.is_loaded(proj_name=proj_name), (
            "Projects info popup should be displayed!"
        )

    @async_step("Verify select project button in Projects info popup displayed")
    async def verify_ui_other_proj_displayed_in_info(self, proj_name: str) -> None:
        assert await self._pm.projects_info_popup.is_select_proj_button_displayed(
            proj_name=proj_name
        ), f"Select {proj_name} button should be displayed!"

    @async_step("Click People button on the Projects info popup")
    async def ui_click_people_btn_proj_info_popup(self) -> None:
        await self._pm.projects_info_popup.click_people_btn()

    # ********************   Create project popup steps   ******************
    @async_step("Verify Create project popup displayed")
    async def verify_ui_create_proj_popup_displayed(self, org_name: str) -> None:
        assert await self._pm.create_proj_popup.is_loaded(org_name=org_name), (
            "Create project popup should be displayed!"
        )

    @async_step("Enter project name")
    async def ui_enter_proj_name(self, proj_name: str) -> None:
        await self._pm.create_proj_popup.enter_proj_name(proj_name=proj_name)

    @async_step("Select user role")
    async def ui_select_role(self, role: str) -> None:
        await self._pm.create_proj_popup.select_default_role(role=role)

    @async_step("Click Create button")
    async def ui_click_create_button(self) -> None:
        await self._pm.create_proj_popup.click_create_button()

    # ********************   Apps page steps   ******************
    @async_step("Verify Apps page displayed")
    async def verify_ui_apps_page_displayed(self) -> None:
        assert await self._pm.apps_page.is_loaded(), (
            "Create project popup should be displayed!"
        )

    # ********************   Project people page steps   ******************
    @async_step("Verify People page displayed")
    async def verify_ui_proj_people_page_displayed(self) -> None:
        assert await self._pm.project_people_page.is_loaded(), (
            "Project people page should be displayed!"
        )

    @async_step("Click Invite people button")
    async def ui_click_invite_people_proj_people_btn(self) -> None:
        await self._pm.project_people_page.click_invite_people_btn()

    @async_step("Verify user displayed in users list")
    async def verify_ui_user_displayed_in_users_list(self, username: str) -> None:
        assert await self._pm.project_people_page.is_user_row_displayed(
            username=username
        ), f"User {username} should be displayed in the project users list!"

    @async_step("Verify user role is valid")
    async def verify_ui_invited_user_role(self, username: str, role: str) -> None:
        value = await self._pm.project_people_page.get_row_role(username=username)
        assert value.lower() == role.lower(), f"User role should be {role}!"

    @async_step("Verify user email is valid")
    async def verify_ui_invited_user_email(self, username: str, email: str) -> None:
        value = await self._pm.project_people_page.get_row_email(username=username)
        assert value.lower() == email.lower(), f"User email should be {email}!"

    # ********************   Invite project member popup steps   ******************
    @async_step("Verify Invite project member popup displayed")
    async def verify_ui_invite_proj_member_popup_displayed(
        self, org_name: str, proj_name: str
    ) -> None:
        assert await self._pm.invite_proj_member_popup.is_loaded(
            org_name=org_name, proj_name=proj_name
        ), "Invite project member popup should be displayed!"

    @async_step("Enter user email/username")
    async def ui_enter_user_data(self, email: str) -> None:
        await self._pm.invite_proj_member_popup.enter_user_data(email)

    @async_step("Select user role")
    async def ui_select_user_role(self, role: str) -> None:
        await self._pm.invite_proj_member_popup.select_user_role(role=role)

    @async_step("Verify Invite user button displayed")
    async def verify_ui_invite_user_btn_displayed(self, email: str) -> None:
        assert await self._pm.invite_proj_member_popup.is_invite_user_btn_displayed(
            email=email
        ), f"Invite user {email} button should be displayed!"

    @async_step("Verify Invite user button not displayed")
    async def verify_ui_invite_user_btn_not_displayed(self, email: str) -> None:
        assert not await self._pm.invite_proj_member_popup.is_invite_user_btn_displayed(
            email=email
        ), f"Invite user {email} button should not be displayed!"

    @async_step("Verify Invite button disabled")
    async def verify_ui_invite_bth_disabled(self) -> None:
        assert not await self._pm.invite_proj_member_popup.is_invite_btn_enabled(), (
            "Invite button should be disabled!"
        )

    @async_step("Click invite user button")
    async def ui_click_invite_user_btn(self, email: str) -> None:
        await self._pm.invite_proj_member_popup.click_invite_user_btn(email=email)

    @async_step("Verify Invite button enabled")
    async def verify_ui_invite_bth_enabled(self) -> None:
        assert await self._pm.invite_proj_member_popup.is_invite_btn_enabled(), (
            "Invite button should be enabled!"
        )

    @async_step("Click Invite button")
    async def ui_click_invite_btn(self) -> None:
        await self._pm.invite_proj_member_popup.click_invite_btn()
