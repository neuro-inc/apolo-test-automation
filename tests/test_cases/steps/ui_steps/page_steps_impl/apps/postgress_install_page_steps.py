from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class PostgresInstallPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Postgres install page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.postgres_install_page.is_loaded(), (
            "Postgres Install page should be displayed!"
        )

    @async_step("Click Resource preset button")
    async def ui_click_resource_preset_btn(self) -> None:
        await self._pm.postgres_install_page.click_resource_preset_btn()

    @async_step("Enter Postgres replicas count")
    async def ui_enter_postgres_replicas_count(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_postgres_replicas_count(value=value)

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

    @async_step("Click PG Bouncer Resource Preset button")
    async def ui_click_pg_bouncer_resource_preset_btn(self) -> None:
        await self._pm.postgres_install_page.click_pg_bouncer_resource_preset_btn()

    @async_step("Enter PG Bouncer replicas count")
    async def ui_enter_pg_bouncer_replicas_count(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_pg_bouncer_replicas_count(
            value=value
        )

    @async_step("Enter Postgres Display name")
    async def ui_enter_postgres_display_name(self, value: str) -> None:
        await self._pm.postgres_install_page.enter_display_name(value=value)

    @async_step("Click Install button")
    async def ui_click_install_btn(self) -> None:
        await self._pm.shell_install_page.click_install_btn()
