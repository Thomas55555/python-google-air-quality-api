"""Snapshot tests for Google Air Quality API client."""

from dataclasses import fields

from syrupy.assertion import SnapshotAssertion
import pytest
from google_air_quality_api.model import AirQualityData, AQICategoryMapping
from typing import Any


def test_air_quality_snapshot(
    snapshot: SnapshotAssertion, air_quality_data: dict
) -> None:
    """Testing a snapshot of air quality data."""
    data = AirQualityData.from_dict(air_quality_data)

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
