import json
import os
from pathlib import Path

import yaml

from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class PostgresInstallPageSteps:
    def __init__(self, page_manager: PageManager, data_manager: DataManager) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

    @async_step("Verify that Postgres install page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.postgres_install_page.is_loaded(), (
            "Postgres Install page should be displayed!"
        )

    @async_step("Click Resource preset button")
    async def ui_click_resource_preset_btn(self) -> None:
        await self._pm.postgres_install_page.click_resource_preset_btn()

    @async_step("Verify Resource preset value")
    async def verify_ui_resource_preset_value(self, expected_value: str) -> None:
        actual_value = await self._pm.postgres_install_page.get_resource_preset_value()
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Enter Postgres replicas count")
    async def ui_enter_postgres_replicas_count(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_postgres_replicas_count(value=value)

    @async_step("Verify Postgres replicas count value")
    async def verify_ui_postgres_replicas_value(self, expected_value: str) -> None:
        actual_value = (
            await self._pm.postgres_install_page.get_postgres_replicas_value()
        )
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Click Add database user button")
    async def ui_click_add_database_user_btn(self) -> None:
        await self._pm.postgres_install_page.click_add_database_user_btn()

    @async_step("Verify that Postgres User name input displayed")
    async def verify_ui_postgres_username_input_displayed(self) -> None:
        assert (
            await self._pm.postgres_install_page.is_postgres_user_name_input_displayed()
        ), "Postgres User name input should be displayed!"

    @async_step("Enter Postgres User name")
    async def ui_enter_postgres_username(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_postgres_user_name(value=value)

    @async_step("Verify that Postgres user name value")
    async def verify_ui_postgres_username_value(self, expected_value: str) -> None:
        actual_value = (
            await self._pm.postgres_install_page.get_postgres_user_name_value()
        )
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Verify that Add User Database button displayed")
    async def verify_ui_add_postgres_user_db_btn_displayed(self) -> None:
        assert (
            await self._pm.postgres_install_page.is_add_database_name_button_displayed()
        ), "Add Postgres User Databese button should be displayed!"

    @async_step("Click Add Postgres User Database button")
    async def ui_click_add_postgres_user_db_btn(self) -> None:
        await self._pm.postgres_install_page.click_add_database_name_button()

    @async_step("Verify that User Database name input displayed")
    async def verify_ui_postgres_user_db_input_displayed(self) -> None:
        assert (
            await self._pm.postgres_install_page.is_postgres_db_name_input_displayed()
        ), "Postgres User Database name input should be displayed!"

    @async_step("Enter Postgres User Database name")
    async def ui_enter_postgres_user_db_name(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_postgres_db_name(value=value)

    @async_step("Verify Postgres User Database name value")
    async def verify_ui_postgres_user_db_name_value(self, expected_value: str) -> None:
        actual_value = await self._pm.postgres_install_page.get_postgres_db_name_value()
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Click PG Bouncer Resource Preset button")
    async def ui_click_pg_bouncer_resource_preset_btn(self) -> None:
        await self._pm.postgres_install_page.click_pg_bouncer_resource_preset_btn()

    @async_step("Verify PG Bouncer Resource preset value")
    async def verify_pg_bouncer_resource_preset_value(
        self, expected_value: str
    ) -> None:
        actual_value = (
            await self._pm.postgres_install_page.get_pg_bouncer_resource_preset_value()
        )
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Enter PG Bouncer replicas count")
    async def ui_enter_pg_bouncer_replicas_count(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_pg_bouncer_replicas_count(
            value=value
        )

    @async_step("Verify PG Bouncer replicas count value")
    async def verify_ui_pg_bouncer_replicas_count(self, expected_value: str) -> None:
        actual_value = (
            await self._pm.postgres_install_page.get_pg_bouncer_replicas_value()
        )
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Enter Postgres Display name")
    async def ui_enter_postgres_display_name(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_display_name(value=value)

    @async_step("Verify Postgres Display name value")
    async def verify_ui_postgres_display_name_value(self, expected_value: str) -> None:
        actual_value = await self._pm.postgres_install_page.get_display_name_value()
        assert actual_value == expected_value, (
            f"Expected: {expected_value}, got: {actual_value}"
        )

    @async_step("Click Install button")
    async def ui_click_install_btn(self) -> None:
        await self._pm.postgres_install_page.click_install_btn()

    @async_step("Verify Export config button enabled")
    async def verify_ui_export_config_btn_enabled(self) -> None:
        assert await self._pm.postgres_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be enabled!"
        )

    @async_step("Click Import config button")
    async def ui_click_import_config_btn(self) -> None:
        await self._pm.postgres_install_page.click_import_config_btn()

    @async_step("Get PostgreSQL app import config file path")
    async def get_import_config_file_path(self) -> str:
        return await self._data_manager.app_data.get_app_import_config_file_path(
            app_name="postgres"
        )

    @async_step("Export app config")
    async def ui_export_config(self) -> str:
        async with (
            self._pm.postgres_install_page.page.expect_download() as download_info
        ):
            await self._pm.postgres_install_page.click_export_config_btn()
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

        await self._data_manager.app_data.load_app_config_schema("postgres")

        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            [config_data]
        )

        assert result, f"Schema validation failed: {error_message}"

    @async_step("Verify exported config file data")
    async def verify_exported_config_data(
        self,
        config_file_path: str,
        display_name: str,
        res_preset: str,
        postgres_repl: str,
        postgres_user: str,
        postgres_db: str,
        pg_res_preset: str,
        pg_repl: str,
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

        errors: list[str] = []

        display_name_val = config_data.get("display_name")
        if display_name_val != display_name:
            errors.append(
                f"display_name mismatch: expected '{display_name}', got '{display_name_val}'"
            )

        preset_val = config_data.get("input", {}).get("preset", {}).get("name")
        if preset_val != res_preset:
            errors.append(
                f"preset mismatch: expected '{res_preset}', got '{preset_val}'"
            )

        postgres_repl_val = str(
            config_data.get("input", {})
            .get("postgres_config", {})
            .get("instance_replicas")
        )
        if postgres_repl_val != postgres_repl:
            errors.append(
                f"postgres instance_replicas mismatch: expected '{postgres_repl}', got '{postgres_repl_val}'"
            )

        db_users = (
            config_data.get("input", {}).get("postgres_config", {}).get("db_users", [])
        )
        if not db_users or not isinstance(db_users, list):
            errors.append("db_users missing or not a list")
        else:
            user_name_val = db_users[0].get("name")
            if user_name_val != postgres_user:
                errors.append(
                    f"postgres user mismatch: expected '{postgres_user}', got '{user_name_val}'"
                )

            db_names_val = db_users[0].get("db_names", [])
            if postgres_db not in db_names_val:
                errors.append(
                    f"postgres db mismatch: expected '{postgres_db}' in {db_names_val}"
                )

        pg_repl_val = str(
            config_data.get("input", {}).get("pg_bouncer", {}).get("replicas")
        )
        if pg_repl_val != pg_repl:
            errors.append(
                f"pg_bouncer replicas mismatch: expected '{pg_repl}', got '{pg_repl_val}'"
            )

        pg_preset_val = (
            config_data.get("input", {})
            .get("pg_bouncer", {})
            .get("preset", {})
            .get("name")
        )
        if pg_preset_val != pg_res_preset:
            errors.append(
                f"pg_bouncer preset mismatch: expected '{pg_res_preset}', got '{pg_preset_val}'"
            )

        if errors:
            raise AssertionError("❌ Config validation failed:\n" + "\n".join(errors))
