import json
import os
from pathlib import Path

import yaml

from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class ServiceDeploymentInstallPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
    ) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

    @async_step("Verify that Service Deployment install page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.service_deployment_install_page.is_loaded(), (
            "Service Deployment Install page should be displayed!"
        )

    @async_step("Click Resource preset button")
    async def ui_click_resource_preset_btn(self) -> None:
        await self._pm.service_deployment_install_page.click_resource_preset_btn()

    @async_step("Verify Resource preset button value")
    async def verify_ui_resource_preset_btn_value(self, expected_value: str) -> None:
        actual_value = (
            await self._pm.service_deployment_install_page.get_resource_preset_value()
        )
        assert actual_value == expected_value, (
            f"Expected Resource preset value to be '{expected_value}' but got '{actual_value}'"
        )

    @async_step("Enter Container image repository value")
    async def ui_enter_container_image_repository_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_image_repository(
            value=value
        )

    @async_step("Verify Container image repository value")
    async def verify_ui_container_image_repository_value(
        self, expected_value: str
    ) -> None:
        actual_value = (
            await self._pm.service_deployment_install_page.get_image_repository_value()
        )
        assert actual_value == expected_value, (
            f"Expected '{expected_value}' but got '{actual_value}'"
        )

    @async_step("Click Container Image Tag checkbox")
    async def ui_click_container_image_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_image_tag_checkbox()

    @async_step("Verify Container Image Tag checkbox value")
    async def verify_ui_container_image_checkbox_value(
        self, expected_value: bool
    ) -> None:
        actual_value = (
            await self._pm.service_deployment_install_page.is_image_tag_checked()
        )
        assert actual_value == expected_value, (
            f"Expected '{expected_value}' but got '{actual_value}'"
        )

    @async_step("Verify Container Image Tag input is displayed")
    async def verify_ui_container_image_input_is_displayed(self) -> None:
        assert await self._pm.service_deployment_install_page.is_get_image_tag_input_displayed(), (
            "Container Image Tag input should be displayed!"
        )

    @async_step("Enter Container image Tag input value")
    async def ui_enter_container_image_input_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_image_tag_input(
            value=value
        )

    @async_step("Select Container Image pull policy")
    async def ui_select_container_image_pull_policy(self, value: str) -> None:
        await self._pm.service_deployment_install_page.select_image_pull_policy(
            value=value
        )

    @async_step("Click Container checkbox")
    async def ui_click_container_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_container_checkbox()

    @async_step("Verify that Container Command checkbox displayed")
    async def verify_ui_container_command_checkbox_displayed(self) -> None:
        assert await self._pm.service_deployment_install_page.is_container_configuration_checkbox_displayed(), (
            "Container Command checkbox should be displayed!"
        )

    @async_step("Verify that Container Arguments checkbox displayed")
    async def verify_ui_container_args_checkbox_displayed(self) -> None:
        assert await self._pm.service_deployment_install_page.is_container_arguments_checkbox_displayed(), (
            "Container Arguments checkbox should be displayed!"
        )

    @async_step("Click Container Arguments checkbox")
    async def ui_click_container_args_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_container_arguments_checkbox()

    @async_step("Verify that Add Entry button for Container Arguments displayed")
    async def verify_ui_cnt_args_add_entry_btn_displayed(self) -> None:
        assert await self._pm.service_deployment_install_page.is_add_container_argument_btn_displayed(), (
            "Add Entry button for Container Arguments should be displayed!"
        )

    @async_step("Click Add Entry button for Container Arguments")
    async def ui_click_cnt_args_add_entry_button(self) -> None:
        await self._pm.service_deployment_install_page.click_add_container_argument_button()

    @async_step("Verify that Container Argument input displayed")
    async def verify_ui_container_argument_input_displayed(self, index: int) -> None:
        assert self._pm.service_deployment_install_page.is_container_argument_input_displayed(
            index=index
        ), f"Container Argument input {index} should be displayed!"

    @async_step("Enter Container Argument input value")
    async def ui_enter_container_argument_value(self, index: int, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_container_argument_input(
            index=index, value=value
        )

    @async_step("Click Network Configuration button")
    async def ui_click_network_configuration_button(self) -> None:
        await self._pm.service_deployment_install_page.click_network_configuration_btn()

    @async_step("Click Enable Authorization and Authentication checkbox")
    async def ui_click_enable_authorization_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_enable_auth_checkbox()

    @async_step("Click Add Entry button for Exposed ports")
    async def ui_click_exp_ports_add_entry_button(self) -> None:
        await self._pm.service_deployment_install_page.click_exposed_ports_add_entry_button()

    @async_step("Enter Exposed Port name")
    async def ui_enter_exposed_port_name(self, index: int, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_exposed_port_name(
            index=index, value=value
        )

    @async_step("Enter Exposed Port number")
    async def ui_enter_exposed_port_number(self, index: int, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_exposed_port_number(
            index=index, value=value
        )

    @async_step("Select Exposed Port path type")
    async def ui_select_exposed_port_path_type(self, index: int, value: str) -> None:
        await self._pm.service_deployment_install_page.select_exposed_port_path_type(
            index=index, value=value
        )

    @async_step("Enter Exposed Port path")
    async def ui_enter_exposed_port_path(self, index: int, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_exposed_port_path(
            index=index, value=value
        )

    @async_step("Click Health Check Probes checkbox")
    async def ui_click_health_check_probes_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_health_check_probes_checkbox()

    @async_step("Click Startup Probe checkbox")
    async def ui_click_startup_probe_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_startup_probe_checkbox()

    @async_step("Enter Startup Probe Initial Delay value")
    async def ui_enter_startup_probe_delay_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_st_prb_initial_delay(
            value=value
        )

    @async_step("Enter Startup Probe Period value")
    async def ui_enter_startup_probe_period_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_st_prb_period(value=value)

    @async_step("Enter Startup Probe Failure Threshold value")
    async def ui_enter_startup_probe_failure_threshold_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_st_prb_failure_threshold(
            value=value
        )

    @async_step("Enter Startup Probe Timeout value")
    async def ui_enter_startup_probe_timeout_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_st_prb_timeout(value=value)

    @async_step("Select Startup Probe Health Check config type")
    async def ui_select_startup_probe_health_check_config_type(
        self, value: str
    ) -> None:
        await self._pm.service_deployment_install_page.select_st_prb_config_type(
            value=value
        )

    @async_step("Enter Startup Probe Health Check port number")
    async def ui_enter_startup_probe_port_number(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_st_prb_http_port(
            value=value
        )

    @async_step("Enter Startup Probe Health Check HTTP Path")
    async def ui_enter_startup_probe_http_path(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_st_prb_http_path(
            value=value
        )

    @async_step("Click Readiness Probe Checkbox")
    async def ui_click_readiness_probe_checkbox(self) -> None:
        await self._pm.service_deployment_install_page.click_readiness_probe_checkbox()

    @async_step("Enter Readiness Probe Initial Delay value")
    async def ui_enter_readiness_probe_delay_value(self, value: str) -> None:
        await (
            self._pm.service_deployment_install_page.enter_rdns_prb_initial_delay_value(
                value=value
            )
        )

    @async_step("Enter Readiness Probe Period value")
    async def ui_enter_readiness_probe_period_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_rdns_prb_period_value(
            value=value
        )

    @async_step("Enter Readiness Probe Failure Threshold value")
    async def ui_enter_readiness_probe_failure_threshold_value(
        self, value: str
    ) -> None:
        await self._pm.service_deployment_install_page.enter_rdns_prb_failure_threshold_value(
            value=value
        )

    @async_step("Enter Readiness Probe Timeout value")
    async def ui_enter_readiness_probe_timeout_value(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_rdns_prb_timeout_value(
            value=value
        )

    @async_step("Select Readiness Probe Health Check config type")
    async def ui_select_readiness_probe_health_check_config_type(
        self, value: str
    ) -> None:
        await self._pm.service_deployment_install_page.select_rdns_prb_config_type(
            value=value
        )

    @async_step("Enter Readiness Probe Health Check port number")
    async def ui_enter_readiness_probe_port_number(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_rdns_prb_http_port_value(
            value=value
        )

    @async_step("Enter Readiness Probe Health Check HTTP Path")
    async def ui_enter_readiness_probe_http_path(self, value: str) -> None:
        await self._pm.service_deployment_install_page.enter_rdns_prb_http_path_value(
            value=value
        )

    @async_step("Enter Service Deployment instance display name")
    async def ui_enter_serv_depl_app_name(self, app_name: str) -> None:
        await self._pm.service_deployment_install_page.enter_app_name(app_name=app_name)

    @async_step("Click Install button")
    async def ui_click_install_btn(self) -> None:
        await self._pm.service_deployment_install_page.click_install_btn()

    @async_step("Verify Export config button enabled")
    async def verify_ui_export_config_btn_enabled(self) -> None:
        assert await self._pm.service_deployment_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be enabled!"
        )

    @async_step("Export app config")
    async def ui_export_config(self) -> str:
        async with (
            self._pm.service_deployment_install_page.page.expect_download() as download_info
        ):
            await self._pm.service_deployment_install_page.click_export_config_btn()
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

        await self._data_manager.app_data.load_app_config_schema("service_deployment")

        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            [config_data]
        )

        assert result, f"Schema validation failed: {error_message}"
