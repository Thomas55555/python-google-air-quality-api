"""Tests for Google Photos library API."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import patch

from aiohttp import web
import pytest

from google_air_quality_api.api import GooglePhotosLibraryApi
from google_air_quality_api.model import (
    UserInfoResult,
)

from .conftest import AuthCallback

FAKE_MEDIA_ITEM = {
    "id": "media-item-id-1",
    "description": "Photo 1",
}
FAKE_MEDIA_ITEM2 = {
    "id": "media-item-id-2",
    "description": "Photo 2",
}
FAKE_LIST_MEDIA_ITEMS = {
    "mediaItems": [FAKE_MEDIA_ITEM],
}
FAKE_ALBUM = {
    "id": "album-id-1",
    "title": "Album 1",
}


@pytest.fixture(name="get_user_info")
async def mock_get_user_info() -> list[dict[str, Any]]:
    """Fixture for returning fake user info responses."""
    return []


@pytest.fixture(name="get_media_item")
async def mock_get_media_item() -> list[dict[str, Any]]:
    """Fixture for fake get media item responses."""
    return []


@pytest.fixture(name="list_media_items")
async def mock_list_media_items() -> list[dict[str, Any]]:
    """Fixture for fake list media items responses."""
    return []


@pytest.fixture(name="search_media_items")
async def mock_search_media_items() -> list[dict[str, Any]]:
    """Fixture for fake search media items responses."""
    return []


@pytest.fixture(name="upload_media_items")
async def mock_upload_media_items() -> list[str]:
    """Fixture for fake list upload endpoint responses."""
    return []


@pytest.fixture(name="create_media_items")
async def mock_create_media_items() -> list[dict[str, Any]]:
    """Fixture for fake create media items responses."""
    return []


@pytest.fixture(name="get_album")
async def mock_get_album() -> list[dict[str, Any]]:
    """Fixture for fake album responses."""
    return []


@pytest.fixture(name="albums")
async def mock_albums() -> list[dict[str, Any]]:
    """Fixture for fake list albums responses."""
    return []


@pytest.fixture(name="create_album")
async def mock_create_album() -> list[dict[str, Any]]:
    """Fixture for fake create album responses."""
    return []


@pytest.fixture(name="requests")
async def mock_requests() -> list[web.Request]:
    """Fixture for fake create media items responses."""
    return []


@pytest.fixture(name="api")
async def mock_api(
    auth_cb: AuthCallback,
    requests: list[web.Request],
    get_user_info: list[dict[str, Any]],
    get_media_item: list[dict[str, Any]],
    list_media_items: list[dict[str, Any]],
    search_media_items: list[dict[str, Any]],
    get_album: list[dict[str, Any]],
    albums: list[dict[str, Any]],
    upload_media_items: list[str],
    create_media_items: list[dict[str, Any]],
    create_album: list[dict[str, Any]],
) -> AsyncGenerator[GooglePhotosLibraryApi, None]:
    """Fixture for fake API object."""

    async def get_user_info_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(get_user_info.pop(0))

    async def get_media_item_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(get_media_item.pop(0))

    async def list_media_items_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(list_media_items.pop(0))

    async def search_media_items_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(search_media_items.pop(0))

    async def get_album_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(get_album.pop(0))

    async def albums_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(albums.pop(0))

    async def upload_media_items_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.Response(body=upload_media_items.pop(0))

    async def create_media_items_handler(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(create_media_items.pop(0))

    async def async_create_album(
        request: web.Request,
    ) -> web.Response:
        requests.append(request)
        return web.json_response(create_album.pop(0))

    with patch("google_air_quality_api.api.USERINFO_API", "v1/userInfo"):
        auth = await auth_cb(
            [
                ("/v1/userInfo", get_user_info_handler),
                ("/v1/mediaItems", list_media_items_handler),
                ("/v1/mediaItems/{media_item_id}", get_media_item_handler),
                ("/v1/mediaItems:search", search_media_items_handler),
                ("/v1/albums", albums_handler),
                ("/v1/albums/{album_id}", get_album_handler),
                ("/v1/uploads", upload_media_items_handler),
                ("/v1/mediaItems:batchCreate", create_media_items_handler),
            ]
        )
        yield GooglePhotosLibraryApi(auth)


async def test_get_user_info(
    api: GooglePhotosLibraryApi,
    get_user_info: list[dict[str, Any]],
    requests: list[web.Request],
) -> None:
    """Test get user info API."""

    get_user_info.append(
        {
            "id": "user-id-1",
            "name": "User Name",
            "given_name": "User Given Name",
            "family_name": "User Full Name",
            "picture": "http://example.com/profile.jpg",
        }
    )
    result = await api.get_user_info()
    assert result == UserInfoResult(
        id="user-id-1",
        name="User Name",
    )
