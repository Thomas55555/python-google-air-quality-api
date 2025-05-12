"""API for Google Air Quality bound to Home Assistant OAuth."""

import logging
from .const import API_BASE_URL
from .auth import AbstractAuth
from .model import AirQualityData, UserInfoResult


_LOGGER = logging.getLogger(__name__)


USERINFO_API = "https://www.googleapis.com/oauth2/v1/userinfo"
CURRENT_CONDITIONS = f"{API_BASE_URL}airQuality/currentConditions"


class GoogleAirQualityApi:
    """The Google Photos library api client."""

    def __init__(self, auth: AbstractAuth) -> None:
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
            "customLocalAqis": [
                {"regionCode": "DE", "aqi": "USA_EPA_NOWCAST"},
            ],
            "universalAqi": True,
        }
        return await self._auth.post_json(
            CURRENT_CONDITIONS, json=payload, data_cls=AirQualityData
        )

    async def get_user_info(self) -> UserInfoResult:
        """Get the user profile info.

        This call requires the userinfo.email scope.
        """
        return await self._auth.get_json(USERINFO_API, data_cls=UserInfoResult)
