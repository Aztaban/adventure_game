import json
import os
import tempfile
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import TextIO

import pytest

import game.save_file as save_file_module
from game.save_file import (
    SAVE_FORMAT_VERSION,
    SaveFileEnvelope,
    SaveFileStatus,
    SaveWriteStatus,
    create_save_file_envelope,
    inspect_save_file,
    inspect_save_file_text,
    validate_save_file_data,
    write_save_file,
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


class TemporaryFileProxy:
    """Small test double that can fail one temporary-file operation."""

    def __init__(self, path: Path, *, fail_operation: str) -> None:
        self.name = str(path)
        self._file = path.open("w", encoding="utf-8", newline="\n")
        self._fail_operation = fail_operation

    def write(self, text: str) -> int:
        if self._fail_operation == "write":
            raise PermissionError("technical write detail")

        return self._file.write(text)

    def flush(self) -> None:
        if self._fail_operation == "flush":
            raise OSError("technical flush detail")

        self._file.flush()

    def fileno(self) -> int:
        return self._file.fileno()

    def close(self) -> None:
        self._file.close()


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


def test_atomic_write_creates_directory_and_serializes_utf8_json(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    save_path = tmp_path / "new-user-data" / "save.json"
    envelope = valid_envelope()
    envelope["snapshot"]["flags"] = ["flag.příliš"]
    replacement_arguments: list[tuple[Path, Path]] = []
    real_replace = os.replace

    def record_replace(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        replacement_arguments.append((source_path, destination_path))

        assert source_path.parent == save_path.parent
        assert destination_path == save_path
        assert source_path.exists()

        real_replace(source_path, destination_path)

    monkeypatch.setattr(save_file_module.os, "replace", record_replace)

    assert not save_path.parent.exists()

    result = write_save_file(path=save_path, envelope=envelope)

    assert result.status is SaveWriteStatus.SAVED
    assert result.is_success
    assert save_path.parent.is_dir()
    assert replacement_arguments
    assert b"flag.p\xc5\x99\xc3\xadli\xc5\xa1" in save_path.read_bytes()
    assert json.loads(save_path.read_text(encoding="utf-8")) == envelope
    assert not list(save_path.parent.glob(".save.json.*.tmp"))


def test_atomic_write_replaces_existing_save(tmp_path: Path) -> None:
    save_path = tmp_path / "save.json"
    previous_envelope = valid_envelope()
    replacement_envelope = create_save_file_envelope(
        valid_snapshot(),
        saved_at_utc=datetime(2026, 8, 6, 14, 52, tzinfo=UTC),
    )
    replacement_envelope["snapshot"]["ending_reached"] = True
    save_path.write_text(json.dumps(previous_envelope), encoding="utf-8")

    result = write_save_file(
        path=save_path,
        envelope=replacement_envelope,
    )

    assert result.status is SaveWriteStatus.SAVED
    assert json.loads(save_path.read_text(encoding="utf-8")) == replacement_envelope
    assert not list(tmp_path.glob(".save.json.*.tmp"))


def test_malformed_file_read_returns_invalid_json(tmp_path: Path) -> None:
    save_path = tmp_path / "save.json"
    save_path.write_text("{malformed", encoding="utf-8")

    inspection = inspect_save_file(
        path=save_path,
        content=SnapshotContentStub(),
    )

    assert inspection.status is SaveFileStatus.INVALID_JSON
    assert inspection.envelope is None


def test_directory_creation_failure_returns_domain_status(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    save_path = tmp_path / "unavailable" / "save.json"

    def fail_directory_creation(
        self: Path,
        mode: int = 0o777,
        parents: bool = False,
        exist_ok: bool = False,
    ) -> None:
        del self, mode, parents, exist_ok
        raise PermissionError("technical directory detail")

    monkeypatch.setattr(Path, "mkdir", fail_directory_creation)

    result = write_save_file(path=save_path, envelope=valid_envelope())

    assert result.status is SaveWriteStatus.DIRECTORY_CREATION_FAILED
    assert not result.is_success


def test_temporary_file_creation_failure_returns_domain_status(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fail_temporary_file(**_kwargs: object) -> TextIO:
        raise PermissionError("technical temporary-file detail")

    monkeypatch.setattr(save_file_module.tempfile, "NamedTemporaryFile", fail_temporary_file)

    result = write_save_file(
        path=tmp_path / "save.json",
        envelope=valid_envelope(),
    )

    assert result.status is SaveWriteStatus.TEMPORARY_FILE_FAILED
    assert not result.is_success


@pytest.mark.parametrize(
    ("fail_operation", "expected_status"),
    [
        ("write", SaveWriteStatus.WRITE_FAILED),
        ("flush", SaveWriteStatus.FLUSH_FAILED),
        ("sync", SaveWriteStatus.SYNC_FAILED),
        ("replace", SaveWriteStatus.REPLACE_FAILED),
    ],
)
def test_atomic_write_failure_preserves_previous_save_and_cleans_temporary_file(
    fail_operation: str,
    expected_status: SaveWriteStatus,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    save_path = tmp_path / "save.json"
    previous_envelope = valid_envelope()
    previous_text = json.dumps(previous_envelope)
    save_path.write_text(previous_text, encoding="utf-8")
    previous_bytes = save_path.read_bytes()
    replace_called = False

    if fail_operation in {"write", "flush"}:

        def create_failing_temporary_file(**kwargs: object) -> TemporaryFileProxy:
            temporary_directory = Path(kwargs["dir"])
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=str(kwargs["prefix"]),
                suffix=str(kwargs["suffix"]),
                dir=temporary_directory,
            )
            os.close(descriptor)
            return TemporaryFileProxy(
                Path(temporary_name),
                fail_operation=fail_operation,
            )

        monkeypatch.setattr(
            save_file_module.tempfile,
            "NamedTemporaryFile",
            create_failing_temporary_file,
        )

    if fail_operation == "sync":

        def fail_sync(_descriptor: int) -> None:
            raise OSError("technical sync detail")

        monkeypatch.setattr(save_file_module.os, "fsync", fail_sync)

    real_replace = os.replace

    def replace_or_fail(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
        nonlocal replace_called
        replace_called = True

        if fail_operation == "replace":
            raise OSError("technical replace detail")

        real_replace(source, destination)

    monkeypatch.setattr(save_file_module.os, "replace", replace_or_fail)

    replacement_envelope = create_save_file_envelope(
        valid_snapshot(),
        saved_at_utc=datetime(2026, 8, 6, 14, 52, tzinfo=UTC),
    )
    result = write_save_file(
        path=save_path,
        envelope=replacement_envelope,
    )

    assert result.status is expected_status
    assert not result.is_success
    assert save_path.read_bytes() == previous_bytes
    assert inspect_save_file(
        path=save_path,
        content=SnapshotContentStub(),
    ).status is SaveFileStatus.VALID
    assert replace_called is (fail_operation == "replace")
    assert not list(tmp_path.glob(".save.json.*.tmp"))


def test_invalid_save_data_does_not_create_directory(tmp_path: Path) -> None:
    save_path = tmp_path / "new-user-data" / "save.json"
    envelope = valid_envelope()
    envelope["snapshot"] = {"not_json": object()}  # type: ignore[typeddict-item]

    result = write_save_file(path=save_path, envelope=envelope)

    assert result.status is SaveWriteStatus.INVALID_DATA
    assert not save_path.parent.exists()


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


def test_write_status_model_contains_no_raw_exception_data() -> None:
    assert {status.value for status in SaveWriteStatus} == {
        "saved",
        "invalid_data",
        "directory_creation_failed",
        "temporary_file_failed",
        "write_failed",
        "flush_failed",
        "sync_failed",
        "replace_failed",
    }
