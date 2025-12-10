"""Snapshot tests for Google Air Quality API client for a specific country."""

import json
from dataclasses import fields
from pathlib import Path
from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion

from google_air_quality_api.model import (
    AirQualityCurrentConditionsData,
    AQICategoryMapping,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "specific"


def load_json(path: Path) -> Any:
    """Load a fixture and return json."""
    return json.loads(path.read_text(encoding="utf-8"))


fixture_files = sorted(FIXTURE_DIR.glob("*.json"))


@pytest.mark.parametrize("fixture_path", fixture_files)
def test_air_quality_current_conditions_snapshot(
    snapshot: SnapshotAssertion,
    fixture_path: Path,
) -> None:
    """Snapshot per-country Current Conditions JSON file, inkl. AQI-Mapping."""
    data_raw = load_json(fixture_path)
    data = AirQualityCurrentConditionsData.from_dict(data_raw)

    stem = fixture_path.stem
    for field in fields(data):
        value = getattr(data, field.name)
        assert value == snapshot(name=f"{stem}_{field.name}")

    assert data.indexes[1].category == snapshot(name=f"{stem}_{'category_normalized'}")
    mapping = AQICategoryMapping._mapping[data.indexes[1].code]  # noqa: SLF001
    original_category = next(
        cat.original for cat in mapping if cat.normalized == data.indexes[1].category
    )
    assert original_category == snapshot(name=f"{stem}_category_original")
