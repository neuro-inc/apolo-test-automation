import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.api_steps.api_steps import APISteps
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("Service Deployment App", parent="E2E Tests")
@pytest.mark.flaky(reruns=0)
@pytest.mark.class_setup
class TestE2EServiceDeploymentApp(BaseTestClass):
    serv_depl_app_name = ""
    serv_depl_app_id = ""
    org_name = ""
    proj_name = ""
    app_install_status = False

    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        ui_steps = await self.init_ui_test_steps()
        api_steps = await self.init_api_test_steps()
        self._ui_steps: UISteps = ui_steps
        self._api_steps: APISteps = api_steps

    @pytest.fixture
    def serv_depl_status(self) -> None:
        if not TestE2EServiceDeploymentApp.app_install_status:
            pytest.skip("Service Deployment app was not installed successfully")

    @async_title("Install Service Deployment app via UI")
    @pytest.mark.order(1)
    @pytest.mark.timeout(700)
    async def test_install_app_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.

        ### Verify that:

        - User can install `Service Deployment` app via **UI**.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user)
        await ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        TestE2EServiceDeploymentApp.org_name = org.org_name
        proj = org.add_project(gherkin_name="Default-project")
        TestE2EServiceDeploymentApp.proj_name = proj.project_name
        await ui_steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )

        await ui_steps.main_page.verify_ui_serv_depl_container_displayed()

        await ui_steps.main_page.ui_serv_depl_container_click_install_btn()
        await ui_steps.service_deployment_install_page.verify_ui_page_displayed()

        await ui_steps.service_deployment_install_page.ui_click_resource_preset_btn()
        await ui_steps.resource_preset_popup.verify_ui_popup_displayed()

        await ui_steps.resource_preset_popup.ui_select_cpu_micro_preset()
        await ui_steps.resource_preset_popup.ui_click_apply_button()
        await ui_steps.resource_preset_popup.ui_wait_to_disappear()

        await ui_steps.service_deployment_install_page.ui_enter_container_image_repository_value(
            value="hashicorp/http-echo"
        )
        await (
            ui_steps.service_deployment_install_page.ui_click_container_image_checkbox()
        )
        await ui_steps.service_deployment_install_page.verify_ui_container_image_input_is_displayed()

        await ui_steps.service_deployment_install_page.ui_enter_container_image_input_value(
            value="1.0.0"
        )
        await ui_steps.service_deployment_install_page.ui_select_container_image_pull_policy(
            value="IfNotPresent"
        )
        await ui_steps.service_deployment_install_page.ui_click_container_checkbox()
        await ui_steps.service_deployment_install_page.verify_ui_container_command_checkbox_displayed()
        await ui_steps.service_deployment_install_page.verify_ui_container_args_checkbox_displayed()

        await (
            ui_steps.service_deployment_install_page.ui_click_container_args_checkbox()
        )
        await ui_steps.service_deployment_install_page.verify_ui_cnt_args_add_entry_btn_displayed()

        await ui_steps.service_deployment_install_page.ui_click_cnt_args_add_entry_button()
        await ui_steps.service_deployment_install_page.verify_ui_container_argument_input_displayed(
            index=0
        )

        await (
            ui_steps.service_deployment_install_page.ui_enter_container_argument_value(
                index=0, value='-text="hello apolo"'
            )
        )
        await ui_steps.service_deployment_install_page.ui_click_cnt_args_add_entry_button()
        await ui_steps.service_deployment_install_page.verify_ui_container_argument_input_displayed(
            index=1
        )

        await (
            ui_steps.service_deployment_install_page.ui_enter_container_argument_value(
                index=1, value="-listen=:8080"
            )
        )

        await ui_steps.service_deployment_install_page.ui_click_network_configuration_button()
        await ui_steps.service_deployment_install_page.ui_click_enable_authorization_checkbox()
        await ui_steps.service_deployment_install_page.ui_click_exp_ports_add_entry_button()
        await ui_steps.service_deployment_install_page.ui_enter_exposed_port_name(
            index=0, value="http"
        )
        await ui_steps.service_deployment_install_page.ui_enter_exposed_port_number(
            index=0, value="8080"
        )
        await ui_steps.service_deployment_install_page.ui_select_exposed_port_path_type(
            index=0, value="Prefix"
        )
        await ui_steps.service_deployment_install_page.ui_enter_exposed_port_path(
            index=0, value="/"
        )

        await ui_steps.service_deployment_install_page.ui_click_health_check_probes_checkbox()
        await ui_steps.service_deployment_install_page.ui_click_startup_probe_checkbox()
        await (
            ui_steps.service_deployment_install_page.ui_enter_startup_probe_delay_value(
                "30"
            )
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_period_value(
            "10"
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_failure_threshold_value(
            "5"
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_timeout_value(
            "5"
        )
        await (
            ui_steps.service_deployment_install_page.ui_enter_startup_probe_port_number(
                "8080"
            )
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_http_path(
            "/"
        )

        await (
            ui_steps.service_deployment_install_page.ui_click_readiness_probe_checkbox()
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_delay_value(
            "30"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_period_value(
            "10"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_failure_threshold_value(
            "5"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_timeout_value(
            "5"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_port_number(
            "8080"
        )
        await (
            ui_steps.service_deployment_install_page.ui_enter_readiness_probe_http_path(
                "/"
            )
        )

        app_name = self._data_manager.generate_app_instance_name(
            app_name="service-deployment"
        )
        TestE2EServiceDeploymentApp.serv_depl_app_name = app_name
        await ui_steps.service_deployment_install_page.ui_enter_serv_depl_app_name(
            app_name=app_name
        )

        await ui_steps.service_deployment_install_page.ui_click_install_btn()
        await ui_steps.service_deployment_details_page.verify_ui_page_displayed()
        await ui_steps.service_deployment_details_page.verify_ui_app_status_is_valid(
            expected_status="Queued"
        )

        app_id = (
            await ui_steps.service_deployment_details_page.ui_get_serv_depl_app_uuid()
        )
        TestE2EServiceDeploymentApp.serv_depl_app_id = app_id

        await api_steps.wait_for_app_events_until_ready(
            token=user.token,
            app_id=app_id,
            org_name=org.org_name,
            proj_name=proj.project_name,
        )
        await ui_steps.ui_reload_page()
        await ui_steps.service_deployment_details_page.verify_ui_app_status_is_valid(
            expected_status="Healthy"
        )

        TestE2EServiceDeploymentApp.app_install_status = True

    @async_title("Verify event list of installed Shell app via API")
    @pytest.mark.order(2)
    async def test_app_event_list_via_api(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - GET '/events' endpoint.

        ### Verify that:

        - App events list contains states queued, progressing and healthy.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name
        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_api_app_events_list(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title(
        "Verify installed Service Deployment app listed in Installed apps via UI"
    )
    @pytest.mark.order(3)
    async def test_app_listed_in_installed_apps_via_ui(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.

        ### Verify that:

        - Service Deployment app displayed in Installed Apps.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_verify_installed_app_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title(
        "Verify User can reach Service Deployment app Details page from Installed Apps page"
    )
    @pytest.mark.order(4)
    async def test_app_details_from_inst_apps_via_ui(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.
        - Click `Details` button on installed app container.

        ### Verify that:

        - `Service Deployment app Details` page displayed.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.service_deployment_details_page.verify_ui_page_displayed()

    @async_title(
        "Verify installed Service Deployment app info displayed on the app container via UI"
    )
    @pytest.mark.order(5)
    async def test_serv_depl_container_installed_info_via_ui(  # type: ignore[no-untyped-def]
        self, serv_depl_status
    ) -> None:
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.

        ### Verify that:

        - Label `Installed` is displayed on the Service Deployment app container.
        - `Show All` button displayed on the Service Deployment app container.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_serv_depl_container_displayed()
        await (
            ui_steps.main_page.verify_ui_installed_label_serv_depl_container_displayed()
        )
        await ui_steps.main_page.verify_ui_show_all_btn_serv_depl_container_displayed()

    @async_title("Verify User can reach Installed apps page from app container via UI")
    @pytest.mark.order(6)
    async def test_serv_depl_installed_apps_from_container_via_ui(  # type: ignore[no-untyped-def]
        self, serv_depl_status
    ) -> None:
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Show All` button on Service Deployment App container.

        ### Verify that:

        - Service Deployment app displayed in Installed Apps.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_serv_depl_container_displayed()
        await ui_steps.main_page.ui_serv_depl_container_click_show_all_btn()
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        await ui_steps.main_page.ui_verify_installed_app_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title("Verify Service Deployment app details info via UI")
    @pytest.mark.order(7)
    async def test_app_details_info_via_ui(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service DEployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Installed Apps` button.
        - Click `Details` button on installed app container.

        ### Verify that:

        - Service Deployment app Details info is valid.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.service_deployment_details_page.verify_ui_page_displayed()
        await ui_steps.service_deployment_details_page.verify_ui_app_details_info(
            owner=user.username,
            app_id=app_id,
            app_name=app_name,
            org_name=org_name,
            proj_name=proj_name,
        )

    @async_title("Verify Installed app details info via API")
    @pytest.mark.order(8)
    async def test_app_details_info_via_api(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `instances` API.

        ### Verify that:

        - API response contains valid data.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_api_app_details_info(
            token=user.token,
            app_id=app_id,
            expected_owner=user.username,
            expected_app_name=app_name,
            expected_org_name=org_name,
            expected_proj_name=proj_name,
        )

    @async_title("Verify app output contains required endpoints via UI")
    @pytest.mark.order(9)
    async def test_app_output_api_via_ui(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.
        - Click `Details` button on installed app container.
        - Scroll to `Output` section.

        ### Verify that `Output` section contains:
        - Http internal API
        - Http external API
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.service_deployment_details_page.verify_ui_page_displayed()
        await ui_steps.service_deployment_details_page.verify_ui_app_output_displayed()
        await ui_steps.service_deployment_details_page.verify_ui_app_output_apis()

    @async_title("Verify app output API schemas is valid via UI")
    @pytest.mark.order(10)
    async def test_app_output_api_data_format_via_ui(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.
        - Click `Details` button on installed app container.
        - Scroll to `Output` section.

        ### Verify that:
        - API sections data matching expected data format.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.service_deployment_details_page.verify_ui_page_displayed()
        await ui_steps.service_deployment_details_page.verify_ui_app_output_displayed()
        await ui_steps.service_deployment_details_page.verify_ui_app_output_apis_data_format()

    @async_title("Verify app output contains required endpoints via API")
    @pytest.mark.order(11)
    async def test_app_output_api_via_api(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `output` API.

        ### Verify that `output` API response contains required endpoints:

        - Http internal API
        - Https external API
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.get_app_output_api(
            token=user.token,
            app_id=app_id,
            org_name=org_name,
            proj_name=proj_name,
        )
        await api_steps.verify_serv_depl_output_endpoints(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title("Verify GET custom-deployment–<id> without auth header")
    @pytest.mark.order(12)
    async def test_get_cust_depl_no_auth_via_api(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `custom-deployment–<id>` API without auth header.

        ### Verify that:

        - Http internal API
        - Https external API
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_serv_depl_output_endpoints(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title("Verify app output endpoints schema via API")
    @pytest.mark.order(12)
    async def test_app_output_api_schema_via_api(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `output` API.

        ### Verify that:

        - API endpoints data matching expected json schema.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_shell_output_endpoints_schema_api(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title("Verify User can uninstall app via UI")
    @pytest.mark.order(15)
    async def test_app_uninstall_via_ui(self, serv_depl_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Service Deployment app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Installed Apps` button.
        - Click `Details` button on installed app container.
        - Click `Uninstall` button.

        ### Verify that:

        - Shell app uninstalled.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_name = TestE2EServiceDeploymentApp.serv_depl_app_name
        app_id = TestE2EServiceDeploymentApp.serv_depl_app_id
        org_name = TestE2EServiceDeploymentApp.org_name
        proj_name = TestE2EServiceDeploymentApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.service_deployment_details_page.verify_ui_page_displayed()

        await ui_steps.service_deployment_details_page.ui_click_uninstall_btn()
        await api_steps.wait_for_app_until_uninstalled(
            token=user.token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        await ui_steps.ui_open_product_base_page()
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_verify_installed_app_not_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title("Export Service Deployment app config via UI")
    @pytest.mark.order(16)
    async def test_export_app_config_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Select `cpu-medium` Resource Preset.
        - Set app Display name.
        - Click `Export config` button.

        ### Verify that:

        - Config downloaded as `yaml` file matches expected schema.
        - Exported config contains valid data.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user

        await ui_steps.ui_login(user, fresh_login=False)

        await ui_steps.main_page.verify_ui_serv_depl_container_displayed()

        await ui_steps.main_page.ui_serv_depl_container_click_install_btn()
        await ui_steps.service_deployment_install_page.verify_ui_page_displayed()

        await ui_steps.service_deployment_install_page.ui_click_resource_preset_btn()
        await ui_steps.resource_preset_popup.verify_ui_popup_displayed()

        await ui_steps.resource_preset_popup.ui_select_cpu_micro_preset()
        await ui_steps.resource_preset_popup.ui_click_apply_button()
        await ui_steps.resource_preset_popup.ui_wait_to_disappear()

        await ui_steps.service_deployment_install_page.ui_enter_container_image_repository_value(
            value="hashicorp/http-echo"
        )
        await (
            ui_steps.service_deployment_install_page.ui_click_container_image_checkbox()
        )
        await ui_steps.service_deployment_install_page.verify_ui_container_image_input_is_displayed()

        await ui_steps.service_deployment_install_page.ui_enter_container_image_input_value(
            value="1.0.0"
        )
        await ui_steps.service_deployment_install_page.ui_select_container_image_pull_policy(
            value="IfNotPresent"
        )
        await ui_steps.service_deployment_install_page.ui_click_container_checkbox()
        await ui_steps.service_deployment_install_page.verify_ui_container_command_checkbox_displayed()
        await ui_steps.service_deployment_install_page.verify_ui_container_args_checkbox_displayed()

        await (
            ui_steps.service_deployment_install_page.ui_click_container_args_checkbox()
        )
        await ui_steps.service_deployment_install_page.verify_ui_cnt_args_add_entry_btn_displayed()

        await ui_steps.service_deployment_install_page.ui_click_cnt_args_add_entry_button()
        await ui_steps.service_deployment_install_page.verify_ui_container_argument_input_displayed(
            index=0
        )

        await (
            ui_steps.service_deployment_install_page.ui_enter_container_argument_value(
                index=0, value="-text='hello apolo'"
            )
        )
        await ui_steps.service_deployment_install_page.ui_click_cnt_args_add_entry_button()
        await ui_steps.service_deployment_install_page.verify_ui_container_argument_input_displayed(
            index=1
        )

        await (
            ui_steps.service_deployment_install_page.ui_enter_container_argument_value(
                index=1, value="-listen=:8080"
            )
        )

        await ui_steps.service_deployment_install_page.ui_click_network_configuration_button()
        await ui_steps.service_deployment_install_page.ui_click_enable_authorization_checkbox()
        await ui_steps.service_deployment_install_page.ui_click_exp_ports_add_entry_button()
        await ui_steps.service_deployment_install_page.ui_enter_exposed_port_name(
            index=0, value="http"
        )
        await ui_steps.service_deployment_install_page.ui_enter_exposed_port_number(
            index=0, value="8080"
        )
        await ui_steps.service_deployment_install_page.ui_select_exposed_port_path_type(
            index=0, value="Prefix"
        )
        await ui_steps.service_deployment_install_page.ui_enter_exposed_port_path(
            index=0, value="/"
        )

        await ui_steps.service_deployment_install_page.ui_click_health_check_probes_checkbox()
        await ui_steps.service_deployment_install_page.ui_click_startup_probe_checkbox()
        await (
            ui_steps.service_deployment_install_page.ui_enter_startup_probe_delay_value(
                "30"
            )
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_period_value(
            "10"
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_failure_threshold_value(
            "5"
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_timeout_value(
            "5"
        )
        await (
            ui_steps.service_deployment_install_page.ui_enter_startup_probe_port_number(
                "8080"
            )
        )
        await ui_steps.service_deployment_install_page.ui_enter_startup_probe_http_path(
            "/"
        )

        await (
            ui_steps.service_deployment_install_page.ui_click_readiness_probe_checkbox()
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_delay_value(
            "30"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_period_value(
            "10"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_failure_threshold_value(
            "5"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_timeout_value(
            "5"
        )
        await ui_steps.service_deployment_install_page.ui_enter_readiness_probe_port_number(
            "8080"
        )
        await (
            ui_steps.service_deployment_install_page.ui_enter_readiness_probe_http_path(
                "/"
            )
        )

        app_name = self._data_manager.generate_app_instance_name(
            app_name="service-deployment"
        )
        await ui_steps.service_deployment_install_page.ui_enter_serv_depl_app_name(
            app_name=app_name
        )

        await ui_steps.service_deployment_install_page.verify_ui_export_config_btn_enabled()
        downloaded_config = (
            await ui_steps.service_deployment_install_page.ui_export_config()
        )
        await ui_steps.service_deployment_install_page.verify_exported_config_schema(
            config_file_path=downloaded_config
        )
        # await ui_steps.shell_install_page.verify_exported_config_data(
        #     config_file_path=downloaded_config,
        #     display_name=app_name,
        #     preset="cpu-medium",
        #     http_auth=True,
        # )

    @async_title("Import Service Deployment app config via UI")
    @pytest.mark.order(17)
    async def test_import_app_config_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Import Service Deployment app config via UI.

        ### Verify that:

        - Install required data is the same as in imported config.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_shell_container_displayed()

        await ui_steps.main_page.ui_shell_container_click_install_btn()
        await ui_steps.shell_install_page.verify_ui_page_displayed()

        await ui_steps.shell_install_page.ui_click_import_config_btn()
        await ui_steps.import_app_config_popup.verify_ui_popup_displayed()

        config_file_path = (
            await ui_steps.shell_install_page.get_import_config_file_path()
        )
        await ui_steps.import_app_config_popup.ui_import_yaml_config(
            config_path=config_file_path
        )
        await ui_steps.import_app_config_popup.ui_click_apply_config_btn()
        await ui_steps.import_app_config_popup.ui_wait_to_disappear()
        await ui_steps.shell_install_page.verify_ui_page_displayed()
        await ui_steps.shell_install_page.verify_ui_resource_preset_btn_value(
            expected_value="cpu-large"
        )
        await ui_steps.shell_install_page.verify_ui_auth_type(
            expected_value="No Authentication"
        )
        await ui_steps.shell_install_page.verify_ui_display_name_value(
            expected_value="shell-testing"
        )
