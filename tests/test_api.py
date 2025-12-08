"""Tests for Google Air Quality library API."""

from datetime import timedelta
from typing import Any

import pytest
from aiohttp import web

from google_air_quality_api.api import GoogleAirQualityApi

from .conftest import AuthCallback


@pytest.fixture(name="requests")
async def mock_requests() -> list[web.Request]:
    """Fixture for fake air quality data responses."""
    return []


@pytest.fixture(name="api")
async def mock_api(
    auth_cb: AuthCallback,
    requests: list[web.Request],
    air_quality_current_conditions_data: dict[str, Any],
    air_quality_forecast_data: dict[str, Any],
) -> GoogleAirQualityApi:
    """Fixture for fake API object."""

    async def async_get_current_conditions_data_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(air_quality_current_conditions_data)

    async def async_get_forecast_data_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(air_quality_forecast_data)

    auth = await auth_cb(
        [
            (
                "/currentConditions:lookup",
                async_get_current_conditions_data_handler,
            ),
            (
                "/forecast:lookup",
                async_get_forecast_data_handler,
            ),
        ]
    )

    return GoogleAirQualityApi(auth)


async def test_async_get_current_conditions_data(
    api: GoogleAirQualityApi,
) -> None:
    """Test get current conditions API."""
    result = await api.async_get_current_conditions(1, 2)
    assert result is not None


async def test_async_get_forecast(api: GoogleAirQualityApi) -> None:
    """Test forecast lookup API."""
    result = await api.async_get_forecast(1.0, 2.0, timedelta(hours=1))

    assert result is not None
