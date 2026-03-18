"""Thin HTTP client for Elephantasm API."""

from typing import Any

import httpx

from .config import settings


class ElephantasmClient:
    """HTTP client wrapping the Elephantasm REST API."""

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str | None = None,
        timeout: int = 30,
    ):
        self._api_key = api_key or settings.api_key
        self._endpoint = (endpoint or settings.endpoint).rstrip("/")

        if not self._api_key:
            raise ValueError(
                "API key required. Set ELEPHANTASM_API_KEY or pass api_key."
            )

        self._client = httpx.Client(
            base_url=self._endpoint,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        """POST request, returns parsed JSON."""
        response = self._client.post(path, json=json)
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """GET request, returns parsed JSON."""
        response = self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self._client.close()
