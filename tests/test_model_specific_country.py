"""Snapshot tests for Google Air Quality API client for a specific country."""

import json
from dataclasses import fields
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from google_air_quality_api.model import (
    AirQualityCurrentConditionsData,
    AQICategoryMapping,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "specific"
fixture_files = sorted(FIXTURE_DIR.glob("*.json"))


@pytest.mark.parametrize(
    "fixture_path",
    fixture_files,
    ids=lambda path: path.stem,
)
def test_air_quality_current_conditions_snapshot(
    snapshot: SnapshotAssertion,
    fixture_path: Path,
) -> None:
    """Snapshot per-country Current Conditions JSON file, inkl. AQI-Mapping."""
    data_raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    data = AirQualityCurrentConditionsData.from_dict(data_raw)

    for field in fields(data):
        value = getattr(data, field.name)
        assert value == snapshot(name=field.name)

    assert data.indexes.laqi.category == snapshot(name="category_normalized")
    mapping = AQICategoryMapping.get(data.indexes.laqi.code)
    original_category = next(
        cat.original for cat in mapping if cat.normalized == data.indexes.laqi.category
    )
    assert original_category == snapshot(name="category_original")
