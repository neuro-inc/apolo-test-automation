from typing import Any

from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class PostgresDetailsPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
    ) -> None:
        self._pm = page_manager
        self._data_manager = data_manager
        self.required_user_data = [
            "Postgres User Credentials (0)",
            "Postgres Admin User",
        ]

    @async_step("Verify that Postgres app Details page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.postgres_details_page.is_loaded(), (
            "Postgres app Details page should be displayed!"
        )

    @async_step("Verify App output section displayed")
    async def verify_ui_app_output_displayed(self) -> None:
        assert await self._pm.postgres_details_page.is_output_container_displayed(), (
            "Output container should be displayed!"
        )

    @async_step("Verify App output contains required user data")
    async def verify_ui_app_output_user_data(self) -> None:
        user_data = await self._pm.postgres_details_page.parse_output_user_data()
        result, error_message = self._verify_required_user_data(user_data)
        assert result, error_message

    @async_step("Verify that app status is valid")
    async def verify_ui_app_status_is_valid(self, expected_status: str) -> None:
        actual_status = await self._pm.postgres_details_page.get_app_status()
        assert actual_status.lower() == expected_status.lower(), (
            f"Expected {expected_status} but got {actual_status}!"
        )

    @async_step("Get Postgres app UUID")
    async def ui_get_postgres_app_uuid(self) -> str:
        return await self._pm.postgres_details_page.get_uuid_value()

    @async_step("Validate Postgres app details info")
    async def verify_ui_app_details_info(
        self, owner: str, app_id: str, app_name: str, proj_name: str, org_name: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._pm.postgres_details_page.verify_app_details_info(
            owner=owner,
            app_id=app_id,
            app_name=app_name,
            proj_name=proj_name,
            org_name=org_name,
        )
        assert result, error_message

    @async_step("Click Uninstall button")
    async def ui_click_uninstall_btn(self) -> None:
        await self._pm.postgres_details_page.click_uninstall_btn()

    @async_step("Verify Users data sections contains valid data format")
    async def verify_ui_app_output_users_data_format(self) -> None:
        user_data = await self._pm.postgres_details_page.parse_output_user_data()
        await self._data_manager.app_data.load_output_ui_schema("postgres")
        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            [user_data]
        )
        assert result, error_message

    @async_step("Verify Users data contains valid created user info")
    async def verify_ui_output_created_user_data(
        self, user_name: str, user_db_name: str
    ) -> None:
        user_data = await self._pm.postgres_details_page.parse_output_user_data()
        result, error_message = await self._validate_created_user_data(
            user_data=user_data, user_name=user_name, user_db_name=user_db_name
        )
        assert result, error_message

    def _verify_required_user_data(self, user_data: dict[str, Any]) -> tuple[bool, str]:
        """
        Verifies that all required user data sections exist inside the PostgresUsers block.

        Returns:
            (True, "") if all checks pass
            (False, "error message") if something is missing
        """
        postgres_users = user_data.get("PostgresUsers", {})
        if not postgres_users:
            return False, "No PostgresUsers block found in UI output"

        found_keys = list(postgres_users.keys())

        missing = []
        for user_type in self.required_user_data:
            if user_type in postgres_users:
                # e.g. "Postgres Admin User"
                continue
            elif (
                "Postgres Users" in postgres_users
                and user_type in postgres_users["Postgres Users"]
            ):
                # e.g. "Postgres User Credentials (0)"
                continue
            else:
                missing.append(user_type)

        if missing:
            return (
                False,
                f"Missing required user type(s): {', '.join(missing)}. "
                f"Top-level keys in PostgresUsers: {found_keys}",
            )

        return True, ""

    async def _validate_created_user_data(
        self, user_data: dict[str, Any], user_name: str, user_db_name: str
    ) -> tuple[bool, str]:
        try:
            # Navigate into PostgresUsers → Postgres Users → Postgres User Credentials (0)
            postgres_users = user_data.get("PostgresUsers", {})
            if not postgres_users:
                return False, "No PostgresUsers block found in UI output"

            postgres_users_block = postgres_users.get("Postgres Users", {})
            if not postgres_users_block:
                return False, "No 'Postgres Users' block found in UI output"

            user_credentials = postgres_users_block.get(
                "Postgres User Credentials (0)", {}
            )
            if not user_credentials:
                return (
                    False,
                    "No 'Postgres User Credentials (0)' block found in UI output",
                )

            # Extract fields
            actual_user = user_credentials.get("Postgres User")
            actual_dbname = user_credentials.get("Dbname")

            # Verify values
            if actual_user != user_name:
                return False, (
                    f"Expected Postgres User '{user_name}', but got '{actual_user}'"
                )
            if actual_dbname != user_db_name:
                return False, (
                    f"Expected Dbname '{user_db_name}', but got '{actual_dbname}'"
                )

            return True, ""

        except Exception as e:
            return False, f"Validation error: {e}"
