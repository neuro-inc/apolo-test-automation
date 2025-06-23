from tests.reporting_hooks.reporting import async_step
from tests.utils.api_helper import APIHelper
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager


class UIOrganizationStructureSetupSteps:
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

    # ********************   Welcome new user page steps   ****************************
    @async_step("Click the let's do it button on Welcome page")
    async def ui_click_welcome_lets_do_it_button(self) -> None:
        await self._pm.welcome_new_user_page.click_lets_do_it_button()

    # ********************   Join organization page steps   ****************************
    @async_step("Verify Join organization page displayed")
    async def verify_ui_join_organization_page_displayed(self, username: str) -> None:
        assert await self._pm.join_organization_page.is_loaded(username=username), (
            "Join organization page should be displayed!"
        )

    @async_step("Click create organization button")
    async def ui_click_create_organization_button(self) -> None:
        await self._pm.join_organization_page.click_create_organization_button()

    # ********************   Name organization page steps   ****************************
    @async_step("Verify Name organization page displayed")
    async def verify_ui_name_organization_page_displayed(self) -> None:
        assert await self._pm.name_your_organization_page.is_loaded(), (
            "Name organization page should be displayed!"
        )

    @async_step("Enter organization name")
    async def ui_enter_organization_name(self, gherkin_name: str) -> None:
        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        organization_name = organization.org_name
        page = self._pm.name_your_organization_page
        await page.enter_organization_name(organization_name)

    @async_step("Click next button")
    async def ui_click_next_button(self) -> None:
        await self._pm.name_your_organization_page.click_next_button()

    # ********************   That's it page steps   ****************************
    @async_step("Verify That's it page displayed")
    async def verify_ui_thats_it_page_displayed(self) -> None:
        assert await self._pm.thats_it_page.is_loaded(), (
            "That's it page should be loaded!"
        )

    @async_step("Click lets do it button on That's it page")
    async def ui_click_thats_it_lets_do_it_button(self) -> None:
        await self._pm.thats_it_page.click_lets_do_it_button()

    # ********************   Main page steps   ****************************
    @async_step("Verify Main page is displayed")
    async def verify_ui_main_page_displayed(self) -> None:
        assert await self._pm.main_page.is_loaded(), "Main page should be loaded!"

    @async_step("Click User Organization settings button")
    async def ui_click_organization_settings_button(self, email: str) -> None:
        await self._pm.main_page.click_organization_settings_button(email)

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

    # ********************   Organization settings popup steps   ****************************

    @async_step(
        "Verify that Organization select button is displayed in organization settings popup"
    )
    async def verify_ui_select_org_button_displayed(self, org_name: str) -> None:
        assert (
            await self._pm.organization_settings_popup.is_select_org_button_displayed(
                org_name=org_name
            )
        ), f"Select organization {org_name} button should be displayed!"

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
