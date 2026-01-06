import asyncio
from pathlib import Path
from google_air_quality_api.api import GoogleAirQualityApi
from google_air_quality_api.auth import Auth
import aiohttp
import yaml
import logging
from datetime import timedelta
# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.

file_path = Path("./secrets.yaml")

with file_path.open(encoding="UTF-8") as file:
    secrets = yaml.safe_load(file)


API_KEY = secrets["API_KEY"]


LONGITUDE = secrets["LONGITUDE"]
LATITUDE = secrets["LATITUDE"]


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

        current_conditions = await api.async_get_current_conditions(
            LATITUDE, LONGITUDE, region_code="DE", custom_local_aqi="usa_epa_nowcast"
        )
        print("Current conditions:%s", current_conditions)
        forecast = await api.async_get_forecast(
            LATITUDE, LONGITUDE, forecast_timedelta=timedelta(hours=1)
        )
        print("Forecast:%s", forecast)

        for idx in current_conditions.indexes:
            print(idx.category_options)


if __name__ == "__main__":
    asyncio.run(main())
