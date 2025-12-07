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
        auth = Auth(websession, API_KEY, referrer="https://storage.googleapis.com")
        api = GoogleAirQualityApi(auth)

        response = await api.async_get_current_conditions(LATITUDE, LONGITUDE)
        print("Air Quality Data:%s", response)
        response = await api.async_get_forecast(LATITUDE, LONGITUDE, date_time=1)
        print("Forecast:%s", response)

        for idx in response.indexes:
            print(idx.category_options)


if __name__ == "__main__":
    asyncio.run(main())
