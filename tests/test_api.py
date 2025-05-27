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


@pytest.fixture(name="requests")
async def mock_requests() -> list[web.Request]:
    """Fixture for fake create media items responses."""
    return []


@pytest.fixture(name="api")
async def mock_api(
    auth_cb: AuthCallback,
    requests: list[web.Request],
    get_user_info: dict[str, Any],
    air_quality_data: dict[str, Any],
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
        return web.json_response(air_quality_data)

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
    assert result is not None
