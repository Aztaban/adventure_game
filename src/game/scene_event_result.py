from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SceneEventResult:
    """Describe how a scene handled an input event."""

    consumed: bool = False
    target_scene_id: str | None = None
