"""Exceptions for Google Air Quality API calls."""


class GoogleAirQualityApiError(Exception):
    """Error talking to the Google Air Quality API."""


class ApiError(GoogleAirQualityApiError):
    """Raised during problems talking to the API."""


class AuthError(GoogleAirQualityApiError):
    """Raised due to auth problems talking to API."""


class ApiForbiddenError(GoogleAirQualityApiError):
    """Raised due to permission errors talking to API."""


class NoDataForLocationError(GoogleAirQualityApiError):
    """Raised due to permission errors talking to API."""


class InvalidAqiConfigurationError(GoogleAirQualityApiError):
    """Invalid combination of region_code and custom_local_aqi."""


class UnsupportedLocalAqiForCountryError(GoogleAirQualityApiError):
    """Raised when a local AQI is not supported for the given country."""
