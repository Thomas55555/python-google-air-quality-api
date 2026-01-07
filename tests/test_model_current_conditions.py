"""Snapshot tests for Google Air Quality API client."""

from syrupy.assertion import SnapshotAssertion

from google_air_quality_api.model import (
    AirQualityCurrentConditionsData,
    AQICategoryMapping,
)


def test_air_quality_current_conditions_snapshot(
    snapshot: SnapshotAssertion, air_quality_current_conditions_data: dict
) -> None:
    """Testing a snapshot of air quality data."""
    data = AirQualityCurrentConditionsData.from_dict(
        air_quality_current_conditions_data
    )

    all_options = [idx.category_options for idx in data.indexes]
    assert all_options == snapshot(name="indexes_category_options")

    all_pollutant_options = [idx.pollutant_options for idx in data.indexes]
    assert all_pollutant_options == snapshot(name="indexes_pollutant_options")

    region_codes = AQICategoryMapping.get_all_laq_indices()
    assert region_codes == snapshot(name="aqi_region_codes")

    seen: dict[str, str] = {}
    for cat in AQICategoryMapping.get_all():
        if cat.normalized not in seen:
            seen[cat.normalized] = cat.original
    assert dict(sorted(seen.items())) == snapshot(name="all_aqi_categories")
