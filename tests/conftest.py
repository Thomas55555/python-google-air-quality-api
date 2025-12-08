"""Libraries used in tests."""

import json
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import pytest
from aiohttp import ClientSession, web
from aiohttp.web import Application

from google_air_quality_api.auth import Auth

PATH_PREFIX = "/path-prefix"

AuthCallback = Callable[
    [list[tuple[str, Callable[[web.Request], Awaitable[web.Response]]]]],
    Awaitable[Auth],
]


def load_fixture_json(filename: str) -> Any:
    """Load a fixture and return json."""
    path = Path(__package__) / "fixtures" / filename
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(name="air_quality_data")
def mock_air_quality_data() -> dict:
    """Return air quality data from deu_uba."""
    return load_fixture_json("deu_uba.json")


@pytest.fixture(name="air_quality_forecast_data")
def mock_air_quality_forecast_data() -> dict:
    """Return air quality data from deu_uba."""
    return load_fixture_json("deu_uba_forecast.json")


@pytest.fixture(name="auth_cb")
def mock_auth_fixture(
    aiohttp_client: Callable[[Application], Awaitable[ClientSession]],
) -> AuthCallback:
    """Create a test authentication library with the specified handler."""

    async def create_auth(
        handlers: list[tuple[str, Callable[[web.Request], Awaitable[web.Response]]]],
    ) -> Auth:
        """Create a test authentication library with the specified handler."""
        app = Application()
        for path, handler in handlers:
            app.router.add_get(f"{PATH_PREFIX}{path}", handler)
            app.router.add_post(f"{PATH_PREFIX}{path}", handler)

        client = await aiohttp_client(app)

        return Auth(client, api_key="dummy-key", host=PATH_PREFIX)

    return create_auth
