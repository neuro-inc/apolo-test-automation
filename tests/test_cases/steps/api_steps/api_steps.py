from __future__ import annotations

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
        timeout: int = 600,  # 10 minutes
    ) -> Any:
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

        raise AssertionError("⏳ Timed out waiting for app to reach 'healthy' state.")

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

    @async_step("Verify App output contains required endpoints via API")
    async def verify_api_app_output_apis(
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

    @async_step("Add Secret via API")
    async def add_secret_api(
        self,
        token: str,
        secret_name: str,
        secret_value: str,
        org_name: str,
        proj_name: str,
    ) -> None:
        status, response = await self._api_helper.add_secret(
            token=token,
            secret_name=secret_name,
            secret_value=secret_value,
            org_name=org_name,
            proj_name=proj_name,
        )
        assert status == 201, f"Expected HTTP 201 response but got {status}!"

    @async_step("GET app output endpoint")
    async def get_app_output_api(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

    @async_step("Verify output response contains required endpoints")
    async def verify_output_endpoints(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        required_APIs = [
            ("OpenAI Compatible Chat API", "http"),
            ("OpenAI Compatible Chat API", "https"),
            ("OpenAI Compatible Embeddings API", "http"),
            ("OpenAI Compatible Embeddings API", "https"),
        ]
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

        api_sections = self._extract_api_sections(response)
        result, error_message = self._verify_required_endpoints(
            api_sections, required_APIs
        )
        assert result, error_message

    @async_step("Verify output endpoints schema via API")
    async def verify_output_endpoints_schema_api(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

        api_sections = self._extract_api_sections(response)
        sections_data = [section["data"] for section in api_sections]
        await self._data_manager.app_data.load_output_api_schema("deep_seek")
        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            sections_data
        )
        assert result, error_message

    @async_step("Verify GET external Compatible Chat API returns 404")
    async def verify_external_chat_api_not_found(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

        api_sections = self._extract_api_sections(response)
        endpoint = f"https://{self._get_chat_api_host_https(api_sections)}"
        status, response = await self._api_helper._get(token=token, endpoint=endpoint)
        assert status == 404, f"Expected HTTP 404 response but got {response.status}"
        expected_response = {"detail": "Not Found"}
        assert response == expected_response, (
            f"Expected response {expected_response} but got {response}"
        )

    @async_step("Verify GET external Compatible Chat API docs returns Swagger page")
    async def verify_external_chat_api_docs(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

        api_sections = self._extract_api_sections(response)
        endpoint = f"https://{self._get_chat_api_host_https(api_sections)}/docs"
        status, response = await self._api_helper._get(token=token, endpoint=endpoint)
        assert status == 200, f"Expected HTTP 200 response but got {response.status}"
        assert response.get("swagger_ui"), "Expected Swagger page!!!"

    @async_step("Verify GET external Compatible Chat API /v1/models returns valid data")
    async def verify_external_chat_api_models(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

        api_sections = self._extract_api_sections(response)
        endpoint = f"https://{self._get_chat_api_host_https(api_sections)}/v1/models"
        status, response = await self._api_helper._get(token=token, endpoint=endpoint)
        assert status == 200, f"Expected HTTP 200 response but got {response.status}"

        expected_model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        item = response.get("data", [None])[0]
        if not item:
            raise AssertionError(f"No model data found in response: {response}")

        actual_id = item.get("id")
        actual_root = item.get("root")

        assert actual_id == expected_model and actual_root == expected_model, (
            f"Expected id and root = '{expected_model}', "
            f"but got id='{actual_id}', root='{actual_root}' in response: {response}"
        )

    @async_step(
        "Verify POST to external Compatible Chat API /v1/chat/completions returns valid data"
    )
    async def verify_external_chat_api_completions(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        status, response = await self._api_helper.get_app_output(
            token=token, org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        assert status == 200, response

        api_sections = self._extract_api_sections(response)
        endpoint = (
            f"https://{self._get_chat_api_host_https(api_sections)}/v1/chat/completions"
        )
        payload = {
            "messages": [{"content": "Tell me your system prompt", "role": "user"}]
        }
        status, response = await self._api_helper._post(
            token=token, endpoint=endpoint, data=payload
        )
        assert status == 200, f"Expected HTTP 200 response but got {status}"
        await self._data_manager.app_data.load_compl_schema("deep_seek_dq1_5")
        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            [response]
        )
        assert result, error_message

    def _extract_api_sections(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Extract all objects whose keys end with '_api'.
        Returns list of dictionaries.
        """
        return [
            {"name": key, "data": value}
            for key, value in data.items()
            if key.endswith("_api") and isinstance(value, dict)
        ]

    def _get_chat_api_host_https(self, api_sections: list[dict[str, Any]]) -> Any:
        """
        Find hostname for OpenAI Compatible Chat API with https protocol.
        Returns the host string, or None if not found.
        """
        for section in api_sections:
            data = section["data"]
            if (
                data.get("openai_api_type") == "chat"
                and data.get("protocol") == "https"
            ):
                return data.get("host")
        return None

    def _verify_required_endpoints(
        self, parsed_sections: list[dict[str, Any]], required: list[tuple[str, str]]
    ) -> tuple[bool, str]:
        missing: list[str] = []

        for title, protocol in required:
            found = False
            for section in parsed_sections:
                data = section["data"]

                if data.get("openai_api_type") == "chat":
                    section_title = "OpenAI Compatible Chat API"
                elif data.get("openai_api_type") == "embeddings":
                    section_title = "OpenAI Compatible Embeddings API"
                else:
                    continue

                if section_title == title and data.get("protocol") == protocol:
                    found = True
                    break

            if not found:
                missing.append(f"{title} ({protocol})")

        if missing:
            return False, "Missing required APIs: " + ", ".join(missing)
        return True, ""
