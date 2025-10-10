import logging
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ServiceDeploymentInstallPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_page_heading().is_visible()
            and await self._get_page_title().is_visible()
        )

    def _get_view_container(self) -> BaseElement:
        return BaseElement(
            self.page,
            locator=self.page.locator("h3:text('Service Deployment')")
            .locator("..")
            .locator("..")
            .locator(".."),
        )

    def _get_page_heading(self) -> BaseElement:
        return BaseElement(self.page, "h4", has_text="Service Deployment App")

    def _get_page_title(self) -> BaseElement:
        return BaseElement(self.page, "h3", has_text="Service Deployment")

    def _get_resource_preset_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h4", has_text="Resource Preset")

    def _get_resource_preset_btn(self) -> BaseElement:
        return BaseElement(
            self.page,
            "//p[@class='text-h4' and normalize-space()='Resource Preset']"
            "/following::button[@type='button'][1]",
        )

    async def click_resource_preset_btn(self) -> None:
        self.log("Click Resource Preset button")
        await self._get_resource_preset_btn().click()

    async def get_resource_preset_value(self) -> str:
        btn = self._get_resource_preset_btn()
        text = await btn.locator.inner_text()
        return text.splitlines()[-1].strip()

    def _get_container_image_title(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="Container Image")

    def _get_image_repository_input(self) -> BaseElement:
        return BaseElement(self.page, "input[name='image.repository']")

    async def enter_image_repository(self, value: str) -> None:
        self.log(f"Entering image repository value: {value}")
        await self._get_image_repository_input().fill(value)

    async def get_image_repository_value(self) -> str:
        self.log("Get image repository value")
        element = self._get_image_repository_input()
        return await element.locator.input_value()

    def _get_image_tag_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page,
            by_role="checkbox",
            name="Container Image Tag",
            exact=True,
        )

    async def click_image_tag_checkbox(self) -> None:
        self.log("Click Container Image Tag checkbox")
        await self._get_image_tag_checkbox().click()

    async def is_image_tag_checked(self) -> bool:
        self.log("Check if Container Image Tag checked")
        element = self._get_image_tag_checkbox()
        return await element.locator.is_checked()

    def _get_image_tag_input(self) -> BaseElement:
        return BaseElement(self.page, "input[name='image.tag']")

    async def is_get_image_tag_input_displayed(self) -> bool:
        self.log("Check if Container Image Tag input displayed")
        return await self._get_image_tag_input().is_visible()

    async def enter_image_tag_input(self, value: str) -> None:
        self.log(f"Entering Image Tag input value: {value}")
        await self._get_image_tag_input().fill(value)

    async def get_image_tag_input_value(self) -> str:
        self.log("Get Image Tag input value")
        element = self._get_image_tag_input()
        return await element.locator.input_value()

    def _get_image_pull_secrets_checkbox(self) -> BaseElement:
        return BaseElement(self.page, by_label="ImagePullSecrets for DockerHub")

    async def click_image_pull_secrets_checkbox(self) -> None:
        self.log("Click Image Pull Secrets checkbox")
        await self._get_image_pull_secrets_checkbox().click()

    async def is_get_image_pull_secrets_checked(self) -> bool:
        self.log("Check if Image Pull Secrets checked")
        element = self._get_image_pull_secrets_checkbox()
        return await element.locator.is_checked()

    def _get_image_pull_policy_dropdown(self) -> BaseElement:
        return BaseElement(self.page, "select[name='image.pull_policy']")

    async def select_image_pull_policy(self, value: str) -> None:
        self.log(f"Select Image Pull Policy dropdown value: {value}")
        await self._get_image_pull_policy_dropdown().select_option(value)

    async def get_image_pull_policy_value(self) -> str:
        self.log("Get Image Pull Policy dropdown value")
        element = self._get_image_pull_policy_dropdown()
        return await element.locator.input_value()

    def _get_autoscaling_checkbox(self) -> BaseElement:
        return BaseElement(self.page, by_label="Autoscaling")

    async def click_autoscaling_checkbox(self) -> None:
        self.log("Click Autoscaling checkbox")
        await self._get_autoscaling_checkbox().click()

    async def is_get_autoscaling_checked(self) -> bool:
        self.log("Check if Autoscaling checked")
        element = self._get_autoscaling_checkbox()
        return await element.locator.is_checked()

    def _get_container_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page, "label:has(input[type='checkbox'][label='Container'])"
        )

    async def click_container_checkbox(self) -> None:
        self.log("Click Container checkbox")
        await self._get_container_checkbox().click()

    async def is_get_container_checked(self) -> bool:
        self.log("Check if Container checked")
        element = self._get_container_checkbox()
        return await element.locator.is_checked()

    def _get_container_configuration_title(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="Container Configuration")

    def _get_container_command_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page, by_role="checkbox", name="Container Command", exact=True
        )

    async def is_container_configuration_checkbox_displayed(self) -> bool:
        self.log("Check if Container Configuration checkbox displayed")
        return await self._get_container_command_checkbox().is_visible()

    async def click_container_configuration_checkbox(self) -> None:
        self.log("Click Container Configuration checkbox")
        await self._get_container_configuration_title().click()

    async def is_get_container_configuration_checked(self) -> bool:
        self.log("Check if Container Configuration checked")
        element = self._get_container_configuration_title()
        return await element.locator.is_checked()

    def _get_container_arguments_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page, "label:has(input[type='checkbox'][label='Container Arguments'])"
        )

    async def is_container_arguments_checkbox_displayed(self) -> bool:
        self.log("Check if Container Arguments checkbox displayed")
        return await self._get_container_arguments_checkbox().is_visible()

    async def click_container_arguments_checkbox(self) -> None:
        self.log("Click Container Arguments checkbox")
        await self._get_container_arguments_checkbox().click()
        # self.log("Scrolling")
        # await self.page.locator("div.overflow-auto.bg-gray-100").evaluate(
        #     "el => { el.scrollBy({ top: 600, behavior: 'smooth' }); }"
        # )
        # self.log("Waiting for 1500 ms")
        # await self.page.wait_for_timeout(1500)

    async def is_get_container_arguments_checked(self) -> bool:
        self.log("Check if Container Arguments checked")
        element = self._get_container_arguments_checkbox()
        return await element.locator.is_checked()

    def _get_add_container_argument_button(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector=(
                "//label[normalize-space()='Container Arguments']"
                "/ancestor::div[1]/following-sibling::div"
                "//button[normalize-space()='Add entry']"
            ),
        )

    async def is_add_container_argument_btn_displayed(self) -> bool:
        self.log("Check if Add Container Argument button displayed")
        return await self._get_add_container_argument_button().is_visible()

    async def click_add_container_argument_button(self) -> None:
        self.log("Click Add Container Argument button")
        await self._get_add_container_argument_button().click()

    def _get_container_argument_input(self, index: int) -> BaseElement:
        """
        Returns a BaseElement for the Nth container argument input.
        Index starts from 0 (0 → first input, 1 → second, etc.)
        """
        return BaseElement(
            self.page,
            selector=(
                f"//label[normalize-space()='Container Arguments']"
                f"/ancestor::div[1]/following-sibling::div"
                f"//input[@name='container.args.{index}']"
            ),
        )

    async def is_container_argument_input_displayed(self, index: int) -> bool:
        self.log("Check if Container Argument input displayed")
        return await self._get_container_argument_input(index=index).is_visible()

    async def enter_container_argument_input(self, index: int, value: str) -> None:
        self.log(f"Enter Container Argument input: {value}")
        await self._get_container_argument_input(index).fill(value)

    async def get_container_argument_input_value(self, index: int) -> str:
        self.log(f"Get {index} Container Argument input")
        element = self._get_container_argument_input(index)
        return await element.locator.input_value()

    def _get_environment_variables_section(self) -> BaseElement:
        """
        Returns the 'Environment Variables' section header element.
        """
        return BaseElement(
            self.page,
            selector="//p[normalize-space()='Environment Variables']",
        )

    def _get_env_vars_add_entry_button(self) -> BaseElement:
        """
        Returns the 'Add entry' button inside the 'Environment Variables' section.
        """
        return BaseElement(
            self.page,
            selector=(
                "//p[normalize-space()='Environment Variables']"
                "/ancestor::div[contains(@class, 'mt-6')]"
                "//button[normalize-space()='Add entry']"
            ),
        )

    async def click_add_environment_variables_add_entry_button(self) -> None:
        self.log("Click Add Environment Variables Add Entry button")
        await self._get_env_vars_add_entry_button().click()

    def _get_mount_config_checkbox(self) -> BaseElement:
        """
        Returns the checkbox labeled 'Mount Configuration Data'.
        """
        return BaseElement(
            self.page,
            by_label="Mount Configuration Data",
        )

    async def click_mount_configuration_checkbox(self) -> None:
        self.log("Click Mount Configuration Checkbox")
        await self._get_mount_config_checkbox().click()

    async def is_mount_configuration_checked(self) -> bool:
        self.log("Check if Mount Configuration checked")
        element = self._get_mount_config_checkbox()
        return await element.locator.is_checked()

    def _get_storage_mounts_checkbox(self) -> BaseElement:
        """
        Returns the checkbox labeled 'Storage Mounts'.
        """
        return BaseElement(
            self.page,
            by_label="Storage Mounts",
        )

    async def click_storage_mounts_checkbox(self) -> None:
        self.log("Click Storage Mounts Checkbox")
        await self._get_storage_mounts_checkbox().click()

    async def is_storage_mounts_checked(self) -> bool:
        self.log("Check if Storage Mounts checked")
        element = self._get_storage_mounts_checkbox()
        return await element.locator.is_checked()

    def _get_network_configuration_btn(self) -> BaseElement:
        """
        Returns the collapsible 'Network Configuration' section toggle button.
        """
        return BaseElement(
            self.page,
            selector="//button[@type='button' and .//h6[normalize-space()='Network Configuration']]",
        )

    async def click_network_configuration_btn(self) -> None:
        self.log("Click Network Configuration Button")
        await self._get_network_configuration_btn().click()

    def _get_service_enabled_checkbox(self) -> BaseElement:
        """
        Returns the 'Service Enabled' checkbox element.
        """
        return BaseElement(self.page, by_label="Service Enabled")

    async def click_service_enabled_checkbox(self) -> None:
        self.log("Click Service Enabled Checkbox")
        await self._get_service_enabled_checkbox().click()

    async def is_service_enabled_checked(self) -> bool:
        self.log("Check if Service Enabled checked")
        element = self._get_service_enabled_checkbox()
        return await element.locator.is_checked()

    def _get_http_ingress_checkbox(self) -> BaseElement:
        """
        Returns the 'HTTP Ingress' checkbox element.
        """
        return BaseElement(self.page, by_label="HTTP Ingress")

    async def click_http_ingress_checkbox(self) -> None:
        self.log("Click HTTP Ingress Checkbox")
        await self._get_http_ingress_checkbox().click()

    async def is_http_ingress_checked(self) -> bool:
        self.log("Check if HTTP Ingress checked")
        element = self._get_http_ingress_checkbox()
        return await element.locator.is_checked()

    def _get_enable_http_ingress_heading(self) -> BaseElement:
        """
        Returns the 'Enable HTTP Ingress' section heading.
        """
        return BaseElement(self.page, "p", has_text="Enable HTTP Ingress")

    def _get_enable_auth_checkbox(self) -> BaseElement:
        """
        Returns the 'Enable Authentication and Authorization' checkbox element.
        """
        return BaseElement(
            self.page, by_label="Enable Authentication and Authorization"
        )

    async def click_enable_auth_checkbox(self) -> None:
        self.log("Click Enable Authentication and Authorization Checkbox")
        element = self._get_enable_auth_checkbox()
        if await element.is_visible():
            await element.click()
        else:
            self.log(
                "Enable Authentication and Authorization Checkbox is missing. Older design. Continue...",
                level=logging.WARNING,
            )

    async def is_enable_auth_checked(self) -> bool:
        self.log("Check if Enable Authentication and Authorization Checkbox")
        element = self._get_enable_auth_checkbox()
        return await element.locator.is_checked()

    def _get_exposed_ports_heading(self) -> BaseElement:
        """
        Returns the 'Exposed Ports' section heading element.
        """
        return BaseElement(self.page, "p", has_text="Exposed Ports")

    def _get_exposed_ports_add_entry_button(self) -> BaseElement:
        """
        Returns the 'Add entry' button inside the 'Exposed Ports' section.
        """
        return BaseElement(
            self.page,
            selector="//p[normalize-space()='Exposed Ports']"
            "/ancestor::div[1]//button[normalize-space()='Add entry']",
        )

    async def click_exposed_ports_add_entry_button(self) -> None:
        self.log("Click Exposed Port Add Entry Button")
        await self._get_exposed_ports_add_entry_button().click()

    def _get_exposed_port_name_input(self, index: int = 0) -> BaseElement:
        """
        Returns the 'Port Name' input field inside the Exposed Ports section.

        Parameters
        ----------
        index : int
            The port index (e.g. 0, 1, 2...). Defaults to 0.
        """
        return BaseElement(
            self.page,
            selector=f'input[name="networking.ports.{index}.name"]',
        )

    async def enter_exposed_port_name(self, value: str, index: int = 0) -> None:
        self.log(f"Enter Exposed Port Name Input: {value}")
        await self._get_exposed_port_name_input(index=index).fill(value)

    async def get_exposed_port_name_value(self, index: int = 0) -> str:
        self.log("Get Exposed Port Name Value")
        element = self._get_exposed_port_name_input(index=index)
        return await element.locator.input_value()

    def _get_exposed_port_number_input(self, index: int = 0) -> BaseElement:
        """
        Returns the 'Port Number' input field inside the Exposed Ports section.

        Parameters
        ----------
        index : int
            The port index (e.g., 0, 1, 2...). Defaults to 0.
        """
        return BaseElement(
            self.page,
            selector=f'input[name="networking.ports.{index}.port"]',
        )

    async def enter_exposed_port_number(self, value: str, index: int = 0) -> None:
        self.log(f"Enter Exposed Port Number Input: {value}")
        await self._get_exposed_port_number_input(index=index).fill(value)

    async def get_exposed_port_number_value(self, index: int = 0) -> str:
        self.log("Get Exposed Port Number Value")
        element = self._get_exposed_port_number_input(index=index)
        return await element.locator.input_value()

    def _get_exposed_port_path_type_dropdown(self, index: int = 0) -> BaseElement:
        """
        Returns the 'Path Type' dropdown inside the Exposed Ports section.

        Parameters
        ----------
        index : int
            The port index (e.g., 0, 1, 2...). Defaults to 0.
        """
        return BaseElement(
            self.page,
            selector=f'select[name="networking.ports.{index}.path_type"]',
        )

    async def select_exposed_port_path_type(self, value: str, index: int = 0) -> None:
        self.log(f"Select Exposed Port Path Type: {value}")
        await self._get_exposed_port_path_type_dropdown(index=index).select_option(
            value
        )

    async def get_exposed_port_path_type_value(self, index: int = 0) -> str:
        self.log("Get Exposed Port Path Type Value")
        element = self._get_exposed_port_path_type_dropdown(index=index)
        return await element.locator.input_value()

    def _get_exposed_port_path_input(self, index: int = 0) -> BaseElement:
        """
        Returns the 'Path' input field inside the Exposed Ports section.

        Parameters
        ----------
        index : int
            The port index (e.g., 0, 1, 2...). Defaults to 0.
        """
        return BaseElement(
            self.page,
            selector=f'input[name="networking.ports.{index}.path"]',
        )

    async def enter_exposed_port_path(self, value: str, index: int = 0) -> None:
        self.log(f"Enter Exposed Port Path Input: {value}")
        await self._get_exposed_port_path_input(index=index).fill(value)

    async def get_exposed_port_path_value(self, index: int = 0) -> str:
        self.log("Get Exposed Port Path Value")
        element = self._get_exposed_port_path_input(index=index)
        return await element.locator.input_value()

    def _get_health_check_probes_checkbox(self) -> BaseElement:
        """
        Returns the 'Health Check Probes' checkbox element.
        """
        return BaseElement(
            self.page,
            selector="label:has(input[type='checkbox'][label='Health Check Probes'])",
        )

    async def click_health_check_probes_checkbox(self) -> None:
        self.log("Click Health Check Probes Checkbox")
        await self._get_health_check_probes_checkbox().click()

    async def is_health_check_probes_checked(self) -> bool:
        self.log("Is Health Check Probes Checked")
        element = self._get_health_check_probes_checkbox()
        return await element.locator.is_checked()

    def _get_health_check_probes_title(self) -> BaseElement:
        """
        Returns the 'Health Check Probes' section title element.
        """
        return BaseElement(
            self.page,
            "p",
            has_text="Health Check Probes",
        )

    def _get_startup_probe_checkbox(self) -> BaseElement:
        """
        Returns the 'Startup Probe' checkbox element.
        """
        return BaseElement(
            self.page,
            selector="label:has(input[type='checkbox'][label='Startup Probe'])",
        )

    async def click_startup_probe_checkbox(self) -> None:
        self.log("Click Startup Probe Checkbox")
        await self._get_startup_probe_checkbox().click()

    async def is_startup_probe_checkbox_checked(self) -> bool:
        self.log("Is Startup Probe Checkbox Checked")
        element = self._get_startup_probe_checkbox()
        return await element.locator.is_checked()

    def _get_st_prb_initial_delay_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.startup.initial_delay']"
        )

    async def enter_st_prb_initial_delay(self, value: str) -> None:
        self.log(f"Enter Start up Delay Input: {value}")
        await self._get_st_prb_initial_delay_input().fill(value)

    async def get_st_prb_initial_delay_value(self) -> str:
        self.log("Get Start up Delay Value")
        element = self._get_st_prb_initial_delay_input()
        return await element.locator.input_value()

    def _get_st_prb_period_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.startup.period']"
        )

    async def enter_st_prb_period(self, value: str) -> None:
        self.log(f"Enter Start up Period Input: {value}")
        await self._get_st_prb_period_input().fill(value)

    async def get_st_prb_period_value(self) -> str:
        self.log("Get Start up Period Value")
        element = self._get_st_prb_period_input()
        return await element.locator.input_value()

    def _get_st_prb_failure_threshold_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.startup.failure_threshold']",
        )

    async def enter_st_prb_failure_threshold(self, value: str) -> None:
        self.log(f"Enter Start up Failure Threshold Input: {value}")
        await self._get_st_prb_failure_threshold_input().fill(value)

    async def get_st_prb_failure_threshold_value(self) -> str:
        self.log("Get Start up Failure Threshold Value")
        element = self._get_st_prb_failure_threshold_input()
        return await element.locator.input_value()

    def _get_st_prb_timeout_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.startup.timeout']"
        )

    async def enter_st_prb_timeout(self, value: str) -> None:
        self.log(f"Enter Start up Timeout Input: {value}")
        await self._get_st_prb_timeout_input().fill(value)

    async def get_st_prb_timeout_value(self) -> str:
        self.log("Get Start up Timeout Value")
        element = self._get_st_prb_timeout_input()
        return await element.locator.input_value()

    def _get_st_prb_config_dropdown(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//label[.//span[normalize-space()='Startup Probe']]/following::select[1]",
        )

    async def select_st_prb_config_type(self, value: str) -> None:
        self.log(f"Select Startup Probe Health Check Config Type: {value}")
        await self._get_st_prb_config_dropdown().select_option(value)

    async def get_st_prb_config_value(self) -> str:
        self.log("Get Startup Probe Health Check Config Value")
        element = self._get_st_prb_config_dropdown()
        return await element.locator.input_value()

    def _get_st_prb_http_port_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.startup.health_check_config.port']",
        )

    async def enter_st_prb_http_port(self, value: str) -> None:
        self.log(f"Enter Startup Health Check HTTP Port: {value}")
        await self._get_st_prb_http_port_input().fill(value)

    async def get_st_prb_http_port_value(self) -> str:
        self.log("Get Startup Health Check HTTP Port Value")
        element = self._get_st_prb_http_port_input()
        return await element.locator.input_value()

    def _get_st_prb_http_path_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.startup.health_check_config.path']",
        )

    async def enter_st_prb_http_path(self, value: str) -> None:
        self.log(f"Enter Startup Health Check HTTP Path: {value}")
        await self._get_st_prb_http_path_input().fill(value)

    async def get_st_prb_http_path_value(self) -> str:
        self.log("Get Startup Health Check HTTP Path Value")
        element = self._get_st_prb_http_path_input()
        return await element.locator.input_value()

    def _get_st_prb_http_headers_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector=(
                "//label[.//span[normalize-space()='Startup Probe']]"
                "/following::label[.//span[normalize-space()='HTTP Headers']][1]//input"
            ),
        )

    async def click_st_prb_http_headers_checkbox(self) -> None:
        await self._get_st_prb_http_headers_checkbox().click()

    async def is_st_prb_http_headers_checked(self) -> str:
        self.log("Is Startup Probe HTTP Headers Checked")
        element = self._get_st_prb_http_headers_checkbox()
        return await element.locator.input_value()

    def _get_liveness_probe_checkbox(self) -> BaseElement:
        """
        Returns the 'Liveness Probe' checkbox element.
        """
        return BaseElement(
            self.page,
            selector="label:has(input[type='checkbox'][label='Liveness Probe'])",
        )

    async def click_liveness_probe_checkbox(self) -> None:
        await self._get_liveness_probe_checkbox().click()

    async def is_liveness_probe_checkbox_checked(self) -> str:
        self.log("Is Liveness Probe Checkbox Checked")
        element = self._get_liveness_probe_checkbox()
        return await element.locator.input_value()

    def _get_liv_prb_initial_delay_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.liveness.initial_delay']"
        )

    async def enter_liv_prb_initial_delay(self, value: str) -> None:
        self.log(f"Enter Liveness Probe Initial Delay: {value}")
        await self._get_liv_prb_initial_delay_input().fill(value)

    async def get_liv_prb_initial_delay_value(self) -> str:
        self.log("Get Liveness Probe Initial Delay Value")
        element = self._get_liv_prb_initial_delay_input()
        return await element.locator.input_value()

    def _get_liv_prb_period_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.liveness.period']"
        )

    async def enter_liv_prb_period_value(self, value: str) -> None:
        self.log(f"Enter Liveness Probe Period: {value}")
        await self._get_liv_prb_period_input().fill(value)

    async def get_liv_prb_period_value(self) -> str:
        self.log("Get Liveness Probe Period Value")
        element = self._get_liv_prb_period_input()
        return await element.locator.input_value()

    def _get_liv_prb_failure_threshold_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.liveness.failure_threshold']",
        )

    async def enter_liv_prb_failure_threshold_value(self, value: str) -> None:
        self.log(f"Enter Liveness Probe Failure Threshold: {value}")
        await self._get_liv_prb_failure_threshold_input().fill(value)

    async def get_liv_prb_failure_threshold_value(self) -> str:
        self.log("Get Liveness Probe Failure Threshold Value")
        element = self._get_liv_prb_failure_threshold_input()
        return await element.locator.input_value()

    def _get_liv_prb_timeout_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.liveness.timeout']"
        )

    async def enter_liv_prb_timeout_value(self, value: str) -> None:
        self.log(f"Enter Liveness Probe Timeout: {value}")
        await self._get_liv_prb_timeout_input().fill(value)

    async def get_liv_prb_timeout_value(self) -> str:
        self.log("Get Liveness Probe Timeout Value")
        element = self._get_liv_prb_timeout_input()
        return await element.locator.input_value()

    def _get_liv_prb_config_dropdown(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//label[.//span[normalize-space()='Liveness Probe']]/following::select[1]",
        )

    async def select_liv_prb_config(self, value: str) -> None:
        self.log(f"Select Liveness Probe HTTP Health Check Config: {value}")
        await self._get_liv_prb_config_dropdown().select_option(value)

    async def get_liv_prb_config_type_value(self) -> str:
        self.log("Get Liveness Probe HTTP Health Check Config Type")
        element = self._get_liv_prb_config_dropdown()
        return await element.locator.input_value()

    def _get_liv_prb_http_port_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.liveness.health_check_config.port']",
        )

    async def enter_liv_prb_http_port_value(self, value: str) -> None:
        self.log(f"Enter Liveness Probe HTTP Health Check Port: {value}")
        await self._get_liv_prb_http_port_input().fill(value)

    async def get_liv_prb_http_port_value(self) -> str:
        self.log("Get Liveness Probe HTTP Health Check Port")
        element = self._get_liv_prb_http_port_input()
        return await element.locator.input_value()

    def _get_liv_prb_http_path_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.liveness.health_check_config.path']",
        )

    async def enter_liv_prb_http_path_value(self, value: str) -> None:
        self.log(f"Enter Liveness Probe HTTP Health Check Path: {value}")
        await self._get_liv_prb_http_path_input().fill(value)

    async def get_liv_prb_http_path_value(self) -> str:
        self.log("Get Liveness Probe HTTP Health Check Path")
        element = self._get_liv_prb_http_path_input()
        return await element.locator.input_value()

    def _get_liv_prb_http_headers_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector=(
                "//label[.//span[normalize-space()='Liveness Probe']]"
                "/following::label[.//span[normalize-space()='HTTP Headers']][1]//input"
            ),
        )

    async def click_liv_prb_http_headers_checkbox(self) -> None:
        self.log("Click Liveness Probe HTTP Health Check Headers Checkbox")
        await self._get_liv_prb_http_headers_checkbox().click()

    async def is_liv_prb_http_headers_checked(self) -> bool:
        self.log("Is Liveness Probe HTTP Health Check Checked")
        element = self._get_liv_prb_http_headers_checkbox()
        return await element.locator.is_checked()

    def _get_readiness_probe_checkbox(self) -> BaseElement:
        """
        Returns the 'Readiness Probe' checkbox element.
        """
        return BaseElement(
            self.page,
            selector="label:has(input[type='checkbox'][label='Readiness Probe'])",
        )

    async def click_readiness_probe_checkbox(self) -> None:
        self.log("Click Readiness Probe Checkbox")
        await self._get_readiness_probe_checkbox().click()

    async def is_readiness_probe_checked(self) -> bool:
        self.log("Is Readiness Probe Checked")
        element = self._get_readiness_probe_checkbox()
        return await element.locator.is_checked()

    def _get_rdns_prb_initial_delay_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.readiness.initial_delay']"
        )

    async def enter_rdns_prb_initial_delay_value(self, value: str) -> None:
        self.log(f"Enter Readiness Probe Initial Delay: {value}")
        await self._get_rdns_prb_initial_delay_input().fill(value)

    async def get_rdns_prb_initial_delay_value(self) -> str:
        self.log("Get Readiness Probe Initial Delay")
        element = self._get_rdns_prb_initial_delay_input()
        return await element.locator.input_value()

    def _get_rdns_prb_period_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.readiness.period']"
        )

    async def enter_rdns_prb_period_value(self, value: str) -> None:
        self.log(f"Enter Readiness Probe Period: {value}")
        await self._get_rdns_prb_period_input().fill(value)

    async def get_rdns_prb_period_value(self) -> str:
        self.log("Get Readiness Probe Period")
        element = self._get_rdns_prb_period_input()
        return await element.locator.input_value()

    def _get_rdns_prb_failure_threshold_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.readiness.failure_threshold']",
        )

    async def enter_rdns_prb_failure_threshold_value(self, value: str) -> None:
        self.log(f"Enter Readiness Probe Failure Threshold: {value}")
        await self._get_rdns_prb_failure_threshold_input().fill(value)

    async def get_rdns_prb_failure_threshold_value(self) -> str:
        self.log("Get Readiness Probe Failure Threshold")
        element = self._get_rdns_prb_failure_threshold_input()
        return await element.locator.input_value()

    def _get_rdns_prb_timeout_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='health_checks.readiness.timeout']"
        )

    async def enter_rdns_prb_timeout_value(self, value: str) -> None:
        self.log(f"Enter Readiness Probe Timeout: {value}")
        await self._get_rdns_prb_timeout_input().fill(value)

    async def get_rdns_prb_timeout_value(self) -> str:
        self.log("Get Readiness Probe Timeout")
        element = self._get_rdns_prb_timeout_input()
        return await element.locator.input_value()

    def _get_rdns_prb_config_dropdown(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//label[.//span[normalize-space()='Readiness Probe']]/following::select[1]",
        )

    async def select_rdns_prb_config_type(self, value: str) -> None:
        self.log(f"Select Readiness Probe HTTP Health Check Config Type: {value}")
        await self._get_rdns_prb_config_dropdown().select_option(value)

    async def get_rdns_prb_config_type(self) -> str:
        self.log("Get Readiness Probe HTTP Health Check Config")
        element = self._get_rdns_prb_config_dropdown()
        return await element.locator.input_value()

    def _get_rdns_prb_http_port_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.readiness.health_check_config.port']",
        )

    async def enter_rdns_prb_http_port_value(self, value: str) -> None:
        self.log(f"Enter Readiness Probe HTTP Health Check Port: {value}")
        await self._get_rdns_prb_http_port_input().fill(value)

    async def get_rdns_prb_http_port_value(self) -> str:
        self.log("Get Readiness Probe HTTP Health Check Port")
        element = self._get_rdns_prb_http_port_input()
        return await element.locator.input_value()

    def _get_rdns_prb_http_path_input(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//input[@name='health_checks.readiness.health_check_config.path']",
        )

    async def enter_rdns_prb_http_path_value(self, value: str) -> None:
        self.log(f"Enter Readiness Probe HTTP Path: {value}")
        await self._get_rdns_prb_http_path_input().fill(value)

    async def get_rdns_prb_http_path_value(self) -> str:
        self.log("Get Readiness Probe HTTP Path")
        element = self._get_rdns_prb_http_path_input()
        return await element.locator.input_value()

    def _get_rdns_prb_http_headers_checkbox(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector=(
                "//label[.//span[normalize-space()='Readiness Probe']]"
                "/following::label[.//span[normalize-space()='HTTP Headers']][1]//input"
            ),
        )

    async def click_rdns_prb_http_headers_checkbox(self) -> None:
        self.log("Click Readiness Probe HTTP Headers Checkbox")
        await self._get_rdns_prb_http_headers_checkbox().click()

    async def is_rdns_prb_http_headers_checked(self) -> bool:
        self.log("Is Readiness Probe HTTP Headers Checked")
        element = self._get_rdns_prb_http_headers_checkbox()
        return await element.locator.is_checked()

    def _get_metadata_label(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="Metadata")

    def _get_display_name_input(self) -> BaseElement:
        return BaseElement(self.page, '[name="displayName"]')

    async def enter_app_name(self, app_name: str) -> None:
        self.log(f"Entering {app_name} app name")
        await self._get_display_name_input().fill(app_name)

    async def get_display_name_value(self) -> str:
        display_name_input = self._get_display_name_input()
        return await display_name_input.locator.input_value()

    def _get_install_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Install")

    async def click_install_btn(self) -> None:
        self.log("Click Install button")
        await self._get_install_btn().click()
        spinner_selector = "button:has-text('Install') div.chase-spinner"
        await self.wait_for_spinner(spinner_selector=spinner_selector, timeout=30000)

    def _get_export_config_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Download parameters")

    async def is_export_config_btn_enabled(self) -> bool:
        return await self._get_export_config_btn().is_enabled()

    async def click_export_config_btn(self) -> None:
        self.log("Click Export config button")
        await self._get_export_config_btn().click()

    def _get_import_config_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Import App Configuration")

    async def is_import_config_btn_enabled(self) -> bool:
        return await self._get_import_config_btn().is_enabled()

    async def click_import_config_btn(self) -> None:
        self.log("Click Import config button")
        await self._get_import_config_btn().click()
