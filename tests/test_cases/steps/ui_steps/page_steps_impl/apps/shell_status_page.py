from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ShellDetailsPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Shell app Details page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.shell_details_page.is_loaded(), (
            "Shell app Details page should be displayed!"
        )

    @async_step("Verify that app status is valid")
    async def verify_ui_app_status_is_valid(self, expected_status: str) -> None:
        actual_status = await self._pm.shell_details_page.get_app_status()
        assert actual_status.lower() == expected_status.lower(), (
            f"Expected {expected_status} but got {actual_status}!"
        )

    @async_step("Get Shell app UUID")
    async def ui_get_shell_app_uuid(self) -> str:
        return await self._pm.shell_details_page.get_uuid_value()

    @async_step("Validate Shell app details info")
    async def verify_ui_app_details_info(
        self, owner: str, app_id: str, app_name: str, proj_name: str, org_name: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._pm.shell_details_page.verify_app_details_info(
            owner=owner,
            app_id=app_id,
            app_name=app_name,
            proj_name=proj_name,
            org_name=org_name,
        )
        assert result, error_message

    @async_step("Click Uninstall button")
    async def ui_click_uninstall_btn(self) -> None:
        await self._pm.shell_details_page.click_uninstall_btn()
