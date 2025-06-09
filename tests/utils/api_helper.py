import aiohttp
from typing import Any, Optional, Union


class APIHelper:
    """
    Stateless API client using aiohttp, with optional per-request bearer token.
    """

    def __init__(self, timeout: int = 10) -> None:
        """
        Initialize the API client and aiohttp session.
        Args:
            timeout (int): Timeout in seconds for all requests.
        """
        self._timeout = timeout
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self._timeout)
        )

    def _headers(self, token: Optional[str] = None) -> dict[str, str]:
        """
        Construct request headers.
        Args:
            token (str, optional): Bearer token for Authorization header.
        Returns:
            dict: Headers for the HTTP request.
        """
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        token: Optional[str] = None,
    ) -> Any:
        async with self._session.get(
            endpoint, headers=self._headers(token), params=params
        ) as response:
            return await response.json()

    async def post(
        self,
        endpoint: str,
        data: Optional[Union[dict[str, Any], list[Any]]] = None,
        token: Optional[str] = None,
    ) -> Any:
        async with self._session.post(
            endpoint, headers=self._headers(token), json=data
        ) as response:
            return await response.json()

    async def put(
        self,
        endpoint: str,
        data: Optional[Union[dict[str, Any], list[Any]]] = None,
        token: Optional[str] = None,
    ) -> Any:
        async with self._session.put(
            endpoint, headers=self._headers(token), json=data
        ) as response:
            return await response.json()

    async def delete(self, endpoint: str, token: Optional[str] = None) -> Any:
        async with self._session.delete(
            endpoint, headers=self._headers(token)
        ) as response:
            return await response.json()

    async def close(self) -> None:
        """
        Close the aiohttp session.
        """
        await self._session.close()
