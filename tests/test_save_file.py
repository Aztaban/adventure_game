import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from game.save_file import (
    SAVE_FORMAT_VERSION,
    SaveFileEnvelope,
    SaveFileStatus,
    create_save_file_envelope,
    inspect_save_file,
    inspect_save_file_text,
    validate_save_file_data,
)
from game.state_snapshot import SAVE_DATA_VERSION, GameSnapshot


@dataclass
class SnapshotContentStub:
    scenes_by_id: dict[str, object] = field(default_factory=lambda: {"scene.start": object()})
    items_by_id: dict[str, object] = field(default_factory=lambda: {"item.cup": object()})
    flag_ids: frozenset[str] = frozenset({"flag.ready"})
    pickup_ids: frozenset[str] = frozenset({"pickup.cup"})
    interaction_ids: frozenset[str] = frozenset({"interaction.well"})

    def build_scenes(self, *_args: object, **_kwargs: object) -> None:
        pytest.fail("Save-file validation must not construct scenes or sessions.")


def valid_snapshot() -> GameSnapshot:
    return {
        "save_version": SAVE_DATA_VERSION,
        "current_scene_id": "scene.start",
        "inventory_item_ids": ["item.cup"],
        "selected_item_id": "item.cup",
        "flags": ["flag.ready"],
        "collected_pickup_ids": ["pickup.cup"],
        "completed_interaction_ids": ["interaction.well"],
        "ending_reached": False,
    }


def valid_envelope() -> SaveFileEnvelope:
    return create_save_file_envelope(
        valid_snapshot(),
        saved_at_utc=datetime(2026, 8, 6, 13, 52, tzinfo=UTC),
    )


def test_save_file_version_is_separate_from_snapshot_version() -> None:
    envelope = valid_envelope()

    assert SAVE_FORMAT_VERSION == 1
    assert SAVE_DATA_VERSION == 1
    assert envelope["save_format_version"] == SAVE_FORMAT_VERSION
    assert envelope["snapshot"]["save_version"] == SAVE_DATA_VERSION


def test_envelope_is_plain_json_compatible_data() -> None:
    envelope = valid_envelope()

    assert json.loads(json.dumps(envelope)) == envelope
    assert set(envelope) == {
        "save_format_version",
        "saved_at_utc",
        "snapshot",
    }


def test_envelope_normalizes_aware_timestamp_to_utc() -> None:
    envelope = create_save_file_envelope(
        valid_snapshot(),
        saved_at_utc=datetime(
            2026,
            8,
            6,
            15,
            52,
            7,
            123456,
            tzinfo=timezone(timedelta(hours=2)),
        ),
    )

    assert envelope["saved_at_utc"] == "2026-08-06T13:52:07.123456Z"


def test_envelope_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone information"):
        create_save_file_envelope(
            valid_snapshot(),
            saved_at_utc=datetime(2026, 8, 6, 13, 52),
        )


def test_valid_envelope_is_validated_without_mutating_input_or_building_session() -> None:
    content = SnapshotContentStub()
    envelope = valid_envelope()
    original_envelope = deepcopy(envelope)

    inspection = validate_save_file_data(data=envelope, content=content)

    assert inspection.status is SaveFileStatus.VALID
    assert inspection.is_valid
    assert inspection.envelope == envelope
    assert envelope == original_envelope


@pytest.mark.parametrize(
    "invalid_data",
    [
        None,
        [],
        {},
        {
            "save_format_version": SAVE_FORMAT_VERSION,
            "saved_at_utc": "2026-08-06T13:52:00Z",
        },
        {
            **valid_envelope(),
            "unexpected": True,
        },
        {
            **valid_envelope(),
            "save_format_version": True,
        },
        {
            **valid_envelope(),
            "saved_at_utc": "not-a-timestamp",
        },
        {
            **valid_envelope(),
            "saved_at_utc": "2026-08-06T15:52:00+02:00",
        },
        {
            **valid_envelope(),
            "snapshot": [],
        },
    ],
)
def test_invalid_envelope_shapes_return_domain_status(invalid_data: object) -> None:
    inspection = validate_save_file_data(
        data=invalid_data,
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.INVALID_ENVELOPE
    assert not inspection.is_valid
    assert inspection.envelope is None


def test_unsupported_file_version_fails_without_migration() -> None:
    envelope = valid_envelope()
    envelope["save_format_version"] = SAVE_FORMAT_VERSION + 1

    inspection = validate_save_file_data(
        data=envelope,
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.UNSUPPORTED_FILE_VERSION
    assert inspection.envelope is None


def test_invalid_snapshot_returns_domain_status() -> None:
    envelope = valid_envelope()
    envelope["snapshot"]["current_scene_id"] = "scene.missing"

    inspection = validate_save_file_data(
        data=envelope,
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.INVALID_SNAPSHOT
    assert inspection.envelope is None


def test_invalid_json_returns_domain_status() -> None:
    inspection = inspect_save_file_text(
        text="{not valid JSON",
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.INVALID_JSON
    assert inspection.envelope is None


def test_missing_file_returns_domain_status(tmp_path: Path) -> None:
    inspection = inspect_save_file(
        path=tmp_path / "save.json",
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.MISSING
    assert inspection.envelope is None


def test_unreadable_file_returns_domain_status(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    save_path = tmp_path / "save.json"
    save_path.write_text("{}", encoding="utf-8")

    def raise_permission_error(self: Path, *, encoding: str) -> str:
        del self, encoding
        raise PermissionError("technical filesystem detail")

    monkeypatch.setattr(Path, "read_text", raise_permission_error)

    inspection = inspect_save_file(
        path=save_path,
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.UNREADABLE_FILE
    assert inspection.envelope is None


def test_valid_file_returns_validated_envelope(tmp_path: Path) -> None:
    save_path = tmp_path / "save.json"
    envelope = valid_envelope()
    save_path.write_text(json.dumps(envelope), encoding="utf-8")

    inspection = inspect_save_file(
        path=save_path,
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.VALID
    assert inspection.envelope == envelope


def test_status_model_distinguishes_all_required_outcomes() -> None:
    assert {status.value for status in SaveFileStatus} == {
        "missing",
        "valid",
        "invalid_json",
        "invalid_envelope",
        "unsupported_file_version",
        "invalid_snapshot",
        "unreadable_file",
    }
