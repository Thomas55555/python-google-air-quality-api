"""Tests for Google Photos library API."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import patch
import aiohttp
from aiohttp import web
import pytest

from google_air_quality_api.api import GoogleAirQualityApi
from google_air_quality_api.model import (
    UserInfoResult,
)

from .conftest import AuthCallback

FAKE_AIR_QUALITY_DATA = {
    "dateTime": "2025-05-27T08:00:00Z",
    "regionCode": "de",
    "indexes": [
        {
            "code": "uaqi",
            "displayName": "Universal AQI",
            "aqi": 72,
            "aqiDisplay": "72",
            "color": {"red": 0.48235294, "green": 0.79607844, "blue": 0.2},
            "category": "Good air quality",
            "dominantPollutant": "o3",
        },
        {
            "code": "deu_uba",
            "displayName": "LQI (DE)",
            "color": {"red": 0.3137255, "green": 0.8039216, "blue": 0.6666667},
            "category": "Good air quality",
            "dominantPollutant": "no2",
        },
    ],
    "pollutants": [
        {
            "code": "co",
            "displayName": "CO",
            "fullName": "Carbon monoxide",
            "concentration": {"value": 191.97, "units": "PARTS_PER_BILLION"},
        },
        {
            "code": "no2",
            "displayName": "NO2",
            "fullName": "Nitrogen dioxide",
            "concentration": {"value": 16.97, "units": "PARTS_PER_BILLION"},
        },
        {
            "code": "o3",
            "displayName": "O3",
            "fullName": "Ozone",
            "concentration": {"value": 35.17, "units": "PARTS_PER_BILLION"},
        },
        {
            "code": "pm10",
            "displayName": "PM10",
            "fullName": "Inhalable particulate matter (\u003c10µm)",
            "concentration": {"value": 13.53, "units": "MICROGRAMS_PER_CUBIC_METER"},
        },
        {
            "code": "pm25",
            "displayName": "PM2.5",
            "fullName": "Fine particulate matter (\u003c2.5µm)",
            "concentration": {"value": 4.61, "units": "MICROGRAMS_PER_CUBIC_METER"},
        },
        {
            "code": "so2",
            "displayName": "SO2",
            "fullName": "Sulfur dioxide",
            "concentration": {"value": 1.37, "units": "PARTS_PER_BILLION"},
        },
    ],
}


@pytest.fixture(name="get_user_info")
async def mock_get_user_info() -> dict[str, Any]:
    """Fixture for returning fake user info responses."""
    return {
        "id": "user-id-1",
        "name": "User Name",
        "given_name": "User Given Name",
        "family_name": "User Full Name",
        "picture": "http://example.com/profile.jpg",
    }


@pytest.fixture(name="async_air_quality_data")
async def mock_async_air_quality_data() -> dict[str, Any]:
    """Fixture for fake get media item responses."""
    return FAKE_AIR_QUALITY_DATA


@pytest.fixture(name="requests")
async def mock_requests() -> list[web.Request]:
    """Fixture for fake create media items responses."""
    return []


@pytest.fixture(name="api")
async def mock_api(
    auth_cb: AuthCallback,
    requests: list[web.Request],
    get_user_info: dict[str, Any],
    async_air_quality_data: dict[str, Any],
) -> AsyncGenerator[GoogleAirQualityApi, None]:
    """Fixture for fake API object."""

    async def get_user_info_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(get_user_info)

    async def async_air_quality_data_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(async_air_quality_data)

    with patch("google_air_quality_api.api.USERINFO_API", "v1/userInfo"):
        auth = await auth_cb(
            [
                ("/v1/userInfo", get_user_info_handler),
                ("/currentConditions:lookup", async_air_quality_data_handler),
            ]
        )
        yield GoogleAirQualityApi(auth)


async def test_get_user_info(
    api: GoogleAirQualityApi,
    get_user_info: dict[str, Any],
    requests: list[web.Request],
) -> None:
    """Test get user info API."""

    result = await api.get_user_info()
    assert result == UserInfoResult(
        id="user-id-1",
        name="User Name",
    )


async def test_async_air_quality_data(
    api: GoogleAirQualityApi,
    get_user_info: dict[str, Any],
    requests: list[web.Request],
) -> None:
    """Test get user info API."""

    result = await api.async_air_quality(1, 2)
    # assert result == UserInfoResult(
    #     id="user-id-1",
    #     name="User Name",
    # )
