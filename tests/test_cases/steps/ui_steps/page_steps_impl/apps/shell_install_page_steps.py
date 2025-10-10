import json
import os
from pathlib import Path

import yaml

from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class ShellInstallPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
    ) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

    @async_step("Verify that Shell install page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.shell_install_page.is_loaded(), (
            "Shell Install page should be displayed!"
        )

    @async_step("Click Resource preset button")
    async def ui_click_resource_preset_btn(self) -> None:
        await self._pm.shell_install_page.click_resource_preset_btn()

    @async_step("Verify Resource preset button value")
    async def verify_ui_resource_preset_btn_value(self, expected_value: str) -> None:
        actual_value = await self._pm.shell_install_page.get_resource_preset_value()
        assert actual_value == expected_value, (
            f"Expected Resource preset value to be '{expected_value}' but got '{actual_value}'"
        )

    @async_step("Select Auth type")
    async def ui_select_auth_type(self, value: str) -> None:
        await self._pm.shell_install_page.select_auth_type(value=value)

    @async_step("Verify value of Auth type")
    async def verify_ui_auth_type(self, expected_value: str) -> None:
        actual_value = await self._pm.shell_install_page.get_auth_type_value()
        assert actual_value == expected_value, (
            f"Expected Auth type to be '{expected_value}' but got '{actual_value}'"
        )

    @async_step("Enter Shell instance display name")
    async def ui_enter_shell_app_name(self, app_name: str) -> None:
        await self._pm.shell_install_page.enter_app_name(app_name=app_name)

    @async_step("Verify Display name value")
    async def verify_ui_display_name_value(self, expected_value: str) -> None:
        actual_value = await self._pm.shell_install_page.get_display_name_value()
        assert actual_value == expected_value, (
            f"Expected Display name '{expected_value}' but got '{actual_value}'"
        )

    @async_step("Click Install button")
    async def ui_click_install_btn(self) -> None:
        await self._pm.shell_install_page.click_install_btn()

    @async_step("Verify Export config button disabled")
    async def verify_ui_export_config_btn_disabled(self) -> None:
        assert not await self._pm.shell_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be disabled!"
        )

    @async_step("Verify Export config button enabled")
    async def verify_ui_export_config_btn_enabled(self) -> None:
        assert await self._pm.shell_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be enabled!"
        )

    @async_step("Export app config")
    async def ui_export_config(self) -> str:
        async with self._pm.shell_install_page.page.expect_download() as download_info:
            await self._pm.shell_install_page.click_export_config_btn()
        download = await download_info.value

        file_path = os.path.join(
            self._data_manager.download_path, download.suggested_filename
        )
        await download.save_as(file_path)
        await self._pm.page.wait_for_timeout(2000)
        return file_path

    @async_step("Verify exported config file schema")
    async def verify_exported_config_schema(self, config_file_path: str) -> None:
        config_file = Path(config_file_path)
        if not config_file.exists():
            raise AssertionError(f"Config file not found: {config_file_path}")

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                if config_file.suffix in [".yaml", ".yml"]:
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
        except Exception as e:
            raise AssertionError(f"Failed to parse config file {config_file_path}: {e}")

        if not isinstance(config_data, dict):
            raise AssertionError(
                f"Config file must be a mapping/dict, got {type(config_data)}"
            )

        await self._data_manager.app_data.load_app_config_schema("shell")

        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            [config_data]
        )

        assert result, f"Schema validation failed: {error_message}"

    @async_step("Verify exported config file data")
    async def verify_exported_config_data(
        self, display_name: str, preset: str, http_auth: bool, config_file_path: str
    ) -> None:
        config_file = Path(config_file_path)
        if not config_file.exists():
            raise AssertionError(f"Config file not found: {config_file_path}")

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                if config_file.suffix in [".yaml", ".yml"]:
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
        except Exception as e:
            raise AssertionError(f"Failed to parse config file {config_file_path}: {e}")

        if not isinstance(config_data, dict):
            raise AssertionError(f"Config file must be a dict, got {type(config_data)}")

        errors = []

        if config_data.get("display_name") != display_name:
            errors.append(
                f"display_name mismatch: expected '{display_name}', got '{config_data.get('display_name')}'"
            )

        preset_val = config_data.get("input", {}).get("preset", {}).get("name")
        if preset_val != preset:
            errors.append(f"preset mismatch: expected '{preset}', got '{preset_val}'")

        http_auth_val = (
            config_data.get("input", {}).get("networking", {}).get("http_auth")
        )
        if http_auth_val != http_auth:
            errors.append(
                f"http_auth mismatch: expected '{http_auth}', got '{http_auth_val}'"
            )

        if errors:
            raise AssertionError("Config validation failed:\n" + "\n".join(errors))

    @async_step("Get Shell app import config file path")
    async def get_import_config_file_path(self) -> str:
        return await self._data_manager.app_data.get_app_import_config_file_path(
            app_name="shell"
        )

    @async_step("Verify Import config button enabled")
    async def verify_ui_import_config_btn_enabled(self) -> None:
        assert await self._pm.shell_install_page.is_import_config_btn_enabled(), (
            "Import Config button should be enabled!"
        )

    @async_step("Click Import config button")
    async def ui_click_import_config_btn(self) -> None:
        await self._pm.shell_install_page.click_import_config_btn()
