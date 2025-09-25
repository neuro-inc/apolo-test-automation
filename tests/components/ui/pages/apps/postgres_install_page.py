from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class PostgresInstallPage(BasePage):
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
            and await self._get_resource_preset_label().is_visible()
            and await self._get_resource_preset_btn().is_visible()
            and await self._get_postgres_config_label().is_visible()
            and await self._get_postgres_replicas_input().is_visible()
            and await self._get_database_users_label().is_visible()
            and await self._get_add_database_user_btn().is_visible()
            and await self._get_pg_bouncer_replicas_input().is_visible()
            and await self._get_display_name_input().is_visible()
            and await self._get_install_button().is_visible()
        )

    def _get_page_heading(self) -> BaseElement:
        return BaseElement(self.page, "h4", has_text="PostgreSQL App")

    def _get_page_title(self) -> BaseElement:
        return BaseElement(self.page, "h3", has_text="PostgreSQL")

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

    def _get_postgres_config_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h4", has_text="Postgres")

    def _get_postgres_replicas_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="postgres_config.instance_replicas"]')

    async def enter_postgres_replicas_count(self, value: str) -> None:
        self.log(f"Entering Postgres replicas count: {value}")
        await self._get_postgres_replicas_input().fill(value)

    def _get_database_users_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h6", has_text="Database users")

    def _get_add_database_user_btn(self) -> BaseElement:
        """
        Outer 'Add entry' button to add a new Database user card
        """
        return BaseElement(
            self.page,
            selector="//p[normalize-space()='Database users']/ancestor::div[1]//button[normalize-space()='Add entry']",
        )

    async def click_add_database_user_btn(self) -> None:
        self.log("Click Add Database User button")
        await self._get_add_database_user_btn().click()

    def _get_postgres_user_name_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='postgres_config.db_users.0.name']"
        )

    async def is_postgres_user_name_input_displayed(self) -> bool:
        self.log("Check if Postgres User name input displayed")
        return await self._get_postgres_user_name_input().is_visible()

    async def enter_postgres_user_name(self, value: str) -> None:
        self.log(f"Entering Postgres User name: {value}")
        await self._get_postgres_user_name_input().fill(value)

    def _get_add_database_name_button(self) -> BaseElement:
        """
        Inner 'Add entry' button (inside a user card, next to Database name)
        """
        return BaseElement(
            self.page,
            "(//div[.//label[text()='Database name']]//button[normalize-space()='Add entry'])[1]",
        )

    async def is_add_database_name_button_displayed(self) -> bool:
        self.log("Check if Add Database name button displayed")
        return await self._get_add_database_name_button().is_visible()

    async def click_add_database_name_button(self) -> None:
        self.log("Click Add Database name button")
        await self._get_add_database_name_button().click()

    def _get_postgres_db_name_input(self) -> BaseElement:
        return BaseElement(
            self.page, selector="//input[@name='postgres_config.db_users.0.db_names.0']"
        )

    async def is_postgres_db_name_input_displayed(self) -> bool:
        self.log("Check if Postgres DB name input displayed")
        return await self._get_postgres_db_name_input().is_visible()

    async def enter_postgres_db_name(self, value: str) -> None:
        self.log(f"Entering Postgres DB name: {value}")
        await self._get_postgres_db_name_input().fill(value)

    def _get_pg_bouncer_label(self) -> BaseElement:
        return BaseElement(self.page, "//p[normalize-space()='PG Bouncer']")

    def _get_pg_bouncer_resource_preset_button(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="//p[normalize-space()='PG Bouncer']"
            "/ancestor::div[1]//button[.//p[normalize-space()='Resource Preset']]",
        )

    async def click_pg_bouncer_resource_preset_btn(self) -> None:
        self.log("Click PG Bouncer resource preset button")
        await self._get_pg_bouncer_resource_preset_button().click()

    def _get_pg_bouncer_replicas_input(self) -> BaseElement:
        return BaseElement(self.page, selector="//input[@name='pg_bouncer.replicas']")

    async def enter_pg_bouncer_replicas_count(self, value: str) -> None:
        self.log(f"Entering PG Bouncer replicas count: {value}")
        await self._get_pg_bouncer_replicas_input().fill(value)

    def _get_metadata_label(self) -> BaseElement:
        return BaseElement(self.page, selector="//p[normalize-space()='Metadata']")

    def _get_display_name_input(self) -> BaseElement:
        return BaseElement(self.page, selector="//input[@name='displayName']")

    async def enter_display_name(self, value: str) -> None:
        self.log(f"Entering Display name: {value}")
        await self._get_display_name_input().fill(value)

    def _get_install_button(self) -> BaseElement:
        return BaseElement(self.page, selector="//button[normalize-space()='Install']")

    async def click_install_button(self) -> None:
        self.log("Click Install button")
        await self._get_install_button().click()
