import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.api_steps.api_steps import APISteps
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("PostgreSQL App", parent="E2E Tests")
@pytest.mark.flaky(reruns=0)
@pytest.mark.class_setup
class TestE2EPostgresApp(BaseTestClass):
    postgres_app_name = ""
    postgres_app_id = ""
    org_name = ""
    proj_name = ""
    postgres_user_name = ""
    postgres_user_db_name = ""
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
    def postgres_status(self) -> None:
        if not TestE2EPostgresApp.app_install_status:
            pytest.skip("PostgreSQL app was not installed successfully")

    @async_title("Install PostgreSQL app via UI")
    @pytest.mark.order(1)
    @pytest.mark.timeout(700)
    async def test_install_postgres_app_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.

        ### Verify that:

        - User can install `PostgreSQL` app via **UI**.
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
        TestE2EPostgresApp.org_name = org.org_name
        proj = org.add_project(gherkin_name="Default-project")
        TestE2EPostgresApp.proj_name = proj.project_name
        await ui_steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )

        await ui_steps.main_page.verify_ui_postgres_container_displayed()

        await ui_steps.main_page.ui_postgres_container_click_install_btn()
        await ui_steps.postgres_install_page.verify_ui_page_displayed()

        await ui_steps.postgres_install_page.ui_click_resource_preset_btn()
        await ui_steps.resource_preset_popup.verify_ui_popup_displayed()

        await ui_steps.resource_preset_popup.ui_select_cpu_medium_preset()
        await ui_steps.resource_preset_popup.ui_click_apply_button()
        await ui_steps.resource_preset_popup.ui_wait_to_disappear()

        await ui_steps.postgres_install_page.ui_enter_postgres_replicas_count(value="1")
        await ui_steps.postgres_install_page.ui_click_add_database_user_btn()
        await (
            ui_steps.postgres_install_page.verify_ui_postgres_username_input_displayed()
        )
        await ui_steps.postgres_install_page.verify_ui_add_postgres_user_db_btn_displayed()

        ps_user_name = self._data_manager.generate_postgres_user_name()
        TestE2EPostgresApp.postgres_user_name = ps_user_name
        await ui_steps.postgres_install_page.ui_enter_postgres_username(
            value=ps_user_name
        )
        await ui_steps.postgres_install_page.ui_click_add_postgres_user_db_btn()
        await (
            ui_steps.postgres_install_page.verify_ui_postgres_user_db_input_displayed()
        )

        ps_user_db_name = self._data_manager.generate_postgres_user_db_name()
        TestE2EPostgresApp.postgres_user_db_name = ps_user_db_name
        await ui_steps.postgres_install_page.ui_enter_postgres_user_db_name(
            value=ps_user_db_name
        )
        await ui_steps.postgres_install_page.ui_click_pg_bouncer_resource_preset_btn()
        await ui_steps.resource_preset_popup.verify_ui_popup_displayed()

        await ui_steps.resource_preset_popup.ui_select_cpu_medium_preset()
        await ui_steps.resource_preset_popup.ui_click_apply_button()
        await ui_steps.resource_preset_popup.ui_wait_to_disappear()

        await ui_steps.postgres_install_page.ui_enter_pg_bouncer_replicas_count(
            value="1"
        )

        app_name = self._data_manager.generate_app_instance_name(app_name="PostgreSQL")
        TestE2EPostgresApp.postgres_app_name = app_name
        await ui_steps.postgres_install_page.ui_enter_postgres_display_name(
            value=app_name
        )

        await ui_steps.postgres_install_page.ui_click_install_btn()

        await ui_steps.postgres_details_page.verify_ui_page_displayed()
        await ui_steps.postgres_details_page.verify_ui_app_status_is_valid(
            expected_status="Queued"
        )

        app_id = await ui_steps.postgres_details_page.ui_get_postgres_app_uuid()
        TestE2EPostgresApp.postgres_app_id = app_id

        await api_steps.wait_for_app_events_until_ready(
            token=user.token,
            app_id=app_id,
            org_name=org.org_name,
            proj_name=proj.project_name,
        )
        await ui_steps.ui_reload_page()
        await ui_steps.postgres_details_page.verify_ui_app_status_is_valid(
            expected_status="Healthy"
        )

        TestE2EPostgresApp.app_install_status = True

    @async_title("Verify installed PostgreSQL app listed in Installed apps via UI")
    @pytest.mark.order(2)
    async def test_app_listed_in_installed_apps_via_ui(self, postgres_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.

        ### Verify that:

        - PostgreSQL app displayed in Installed Apps.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EPostgresApp.postgres_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_verify_installed_app_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title(
        "Verify User can reach PostgreSQL app Details page from Installed Apps page"
    )
    @pytest.mark.order(3)
    async def test_app_details_from_inst_apps_via_ui(self, postgres_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.
        - Click Installed Apps.
        - Click `Details` button on installed app container.

        ### Verify that:

        - `PostgreSQL app Details` page displayed.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EPostgresApp.postgres_app_name
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.verify_ui_inst_app_details_btn_displayed(
            app_name=app_name, owner=user.username
        )

        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.postgres_details_page.verify_ui_page_displayed()

    @async_title(
        "Verify installed PostgreSQL app info displayed on the app container via UI"
    )
    @pytest.mark.order(4)
    async def test_postgres_container_installed_info_via_ui(  # type: ignore[no-untyped-def]
        self, postgres_status
    ) -> None:
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.

        ### Verify that:

        - Label `Installed` is displayed on the PostgreSQL app container.
        - `Show All` button displayed on the PostgreSQL app container.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_shell_container_displayed()
        await (
            ui_steps.main_page.verify_ui_installed_label_postgres_container_displayed()
        )
        await ui_steps.main_page.verify_ui_show_all_btn_postgres_container_displayed()

    @async_title("Verify User can reach Installed apps page from app container via UI")
    @pytest.mark.order(5)
    async def test_postgres_installed_apps_from_container_via_ui(  # type: ignore[no-untyped-def]
        self, postgres_status
    ) -> None:
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Show All` button on PostgreSQL App container.

        ### Verify that:

        - PostgreSQL app displayed in Installed Apps.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.verify_ui_shell_container_displayed()
        await ui_steps.main_page.ui_postgres_container_click_show_all_btn()
        app_name = TestE2EPostgresApp.postgres_app_name
        await ui_steps.main_page.ui_verify_installed_app_displayed(
            app_name=app_name, owner=user.username
        )

    @async_title("Verify PostgreSQL app details info via UI")
    @pytest.mark.order(6)
    async def test_app_details_info_via_ui(self, postgres_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Installed Apps` button.
        - Click `Details` button on installed app container.

        ### Verify that:

        - PostgreSQL app Details info is valid.
        """
        ui_steps = self._ui_steps
        user = self._users_manager.main_user
        app_name = TestE2EPostgresApp.postgres_app_name
        app_id = TestE2EPostgresApp.postgres_app_id
        org_name = TestE2EPostgresApp.org_name
        proj_name = TestE2EPostgresApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.postgres_details_page.verify_ui_page_displayed()
        await ui_steps.postgres_details_page.verify_ui_app_details_info(
            owner=user.username,
            app_id=app_id,
            app_name=app_name,
            org_name=org_name,
            proj_name=proj_name,
        )

    @async_title("Verify Installed apps details info via API")
    @pytest.mark.order(7)
    async def test_app_details_info_via_api(self, postgres_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.
        - Call `instances` API.

        ### Verify that:

        - API response contains valid data.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_name = TestE2EPostgresApp.postgres_app_name
        app_id = TestE2EPostgresApp.postgres_app_id
        org_name = TestE2EPostgresApp.org_name
        proj_name = TestE2EPostgresApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await api_steps.verify_api_app_details_info(
            token=user.token,
            app_id=app_id,
            expected_owner=user.username,
            expected_app_name=app_name,
            expected_org_name=org_name,
            expected_proj_name=proj_name,
        )

    @async_title("Verify User can uninstall app via UI")
    @pytest.mark.order(8)
    async def test_app_uninstall_via_ui(self, postgres_status) -> None:  # type: ignore[no-untyped-def]
        """
        ### Pre-conditions:
        - PostgreSQL app installed.

        ### Steps:
        - Login with valid credentials.
        - Click `Installed Apps` button.
        - Click `Details` button on installed app container.
        - Click `Uninstall` button.

        ### Verify that:

        - PostgreSQL app uninstalled.
        """
        ui_steps = self._ui_steps
        api_steps = self._api_steps
        user = self._users_manager.main_user
        app_name = TestE2EPostgresApp.postgres_app_name
        app_id = TestE2EPostgresApp.postgres_app_id
        org_name = TestE2EPostgresApp.org_name
        proj_name = TestE2EPostgresApp.proj_name

        await ui_steps.ui_login(user, fresh_login=False)
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_click_inst_app_details_btn(
            app_name=app_name, owner=user.username
        )
        await ui_steps.postgres_details_page.verify_ui_page_displayed()

        await ui_steps.postgres_details_page.ui_click_uninstall_btn()
        await api_steps.wait_for_app_until_uninstalled(
            token=user.token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        await ui_steps.ui_open_product_base_page()
        await ui_steps.main_page.ui_click_installed_apps_btn()
        await ui_steps.main_page.ui_verify_installed_app_not_displayed(
            app_name=app_name, owner=user.username
        )
