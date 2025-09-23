from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ShellAppPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Shell app page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.shell_app_page.is_loaded(), (
            "Shell app page should be displayed!"
        )

    @async_step("Open Shell app page")
    async def ui_open_shell_app_page(self, url: str) -> None:
        await self._pm.shell_app_page.open_app(url=url)

    @async_step("Enter command inside shell app page")
    async def ui_enter_command_in_shell(self, command: str) -> None:
        await self._pm.shell_app_page.enter_command(command=command)

    @async_step("Verify executed command displayed in shell output")
    async def verify_ui_executed_command_in_shell_output(self, command: str) -> None:
        assert await self._pm.shell_app_page.check_output_line(value=command), (
            f"No line with: {command}"
        )

    @async_step("Verify User configuration displayed in shell output")
    async def verify_ui_user_config_in_shell_output(
        self, org_name: str, proj_name: str
    ) -> None:
        assert await self._pm.shell_app_page.check_output_line(
            value="User Configuration:"
        ), "No User Configuration line"

        org_line = f"Current Org {org_name}"
        assert await self._pm.shell_app_page.check_output_line(value=org_line), (
            f"No Org line found for {org_line}"
        )

        proj_line = f"Current Project {proj_name}"
        assert await self._pm.shell_app_page.check_output_line(value=proj_line), (
            f"No Project line found for {proj_line}"
        )

    @async_step("Verify Resource Presets displayed in shell output")
    async def verify_ui_res_presets_in_shell_output(self) -> None:
        assert await self._pm.shell_app_page.check_output_line(
            value="Resource Presets:"
        ), "No Resource Presets line"

        assert await self._pm.shell_app_page.check_output_line(value="cpu-medium"), (
            "No preset line found for cpu-medium"
        )

        assert await self._pm.shell_app_page.check_output_line(value="cpu-large"), (
            "No preset line found for cpu-large"
        )
