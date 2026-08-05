from dataclasses import dataclass
from pathlib import Path

import platformdirs

APPLICATION_NAME = "Mysterious Forest"
MANUAL_SAVE_FILENAME = "save.json"

@dataclass(frozen=True)
class SavePaths:
    """Resolved filesystem locations for the manual save slot."""

    user_data_dir: Path
    manual_save_path: Path


def resolve_save_paths(*, user_data_dir: Path | None = None) -> SavePaths:
    """Resolve save locations without creating directories or files."""
    resolved_user_data_dir = user_data_dir

    if resolved_user_data_dir is None:
        resolved_user_data_dir = platformdirs.user_data_path(
            appname=APPLICATION_NAME,
            appauthor=False,
            ensure_exists=False,
        )

    return SavePaths(
        user_data_dir=resolved_user_data_dir,
        manual_save_path=resolved_user_data_dir / MANUAL_SAVE_FILENAME,
    )
