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
