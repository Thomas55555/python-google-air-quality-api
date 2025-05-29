import asyncio
import json
from pathlib import Path
from typing import Any
from google_air_quality_api.api import GoogleAirQualityApi
from google_air_quality_api.auth import AbstractAuth
from google_air_quality_api.const import API_BASE_URL
import aiohttp
import aiofiles
import yaml
import logging
# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.

file_path = Path("./secrets.yaml")

with file_path.open(encoding="UTF-8") as file:
    secrets = yaml.safe_load(file)


CLIENT_ID = secrets["CLIENT_ID"]
CLIENT_SECRET = secrets["CLIENT_SECRET"]

OAUTH2_SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.profile",
]

TOKEN_FILE = Path("oauth_token.json")
REDIRECT_URI = "http://localhost:8080/"
SCOPE = " ".join(OAUTH2_SCOPES)

LONGITUDE = secrets["LONGITUDE"]
LATITUDE = secrets["LATITUDE"]
ZOOM = 4
OUTPUT_FILE = "air_quality.png"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging with specified level."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class AsyncTokenAuth(AbstractAuth):
    """Provide Automower authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: aiohttp.ClientSession,
    ) -> None:
        """Initialize Husqvarna Automower auth."""
        super().__init__(websession, API_BASE_URL)
        self.token: dict = {}

    async def get_auth_code(self) -> str:
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&response_type=code"
            f"&scope={SCOPE}"
            f"&access_type=offline"
            f"&prompt=consent"
        )
        print("Bitte öffne folgenden Link im Browser und gib den Code ein:")
        print(auth_url)
        return input("Code: ").strip()

    async def exchange_code_for_token(self, code: str) -> dict[str, Any]:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def async_get_access_token(self) -> str:
        if TOKEN_FILE.exists():
            with TOKEN_FILE.open("r", encoding="utf-8") as f:
                token_data = json.load(f)
            if "refresh_token" in token_data:
                new_token = await self.refresh_token(token_data["refresh_token"])
                token_data.update(new_token)
                with TOKEN_FILE.open("w", encoding="utf-8") as f:
                    json.dump(token_data, f, indent=2)
                return token_data["access_token"]

        code = await self.get_auth_code()
        token_data = await self.exchange_code_for_token(code)
        with TOKEN_FILE.open("w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2)
        return token_data["access_token"]


async def main() -> None:
    configure_logging(logging.DEBUG)
    async with aiohttp.ClientSession() as websession:
        api = GoogleAirQualityApi(AsyncTokenAuth(websession))
        response = await api.async_heatmap(LATITUDE, LONGITUDE, ZOOM)

        async with response:
            if response.status == 200:
                content = await response.read()
                async with aiofiles.open(OUTPUT_FILE, "wb") as f:
                    await f.write(content)
                print(f"Picture saved as {OUTPUT_FILE}")
            else:
                print(f"Error getting picture: {response.status}")

            user = await api.get_user_info()
            response = await api.async_air_quality(LATITUDE, LONGITUDE)
            print("Air Quality Data:%s", response)
            print("Air Quality Data:%s", response)

            for idx in response.indexes:
                print(idx.category_options)
                print(idx.pollutant_options)


if __name__ == "__main__":
    asyncio.run(main())
