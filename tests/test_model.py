"""Tests for asynchronous Python client for aioautomower."""

from dataclasses import fields

from syrupy.assertion import SnapshotAssertion
import pytest
from google_air_quality_api.model import AirQualityData, AQICategoryMapping
from typing import Any

MOWER_ID = "1234"

FAKE_AIR_QUALITY_DATA = {
    "dateTime": "2025-05-25T08:00:00Z",
    "regionCode": "de",
    "indexes": [
        {
            "code": "uaqi",
            "displayName": "Universal AQI",
            "aqi": 71,
            "aqiDisplay": "71",
            "color": {"red": 0.48235294, "green": 0.79607844, "blue": 0.2},
            "category": "Good air quality",
            "dominantPollutant": "o3",
        },
        {
            "code": "deu_uba",
            "displayName": "LQI (DE)",
            "color": {"red": 0.3137255, "green": 0.8039216, "blue": 0.6666667},
            "category": "Good air quality",
            "dominantPollutant": "no2",
        },
    ],
    "pollutants": [
        {
            "code": "co",
            "displayName": "CO",
            "fullName": "Carbon monoxide",
            "concentration": {"value": 191.97, "units": "PARTS_PER_BILLION"},
        },
        {
            "code": "no2",
            "displayName": "NO2",
            "fullName": "Nitrogen dioxide",
            "concentration": {"value": 16.97, "units": "PARTS_PER_BILLION"},
        },
        {
            "code": "o3",
            "displayName": "O3",
            "fullName": "Ozone",
            "concentration": {"value": 35.17, "units": "PARTS_PER_BILLION"},
        },
        {
            "code": "pm10",
            "displayName": "PM10",
            "fullName": "Inhalable particulate matter (\u003c10µm)",
            "concentration": {"value": 13.53, "units": "MICROGRAMS_PER_CUBIC_METER"},
        },
        {
            "code": "pm25",
            "displayName": "PM2.5",
            "fullName": "Fine particulate matter (\u003c2.5µm)",
            "concentration": {"value": 4.61, "units": "MICROGRAMS_PER_CUBIC_METER"},
        },
        {
            "code": "so2",
            "displayName": "SO2",
            "fullName": "Sulfur dioxide",
            "concentration": {"value": 1.37, "units": "PARTS_PER_BILLION"},
        },
    ],
}


@pytest.fixture(name="async_air_quality_data")
async def mock_async_air_quality_data() -> dict[str, Any]:
    """Fixture for fake get media item responses."""
    return FAKE_AIR_QUALITY_DATA


def test_mower_snapshot(snapshot: SnapshotAssertion) -> None:
    """Testing a snapshot of a high feature mower."""
    data = AirQualityData.from_dict(FAKE_AIR_QUALITY_DATA)

    # 1) Snapshot jedes einzelnen Feldes
    for field in fields(data):
        field_name = field.name
        field_value = getattr(data, field_name)
        assert field_value == snapshot(name=f"{field_name}")

    # 2) Zusätzlich: snapshotten der category_options aller Index-Einträge
    all_options = [idx.category_options for idx in data.indexes]
    assert all_options == snapshot(name="indexes_category_options")

    seen: dict[str, str] = {}
    for cat in AQICategoryMapping.get_all():
        if cat.normalized not in seen:
            seen[cat.normalized] = cat.original
    assert dict(sorted(seen.items())) == snapshot(name="all_aqi_categories")
