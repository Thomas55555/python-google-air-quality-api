import asyncio
import json
from pathlib import Path
from typing import Any
from google_air_quality_api.api import GoogleAirQualityApi
from google_air_quality_api.auth import Auth
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


API_KEY = secrets["API_KEY"]


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


async def main() -> None:
    configure_logging(logging.DEBUG)
    async with aiohttp.ClientSession() as websession:
        auth = Auth(websession, API_KEY)
        api = GoogleAirQualityApi(auth)
        response = await api.async_heatmap(LATITUDE, LONGITUDE, ZOOM)

        async with response:
            if response.status == 200:
                content = await response.read()
                async with aiofiles.open(OUTPUT_FILE, "wb") as f:
                    await f.write(content)
                print(f"Picture saved as {OUTPUT_FILE}")
            else:
                print(f"Error getting picture: {response.status}")

            response = await api.async_air_quality(LATITUDE, LONGITUDE)
            print("Air Quality Data:%s", response)

            for idx in response.indexes:
                print(idx.category_options)

        response = await api.async_reverse_geocode(LATITUDE, LONGITUDE)
        print("location:%s", response.results[0].formatted_address)


if __name__ == "__main__":
    asyncio.run(main())
