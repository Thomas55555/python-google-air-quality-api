"""Libraries used in tests."""

from collections.abc import Awaitable, Callable

from aiohttp import web
import pytest
from aiohttp import ClientSession
from aiohttp.web import Application

from google_air_quality_api.auth import AbstractAuth
from pathlib import Path
from typing import Any
import json

PATH_PREFIX = "/path-prefix"

AuthCallback = Callable[
    [list[tuple[str, Callable[[web.Request], Awaitable[web.Response]]]]],
    Awaitable[AbstractAuth],
]


def load_fixture_json(filename: str) -> Any:
    """Load a fixture and return json."""
    path = Path(__package__) / "fixtures" / filename
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(name="air_quality_data")
def mock_air_quality_data() -> dict:
    """Return snapshot assertion fixture with the Automower extension."""
    return load_fixture_json("deu_uba.json")


class FakeAuth(AbstractAuth):
    """Implementation of AbstractAuth for use in tests."""

    async def async_get_access_token(self) -> str:
        """Return an OAuth credential for the calendar API."""
        return "some-token"


@pytest.fixture(name="auth_cb")
def mock_auth_fixture(
    aiohttp_client: Callable[[Application], Awaitable[ClientSession]],
) -> AuthCallback:
    async def create_auth(
        handlers: list[tuple[str, Callable[[web.Request], Awaitable[web.Response]]]],
    ) -> AbstractAuth:
        """Create a test authentication library with the specified handler."""
        app = Application()
        for path, handler in handlers:
            app.router.add_get(f"{PATH_PREFIX}{path}", handler)
            app.router.add_post(f"{PATH_PREFIX}{path}", handler)

        client = await aiohttp_client(app)
        return FakeAuth(client, PATH_PREFIX)

    return create_auth
