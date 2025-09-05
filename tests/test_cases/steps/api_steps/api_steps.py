import asyncio
import time
from typing import Any

from tests.reporting_hooks.reporting import async_step
from tests.utils.api_helper import APIHelper
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


class APISteps:
    def __init__(
        self,
        test_config: ConfigManager,
        api_helper: APIHelper,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._api_helper = api_helper
        self._data_manager = data_manager

    @async_step("Wait for app events until healthy or degraded")
    async def wait_for_app_events_until_ready(
        self,
        token: str,
        org_name: str,
        proj_name: str,
        app_id: str,
    ) -> Any:
        timeout = 600  # 10 minutes
        interval = 20
        start = time.monotonic()
        deadline = start + timeout
        max_attempts = timeout // interval

        for attempt in range(1, max_attempts + 1):
            status, response = await self._api_helper.get_app_events(
                token=token,
                org_name=org_name,
                proj_name=proj_name,
                app_id=app_id,
            )

            if status != 200:
                # Unexpected API error
                return {"status": status, "response": response}

            items = response.get("items", [])
            if not items:
                # No events yet → keep waiting
                pass
            else:
                latest_event = items[0]
                state = latest_event.get("state")

                if state == "healthy":
                    return latest_event

                if state == "degraded":
                    raise AssertionError(
                        f"❌ App entered degraded state: {latest_event}"
                    )

            if time.monotonic() >= deadline:
                break

            await asyncio.sleep(interval)

        raise TimeoutError("⏳ Timed out waiting for app to reach 'healthy' state.")

    @async_step("Wait for app until uninstalled")
    async def wait_for_app_until_uninstalled(
        self,
        token: str,
        org_name: str,
        proj_name: str,
        app_id: str,
    ) -> Any:
        timeout = 300  # 5 minutes
        interval = 10
        start = time.monotonic()
        deadline = start + timeout
        max_attempts = timeout // interval

        for attempt in range(1, max_attempts + 1):
            status, response = await self._api_helper.get_instances(
                token=token,
                org_name=org_name,
                proj_name=proj_name,
            )

            if status != 200:
                raise RuntimeError(
                    f"[Error] API returned {status} instead of 200 "
                    f"on attempt {attempt}/{max_attempts}"
                )

            items = response.get("items", [])
            match = next((item for item in items if item.get("id") == app_id), None)

            if not match:
                raise ValueError(f"No app with id '{app_id}' found in API response")

            state = match.get("state", "").lower()
            if state == "uninstalled":
                return match

            if time.monotonic() >= deadline:
                break

            await asyncio.sleep(interval)

        raise TimeoutError(
            f"⏳ Timed out waiting for app '{app_id}' to reach 'uninstalled' state."
        )

    @async_step("Validate app instance details via API")
    async def verify_api_app_details_info(
        self,
        token: str,
        app_id: str,
        expected_owner: str,
        expected_app_name: str,
        expected_proj_name: str,
        expected_org_name: str,
    ) -> None:
        (
            result,
            error_message,
        ) = await self._api_helper.verify_app_instance_info(
            token=token,
            app_id=app_id,
            expected_owner=expected_owner,
            expected_app_name=expected_app_name,
            expected_proj_name=expected_proj_name,
            expected_org_name=expected_org_name,
        )
        assert result, error_message
