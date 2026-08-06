from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict, cast

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
