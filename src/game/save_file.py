from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, TextIO, TypedDict, cast

from game.state_snapshot import (
    GameSnapshot,
    SnapshotValidationError,
    validate_state_snapshot,
)

if TYPE_CHECKING:
    from game.game_content import GameContent

SAVE_FORMAT_VERSION = 1
_SAVE_ENVELOPE_FIELDS = frozenset(
    {
        "save_format_version",
        "saved_at_utc",
        "snapshot",
    }
)


class SaveFileEnvelope(TypedDict):
    """Versioned JSON-compatible wrapper around one game-state snapshot."""

    save_format_version: int
    saved_at_utc: str
    snapshot: GameSnapshot


class SaveFileStatus(Enum):
    """Non-technical outcomes from inspecting one manual-save file."""

    MISSING = "missing"
    VALID = "valid"
    INVALID_JSON = "invalid_json"
    INVALID_ENVELOPE = "invalid_envelope"
    UNSUPPORTED_FILE_VERSION = "unsupported_file_version"
    INVALID_SNAPSHOT = "invalid_snapshot"
    UNREADABLE_FILE = "unreadable_file"


@dataclass(frozen=True)
class SaveFileInspection:
    """Validated save data or a domain-level reason it cannot be used."""

    status: SaveFileStatus
    envelope: SaveFileEnvelope | None = None

    @property
    def is_valid(self) -> bool:
        """Return whether a validated save envelope is available."""
        return self.status is SaveFileStatus.VALID


class SaveWriteStatus(Enum):
    """Domain-level outcomes from writing one manual-save file."""

    SAVED = "saved"
    INVALID_DATA = "invalid_data"
    DIRECTORY_CREATION_FAILED = "directory_creation_failed"
    TEMPORARY_FILE_FAILED = "temporary_file_failed"
    WRITE_FAILED = "write_failed"
    FLUSH_FAILED = "flush_failed"
    SYNC_FAILED = "sync_failed"
    REPLACE_FAILED = "replace_failed"


@dataclass(frozen=True)
class SaveWriteResult:
    """Non-technical result from one atomic manual-save attempt."""

    status: SaveWriteStatus

    @property
    def is_success(self) -> bool:
        """Return whether the final save was replaced successfully."""
        return self.status is SaveWriteStatus.SAVED


def create_save_file_envelope(
    snapshot: GameSnapshot,
    *,
    saved_at_utc: datetime | None = None,
) -> SaveFileEnvelope:
    """Wrap a snapshot in save-file format version 1 using a UTC timestamp."""
    timestamp = saved_at_utc or datetime.now(UTC)

    if timestamp.tzinfo is None:
        raise ValueError("Save timestamps must include timezone information.")

    normalized_timestamp = timestamp.astimezone(UTC)

    return {
        "save_format_version": SAVE_FORMAT_VERSION,
        "saved_at_utc": normalized_timestamp.isoformat().replace("+00:00", "Z"),
        "snapshot": cast(GameSnapshot, dict(snapshot)),
    }


def write_save_file(
    *,
    path: Path,
    envelope: SaveFileEnvelope,
) -> SaveWriteResult:
    """Write one save envelope atomically without risking the previous file."""
    try:
        serialized_envelope = json.dumps(
            envelope,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"
    except (OverflowError, RecursionError, TypeError, ValueError):
        return SaveWriteResult(SaveWriteStatus.INVALID_DATA)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return SaveWriteResult(SaveWriteStatus.DIRECTORY_CREATION_FAILED)

    temporary_file: TextIO | None = None
    temporary_path: Path | None = None

    try:
        try:
            temporary_file = tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                prefix=f".{path.name}.",
                suffix=".tmp",
                dir=path.parent,
                delete=False,
            )
            temporary_path = Path(temporary_file.name)
        except OSError:
            return SaveWriteResult(SaveWriteStatus.TEMPORARY_FILE_FAILED)

        try:
            written_characters = temporary_file.write(serialized_envelope)
        except (OSError, UnicodeError, ValueError):
            return SaveWriteResult(SaveWriteStatus.WRITE_FAILED)

        if written_characters != len(serialized_envelope):
            return SaveWriteResult(SaveWriteStatus.WRITE_FAILED)

        try:
            temporary_file.flush()
        except (OSError, UnicodeError, ValueError):
            return SaveWriteResult(SaveWriteStatus.FLUSH_FAILED)

        try:
            _sync_file(temporary_file)
        except (OSError, ValueError):
            return SaveWriteResult(SaveWriteStatus.SYNC_FAILED)

        try:
            temporary_file.close()
        except (OSError, UnicodeError, ValueError):
            return SaveWriteResult(SaveWriteStatus.WRITE_FAILED)

        temporary_file = None

        try:
            os.replace(temporary_path, path)
        except OSError:
            return SaveWriteResult(SaveWriteStatus.REPLACE_FAILED)

        temporary_path = None
        return SaveWriteResult(SaveWriteStatus.SAVED)
    finally:
        if temporary_file is not None:
            try:
                temporary_file.close()
            except (OSError, UnicodeError, ValueError):
                pass

        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


