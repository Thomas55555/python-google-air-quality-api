"""Exceptions for Google Photos API calls."""


class GooglePhotosApiError(Exception):
    """Error talking to the Google Photos API."""


class ApiError(GooglePhotosApiError):
    """Raised during problems talking to the API."""


class AuthError(GooglePhotosApiError):
    """Raised due to auth problems talking to API."""


class ApiForbiddenError(GooglePhotosApiError):
    """Raised due to permission errors talking to API."""


class NoDataForLocationError(GooglePhotosApiError):
    """Raised due to permission errors talking to API."""
