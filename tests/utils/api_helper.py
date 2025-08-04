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

    def __init__(self, config: ConfigManager, timeout: int = 10) -> None:
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
    ) -> Any:
        assert self._session is not None, "ClientSession is not initialized"
        logger.info(f"GET {endpoint}")
        async with self._session.get(
            endpoint, headers=self._headers(token), params=params
        ) as response:
            status = response.status
            json_data = await response.json()
            return status, json_data

    async def _post(
        self,
        endpoint: str,
        data: Optional[Union[dict[str, Any], list[Any]]] = None,
        token: Optional[str] = None,
    ) -> Any:
        assert self._session is not None, "ClientSession is not initialized"
        async with self._session.post(
            endpoint, headers=self._headers(token), json=data
        ) as response:
            return await response.json()

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

    async def delete_org(self, token: str, org_name: str) -> Any:
        url = self._config.get_delete_org_url(org_name=org_name)
        response = await self._delete(url, token=token)
        logger.info(f"Delete organization response: {response}")

        return response