def inspect_save_file(
    *,
    path: Path,
    content: GameContent,
) -> SaveFileInspection:
    """Read and validate a save file without constructing or mutating a session."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return SaveFileInspection(SaveFileStatus.MISSING)
    except (OSError, UnicodeError):
        return SaveFileInspection(SaveFileStatus.UNREADABLE_FILE)

    return inspect_save_file_text(text=text, content=content)


def inspect_save_file_text(
    *,
    text: str,
    content: GameContent,
) -> SaveFileInspection:
    """Parse and validate save-file JSON without exposing JSON exceptions."""
    try:
        data = json.loads(text)
    except JSONDecodeError:
        return SaveFileInspection(SaveFileStatus.INVALID_JSON)

    return validate_save_file_data(data=data, content=content)


def validate_save_file_data(
    *,
    data: object,
    content: GameContent,
) -> SaveFileInspection:
    """Validate an already-decoded save envelope and its snapshot payload."""
    if not isinstance(data, Mapping):
        return SaveFileInspection(SaveFileStatus.INVALID_ENVELOPE)

    if frozenset(data) != _SAVE_ENVELOPE_FIELDS:
        return SaveFileInspection(SaveFileStatus.INVALID_ENVELOPE)

    save_format_version = data.get("save_format_version")

    if not isinstance(save_format_version, int) or isinstance(save_format_version, bool):
        return SaveFileInspection(SaveFileStatus.INVALID_ENVELOPE)

    if save_format_version != SAVE_FORMAT_VERSION:
        return SaveFileInspection(SaveFileStatus.UNSUPPORTED_FILE_VERSION)

    saved_at_utc = data.get("saved_at_utc")

    if not isinstance(saved_at_utc, str) or not _is_utc_timestamp(saved_at_utc):
        return SaveFileInspection(SaveFileStatus.INVALID_ENVELOPE)

    snapshot = data.get("snapshot")

    if not isinstance(snapshot, Mapping):
        return SaveFileInspection(SaveFileStatus.INVALID_ENVELOPE)

    try:
        validated_snapshot = validate_state_snapshot(
            content=content,
            snapshot=snapshot,
        )
    except SnapshotValidationError:
        return SaveFileInspection(SaveFileStatus.INVALID_SNAPSHOT)

    envelope = SaveFileEnvelope(
        save_format_version=SAVE_FORMAT_VERSION,
        saved_at_utc=saved_at_utc,
        snapshot=validated_snapshot,
    )
    return SaveFileInspection(
        status=SaveFileStatus.VALID,
        envelope=envelope,
    )


def _is_utc_timestamp(value: str) -> bool:
    """Return whether a string is an ISO-8601 timestamp with a UTC offset."""
    normalized_value = value[:-1] + "+00:00" if value.endswith("Z") else value

    try:
        timestamp = datetime.fromisoformat(normalized_value)
    except ValueError:
        return False

    return timestamp.tzinfo is not None and timestamp.utcoffset() == timedelta(0)


def _sync_file(file: TextIO) -> None:
    """Sync a flushed temporary file when the current platform supports it."""
    sync = getattr(os, "fsync", None)

    if sync is not None:
        sync(file.fileno())
