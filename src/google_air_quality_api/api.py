"""API for Google Air Quality bound to Home Assistant OAuth."""

import logging

from .auth import Auth
from .model import AirQualityData

_LOGGER = logging.getLogger(__name__)

CURRENT_CONDITIONS = "currentConditions:lookup"


class GoogleAirQualityApi:
    """The Google Air Quality library api client."""

    def __init__(self, auth: Auth) -> None:
        """Initialize GoogleAirQualityApi."""
        self._auth = auth

    async def async_air_quality(self, lat: float, long: float) -> AirQualityData:
        """Get all air quality data."""
        payload = {
            "location": {"latitude": lat, "longitude": long},
            "extraComputations": [
                "LOCAL_AQI",
                "POLLUTANT_CONCENTRATION",
            ],
            "universalAqi": True,
        }
        return await self._auth.post_json(
            CURRENT_CONDITIONS, json=payload, data_cls=AirQualityData
        )
