import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.api_steps.api_steps import APISteps
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("Shell App", parent="E2E Tests")
@pytest.mark.flaky(reruns=0)
@pytest.mark.class_setup
class TestE2EShellApp(BaseTestClass):
    shell_app_name = ""
    shell_app_id = ""
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
    def shell_status(self) -> None:
        if not TestE2EShellApp.app_install_status:
            pytest.skip("Shell app was not installed successfully")

    @async_title("Install Shell app via UI")
    @pytest.mark.order(1)
    @pytest.mark.timeout(700)
    async def test_install_shell_app_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.

        ### Verify that:

        - User can install `Shell` app via **UI**.
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
        TestE2EShellApp.org_name = org.org_name
        proj = org.add_project(gherkin_name="Default-project")
        TestE2EShellApp.proj_name = proj.project_name
        await ui_steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )

        await ui_steps.main_page.verify_ui_shell_container_displayed()

        await ui_steps.main_page.ui_shell_container_click_install_btn()
        await ui_steps.shell_install_page.verify_ui_page_displayed()

        await ui_steps.shell_install_page.ui_click_resource_preset_btn()
        await ui_steps.resource_preset_popup.verify_ui_popup_displayed()

        await ui_steps.resource_preset_popup.ui_select_cpu_medium_preset()
        await ui_steps.resource_preset_popup.ui_click_apply_button()
        await ui_steps.resource_preset_popup.ui_wait_to_disappear()
        app_name = self._data_manager.generate_app_instance_name(app_name="Shell")
        TestE2EShellApp.shell_app_name = app_name
        await ui_steps.shell_install_page.ui_enter_shell_app_name(app_name=app_name)

        await ui_steps.shell_install_page.ui_click_install_btn()

        await ui_steps.shell_details_page.verify_ui_page_displayed()
        await ui_steps.shell_details_page.verify_ui_app_status_is_valid(
            expected_status="Queued"
        )

        app_id = await ui_steps.shell_details_page.ui_get_shell_app_uuid()
        TestE2EShellApp.shell_app_id = app_id

        await api_steps.wait_for_app_events_until_ready(
            token=user.token,
            app_id=app_id,
            org_name=org.org_name,
            proj_name=proj.project_name,
        )
        await ui_steps.ui_reload_page()
        await ui_steps.shell_details_page.verify_ui_app_status_is_valid(
            expected_status="Healthy"
        )

        TestE2EShellApp.app_install_status = True

    @async_title("Verify event list of installed Shell app via API")
    @pytest.mark.order(2)
    async def test_app_event_list_via_api(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - GET '/events' endpoint.

        ### Verify that:

        - App events list contains states queued, progressing and healthy.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name
        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_api_app_events_list(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title("Verify installed Shell app listed in Installed apps via UI")
    @pytest.mark.order(3)
    async def test_app_listed_in_installed_apps_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.

        ### Verify that:

        - Shell app displayed in Installed Apps.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EShellApp.shell_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_verify_installed_app_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title(
        "Verify User can reach Shell app Details page from Installed Apps page"
    )
    @pytest.mark.order(4)
    async def test_app_details_from_inst_apps_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.
        - Click `Details` button on installed app container.

        ### Verify that:

        - `Shell app Details` page displayed.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EShellApp.shell_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.shell_details_page.verify_ui_page_displayed()

    @async_title(
        "Verify installed Shell app info displayed on the app container via UI"
    )
    @pytest.mark.order(5)
    async def test_shell_container_installed_info_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.

        ### Verify that:

        - Label `Installed` is displayed on the Shell app container.
        - `Show All` button displayed on the Shell app container.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_shell_container_displayed()
        await ui_steps.main_page.verify_ui_installed_label_shell_container_displayed()
        await ui_steps.main_page.verify_ui_show_all_btn_shell_container_displayed()

    @async_title("Verify User can reach Installed apps page from app container via UI")
    @pytest.mark.order(6)
    async def test_shell_installed_apps_from_container_via_ui(  # type: ignore[no-untyped-def]
        self, shell_status
    ) -> None:
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Show All` button on Shell App container.

        ### Verify that:

        - Shell app displayed in Installed Apps.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_shell_container_displayed()
        await ui_steps.main_page.ui_shell_container_click_show_all_btn()
        app_name = TestE2EShellApp.shell_app_name
        await ui_steps.main_page.ui_verify_installed_app_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title("Verify Installed apps details info via UI")
    @pytest.mark.order(7)
    async def test_app_details_info_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Installed Apps` button.
        - Click `Details` button on installed app container.

        ### Verify that:

        - Shell app Details info is valid.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EShellApp.shell_app_name
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.shell_details_page.verify_ui_page_displayed()
        await ui_steps.shell_details_page.verify_ui_app_details_info(
            owner=user.username,
            app_id=app_id,
            app_name=app_name,
            org_name=org_name,
            proj_name=proj_name,
        )

    @async_title("Verify Installed apps details info via API")
    @pytest.mark.order(8)
    async def test_app_details_info_via_api(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `instances` API.

        ### Verify that:

        - API response contains valid data.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_name = TestE2EShellApp.shell_app_name
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

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
    async def test_app_output_api_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.
        - Click `Details` button on installed app container.
        - Scroll to `Output` section.

        ### Verify that `Output` section contains:
        - Http internal API
        - Https external API
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EShellApp.shell_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.shell_details_page.verify_ui_page_displayed()
        await ui_steps.shell_details_page.verify_ui_app_output_displayed()
        await ui_steps.shell_details_page.verify_ui_app_output_apis()

    @async_title("Verify app output API schemas is valid via UI")
    @pytest.mark.order(10)
    async def test_app_output_api_data_format_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
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
        app_name = TestE2EShellApp.shell_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.shell_details_page.verify_ui_page_displayed()
        await ui_steps.shell_details_page.verify_ui_app_output_displayed()
        await ui_steps.shell_details_page.verify_ui_app_output_apis_data_format()

    @async_title("Verify app output contains required endpoints via API")
    @pytest.mark.order(11)
    async def test_app_output_api_via_api(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

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
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.get_app_output_api(
            token=user.token,
            app_id=app_id,
            org_name=org_name,
            proj_name=proj_name,
        )
        await api_steps.verify_shell_output_endpoints(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title("Verify app output endpoints schema via API")
    @pytest.mark.order(12)
    async def test_app_output_api_schema_via_api(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `output` API.

        ### Verify that:

        - API endpoints data matching expected json schema.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_shell_output_endpoints_schema_api(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )

    @async_title("Open Shell application via UI")
    @pytest.mark.order(13)
    async def test_open_shell_app_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `output` API.
        - Get `external https` endpoint.

        ### Verify that:

        - Shell app can be launched via UI.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        url = await api_steps.get_shell_ext_output_endpoint_api(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )
        await ui_steps.shell_app_page.ui_open_shell_app_page(url=url)
        await ui_steps.shell_app_page.verify_ui_page_displayed()

    @async_title("Enter command in Shell app via UI")
    @pytest.mark.order(14)
    async def test_enter_command_in_shell_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `output` API.
        - Get `external https` endpoint.
        - Launch Shell app.
        - Execute `apolo config show` command.

        ### Verify that Shell app output contains:

        - executed command `apolo config show`.
        - `User configuration` section.
        - `Resource Preset` section.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        url = await api_steps.get_shell_ext_output_endpoint_api(
            token=user.token, app_id=app_id, org_name=org_name, proj_name=proj_name
        )
        await ui_steps.shell_app_page.ui_open_shell_app_page(url=url)
        await ui_steps.shell_app_page.verify_ui_page_displayed()

        await ui_steps.shell_app_page.ui_enter_command_in_shell("apolo config show")
        await ui_steps.shell_app_page.ui_open_shell_app_page(url=url)
        await ui_steps.shell_app_page.verify_ui_executed_command_in_shell_output(
            command="apolo config show"
        )
        await ui_steps.shell_app_page.verify_ui_user_config_in_shell_output(
            org_name=org_name, proj_name=proj_name
        )
        await ui_steps.shell_app_page.verify_ui_res_presets_in_shell_output()

    @async_title("Verify User can uninstall app via UI")
    @pytest.mark.order(15)
    async def test_app_uninstall_via_ui(self, shell_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - Shell app installed.

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
        app_name = TestE2EShellApp.shell_app_name
        app_id = TestE2EShellApp.shell_app_id
        org_name = TestE2EShellApp.org_name
        proj_name = TestE2EShellApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.shell_details_page.verify_ui_page_displayed()

        await ui_steps.shell_details_page.ui_click_uninstall_btn()
        await api_steps.wait_for_app_until_uninstalled(
            token=user.token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        await ui_steps.ui_open_product_base_page()
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_verify_installed_app_not_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title("Export Shell app config via UI")
    @pytest.mark.order(16)
    async def test_export_shell_app_config_via_ui(self) -> None:
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

        await ui_steps.main_page.verify_ui_shell_container_displayed()

        await ui_steps.main_page.ui_shell_container_click_install_btn()
        await ui_steps.shell_install_page.verify_ui_page_displayed()

        await ui_steps.shell_install_page.ui_click_resource_preset_btn()
        await ui_steps.resource_preset_popup.verify_ui_popup_displayed()

        await ui_steps.resource_preset_popup.ui_select_cpu_medium_preset()
        await ui_steps.resource_preset_popup.ui_click_apply_button()
        await ui_steps.resource_preset_popup.ui_wait_to_disappear()
        app_name = self._data_manager.generate_app_instance_name(app_name="Shell")
        await ui_steps.shell_install_page.ui_enter_shell_app_name(app_name=app_name)
        await ui_steps.shell_install_page.verify_ui_export_config_btn_enabled()
        downloaded_config = await ui_steps.shell_install_page.ui_export_config()
        await ui_steps.shell_install_page.verify_exported_config_schema(
            config_file_path=downloaded_config
        )
        await ui_steps.shell_install_page.verify_exported_config_data(
            config_file_path=downloaded_config,
            display_name=app_name,
            preset="cpu-medium",
            http_auth=True,
        )

    @async_title("Import Shell app config via UI")
    @pytest.mark.order(17)
    async def test_import_shell_app_config_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Import Shell app config via UI.

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
        await ui_steps.shell_install_page.verify_ui_auth_type(expected_value="False")
        await ui_steps.shell_install_page.verify_ui_display_name_value(
            expected_value="shell-testing"
        )
