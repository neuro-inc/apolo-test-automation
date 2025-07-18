from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class OrgSettingsPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Organization settings pop up displayed")
    async def verify_ui_popup_displayed(self, email: str, username: str) -> None:
        assert await self._pm.organization_settings_popup.is_loaded(
            email=email, username=username
        ), "Organization settings popup should be displayed!"

    @async_step("Click People button")
    async def ui_click_people_button(self) -> None:
        await self._pm.organization_settings_popup.click_people_button()

    @async_step(
        "Verify that Organization select button is displayed in organization settings popup"
    )
    async def verify_ui_select_org_button_displayed(self, org_name: str) -> None:
        assert (
            await self._pm.organization_settings_popup.is_select_org_button_displayed(
                org_name=org_name
            )
        ), f"Select organization {org_name} button should be displayed!"

    @async_step("Select organization in Organization settings popup")
    async def ui_select_org(self, org_name: str) -> None:
        await self._pm.organization_settings_popup.click_select_organization_button(
            org_name=org_name
        )

    @async_step(
        "Verify that Settings button is not displayed in organization settings popup"
    )
    async def verify_ui_settings_btn_not_displayed(self) -> None:
        assert (
            not await self._pm.organization_settings_popup.is_settings_btn_displayed()
        ), "Settings button should not be displayed!"

    @async_step(
        "Verify that Settings button is displayed in organization settings popup"
    )
    async def verify_ui_settings_btn_displayed(self) -> None:
        assert await self._pm.organization_settings_popup.is_settings_btn_displayed(), (
            "Settings button should be displayed!"
        )

    @async_step("Click Settings button")
    async def ui_click_settings_btn(self) -> None:
        await self._pm.organization_settings_popup.click_settings_button()

    @async_step(
        "Verify that Billing button is not displayed in organization settings popup"
    )
    async def verify_ui_billing_btn_not_displayed(self) -> None:
        assert (
            not await self._pm.organization_settings_popup.is_billing_btn_displayed()
        ), "Billing button should not be displayed!"

    @async_step(
        "Verify that Billing button is displayed in organization settings popup"
    )
    async def verify_ui_billing_btn_displayed(self) -> None:
        assert await self._pm.organization_settings_popup.is_billing_btn_displayed(), (
            "Billing button should be displayed!"
        )

    @async_step("Click Billing button")
    async def ui_click_billing_btn(self) -> None:
        await self._pm.organization_settings_popup.click_billing_button()

    @async_step("Verify the Create new organization button displayed")
    async def verify_ui_create_new_org_btn_displayed(self) -> None:
        assert await self._pm.organization_settings_popup.is_create_new_organization_btn_displayed(), (
            "Create new organization button should be displayed!"
        )

    @async_step("Click Create new organization button")
    async def ui_click_create_new_org_btn(self) -> None:
        await self._pm.organization_settings_popup.click_create_new_org_btn()
