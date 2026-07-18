from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ContentLoadError(ValueError):
    """Raised when JSON content cannot be loaded into domain objects."""


def load_json_file(path: Path | str) -> Any:
    """Load JSON data from disk with content-specific error context."""
    source_path = Path(path)

    try:
        with source_path.open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise ContentLoadError(f"{source_path}: file not found.") from error
    except json.JSONDecodeError as error:
        raise ContentLoadError(f"{source_path}: invalid JSON at line {error.lineno}, column {error.colno}.") from error


def require_string(
    entry: dict[str, Any],
    field_name: str,
    context: str,
) -> str:
    """Return a required non-empty string field from a JSON object."""
    value = entry.get(field_name)

    if not isinstance(value, str) or value == "":
        raise ContentLoadError(f"{context}: field '{field_name}' must be a non-empty string.")

    return value
