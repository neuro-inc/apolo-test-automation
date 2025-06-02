import requests


class APIHelper:
    """
    Stateless API client using requests, with optional per-request bearer token.
    """

    def __init__(self, timeout=10):
        """
        Initialize the API client.
        Args:
            timeout (int): Timeout in seconds for all requests.
        """
        self.timeout = timeout

    def _headers(self, token=None):
        """
        Construct request headers.
        Args:
            token (str, optional): Bearer token for Authorization header.
        Returns:
            dict: Headers for the HTTP request.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def get(self, endpoint, params=None, token=None):
        """
        Send a GET request.
        Args:
            endpoint (str): Request endpoint.
            params (dict, optional): URL query parameters.
            token (str, optional): Authorization bearer token.
        Returns:
            Response: The HTTP response.
        """
        return requests.get(
            endpoint,
            headers=self._headers(token),
            params=params,
            timeout=self.timeout
        )

    def post(self, endpoint, data=None, token=None):
        """
        Send a POST request.
        Args:
            endpoint (str): Request endpoint.
            data (dict, optional): JSON payload.
            token (str, optional): Authorization bearer token.
        Returns:
            Response: The HTTP response.
        """
        return requests.post(
            endpoint,
            headers=self._headers(token),
            json=data,
            timeout=self.timeout
        )

    def put(self, endpoint, data=None, token=None):
        """
        Send a PUT request.
        Args:
            endpoint (str): Request endpoint.
            data (dict, optional): JSON payload.
            token (str, optional): Authorization bearer token.
        Returns:
            Response: The HTTP response.
        """
        return requests.put(
            endpoint,
            headers=self._headers(token),
            json=data,
            timeout=self.timeout
        )

    def delete(self, endpoint, token=None):
        """
        Send a DELETE request.
        Args:
            endpoint (str): Request endpoint.
            token (str, optional): Authorization bearer token.
        Returns:
            Response: The HTTP response.
        """
        return requests.delete(
            endpoint,
            headers=self._headers(token),
            timeout=self.timeout
        )
