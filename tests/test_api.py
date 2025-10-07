"""Tests for Google Air Quality library API."""

from typing import Any

import pytest
from aiohttp import web

from google_air_quality_api.api import GoogleAirQualityApi
from tests.conftest import AuthCallback


@pytest.fixture(name="requests")
async def mock_requests() -> list[web.Request]:
    """Fixture for fake air quality data responses."""
    return []


@pytest.fixture(name="api")
async def mock_api(
    auth_cb: AuthCallback,
    requests: list[web.Request],
    air_quality_data: dict[str, Any],
) -> GoogleAirQualityApi:
    """Fixture for fake API object."""

    async def async_air_quality_data_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(air_quality_data)

    auth = await auth_cb(
        [
            ("/currentConditions:lookup", async_air_quality_data_handler),
        ]
    )

    return GoogleAirQualityApi(auth)


async def test_async_air_quality_data(
    api: GoogleAirQualityApi,
) -> None:
    """Test get user info API."""
    result = await api.async_air_quality(1, 2)
    assert result is not None
