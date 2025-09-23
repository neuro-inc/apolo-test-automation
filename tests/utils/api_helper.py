from __future__ import annotations

import base64
import logging
import os

import aiohttp
from typing import Any, Optional, Union

from tests.utils.test_config_helper import ConfigManager

logger = logging.getLogger("[🌐API_helper]")


class APIHelper:
    """
    Stateless API client using aiohttp, with optional per-request bearer token.
    """

    def __init__(self, config: ConfigManager, timeout: int = 60) -> None:
        self._config = config
        self._timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None

    async def init(self) -> "APIHelper":
        """
        Async initializer to create aiohttp session safely.
        """
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self._timeout)
        )
        return self

    def _headers(self, token: Optional[str] = None) -> dict[str, str]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def _get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        token: Optional[str] = None,
    ) -> tuple[int, Any]:
        """
        Make GET request.
        Returns (status, response_data).
        - If JSON → returns parsed JSON dict.
        - If HTML Swagger UI → returns {"swagger_ui": True, "content": text}.
        - Otherwise → returns raw text.
        """
        assert self._session is not None, "ClientSession is not initialized"
        logger.info(f"GET {endpoint}")

        async with self._session.get(
            endpoint, headers=self._headers(token), params=params
        ) as response:
            status = response.status
            content_type = response.headers.get("content-type", "")

            # Try JSON if content type is JSON
            if "application/json" in content_type:
                try:
                    json_data = await response.json()
                    return status, json_data
                except Exception:
                    pass

            # Fallback to text
            text = await response.text()

            # Detect Swagger UI page
            if "swagger" in text.lower() and "<html" in text.lower():
                return status, {"swagger_ui": True, "content": text}

            return status, text

    async def _post(
        self,
        endpoint: str,
        data: Optional[Union[dict[str, Any], list[Any]]] = None,
        token: Optional[str] = None,
    ) -> tuple[int, Any]:
        assert self._session is not None, "ClientSession is not initialized"
        logger.info(f"POST {endpoint} with data: {data}")

        async with self._session.post(
            endpoint, headers=self._headers(token), json=data
        ) as response:
            status = response.status
            content_type = response.headers.get("Content-Type", "")

            try:
                if "application/json" in content_type:
                    result = await response.json()
                else:
                    result = await response.text()
            except Exception:
                result = await response.text()

            return status, result

    async def _put(
        self,
        endpoint: str,
        data: Optional[Union[dict[str, Any], list[Any], bytes]] = None,
        token: Optional[str] = None,
        is_json: bool = True,
    ) -> Any:
        assert self._session is not None, "ClientSession is not initialized"
        if is_json and isinstance(data, (dict, list)):
            async with self._session.put(
                endpoint, headers=self._headers(token), json=data
            ) as response:
                return await response.json()
        else:
            async with self._session.put(
                endpoint, headers=self._headers(token), data=data
            ) as response:
                return response

    async def _delete(self, endpoint: str, token: Optional[str] = None) -> Any:
        assert self._session is not None, "ClientSession is not initialized"
        async with self._session.delete(
            endpoint, headers=self._headers(token)
        ) as response:
            return response

    async def _close(self) -> None:
        if self._session:
            await self._session.close()

    async def check_user_needs_verification(self, email: str) -> tuple[bool, str]:
        """
        Check user signup status using the verification ticket API.
        Returns:
            (True, ticket_link) if email is unverified.
            (False, message) if already verified.
        Raises:
            ValueError if user not found.
        """
        url = self._config.get_signup_status_url(email)
        logger.info(f"Checking if user {email} needs verification...")
        status, response = await self._get(url)
        logger.info(f"Status: {status}. Response: {response}")

        if status == 200:
            if response.get("detail") == "Email already verified":
                return False, "Email already verified"
            elif "ticket" in response:
                return True, response["ticket"]
            else:
                return False, "unknown response"
        elif status == 409:
            raise ValueError(response)
        else:
            raise RuntimeError(f"Unexpected response: {status}, {response}")

    async def upload_file(
        self, token: str, organization: str, project_name: str, file_path: str
    ) -> Any:
        file_name = os.path.basename(file_path)
        url = self._config.get_file_upload_url(organization, project_name, file_name)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            response = await self._put(url, data=file_bytes, token=token)
            logger.info(f"File upload response: {response}")

        return response

    async def get_orgs(self, token: str) -> Any:
        url = self._config.get_orgs_url()
        status, response = await self._get(url, token=token)
        logger.info(f"Status: {status}. Response: {response}")

        return response

    async def delete_org(self, token: str, org_name: str) -> Any:
        url = self._config.get_delete_org_url(org_name=org_name)
        response = await self._delete(url, token=token)
        logger.info(f"Delete organization response: {response}")

        return response

    async def add_user_to_org(
        self, token: str, org_name: str, username: str, role: str
    ) -> Any:
        url = self._config.get_add_user_to_org_url(org_name=org_name)
        data = {"user_name": username, "role": role}
        status, response = await self._post(url, token=token, data=data)
        logger.info(f"Add user {username} to org response: {response}")

        return status, response

    async def add_org(self, token: str, org_name: str) -> Any:
        url = self._config.get_add_org_url()
        data = {"name": org_name}
        status, response = await self._post(url, token=token, data=data)
        logger.info(f"Add org {org_name} response: {response}")

        return status, response

    async def add_proj(
        self,
        token: str,
        org_name: str,
        proj_name: str,
        default_role: str,
        proj_default: bool,
    ) -> Any:
        url = self._config.get_add_proj_url(org_name=org_name)
        data = {
            "name": proj_name,
            "default_role": default_role,
            "is_default": proj_default,
        }
        status, response = await self._post(url, token=token, data=data)
        logger.info(f"Add proj {org_name} response: {response}")

        return status, response

    async def get_app_output(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        url = self._config.get_app_output_url(
            org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        status, response = await self._get(url, token=token)
        logger.info(f"Status: {status}. Response: {response}")

        return status, response

    async def get_app_events(
        self, token: str, org_name: str, proj_name: str, app_id: str
    ) -> Any:
        url = self._config.get_app_events_url(
            org_name=org_name, proj_name=proj_name, app_id=app_id
        )
        status, response = await self._get(url, token=token)
        logger.info(f"Status: {status}. Response: {response}")

        return status, response

    async def get_instances(self, token: str, org_name: str, proj_name: str) -> Any:
        url = self._config.get_instances_url(org_name=org_name, proj_name=proj_name)
        status, response = await self._get(url, token=token)
        logger.info(f"Status: {status}. Response: {response}")

        return status, response

    async def get_app_instance(self, app_id: str, token: str) -> Any:
        url = self._config.get_app_instance_url(app_id=app_id)
        status, response = await self._get(url, token=token)
        logger.info(f"Status: {status}. Response: {response}")

        return status, response

    async def verify_app_instance_info(
        self,
        token: str,
        expected_owner: str,
        app_id: str,
        expected_app_name: str,
        expected_proj_name: str,
        expected_org_name: str,
    ) -> tuple[bool, str]:
        mismatches: list[str] = []

        status, response = await self.get_app_instance(app_id=app_id, token=token)

        if status != 200:
            return False, f"Expected status 200, got {status}"

        actual_owner = response.get("creator", "").strip()
        actual_app_id = response.get("id", "").strip()
        actual_app_name = response.get("display_name", "").strip()
        actual_proj_name = response.get("project_name", "").strip()
        actual_org_name = response.get("org_name", "").strip()

        if actual_owner != expected_owner:
            mismatches.append(
                f"Owner expected '{expected_owner}', got '{actual_owner}'"
            )
        if actual_app_id != app_id:
            mismatches.append(f"ID expected '{app_id}', got '{actual_app_id}'")
        if actual_app_name != expected_app_name:
            mismatches.append(
                f"Display Name expected '{expected_app_name}', got '{actual_app_name}'"
            )
        if actual_proj_name != expected_proj_name:
            mismatches.append(
                f"Project expected '{expected_proj_name}', got '{actual_proj_name}'"
            )
        if actual_org_name != expected_org_name:
            mismatches.append(
                f"Organization expected '{expected_org_name}', got '{actual_org_name}'"
            )

        if mismatches:
            return False, "; ".join(mismatches)
        return True, "All fields matched"

    async def add_secret(
        self,
        token: str,
        org_name: str,
        proj_name: str,
        secret_name: str,
        secret_value: str,
    ) -> Any:
        url = self._config.get_create_secret_url()
        encoded_value = base64.b64encode(secret_value.encode()).decode()
        data = {
            "key": secret_name,
            "value": encoded_value,
            "org_name": org_name,
            "project_name": proj_name,
        }
        status, response = await self._post(url, token=token, data=data)
        logger.info(f"Add secret {secret_name} response: {response}")

        return status, response
