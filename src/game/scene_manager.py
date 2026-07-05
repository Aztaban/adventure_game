from __future__ import annotations

import pygame

from game.scenes.base_scene import BaseScene


class SceneManager:
    """Own and switch between game scenes."""

    def __init__(
        self,
        scenes: dict[str, BaseScene],
        starting_scene_id: str,
    ) -> None:
        if not scenes:
            raise ValueError("Scene manager requires at least one scene.")

        if starting_scene_id not in scenes:
            raise ValueError(f"Starting scene does not exist: {starting_scene_id}")

        self._scenes = scenes
        self._current_scene_id = starting_scene_id

    @property
    def current_scene_id(self) -> str:
        """Return the ID of the active scene."""
        return self._current_scene_id

    @property
    def current_scene(self) -> BaseScene:
        """Return the active scene."""
        return self._scenes[self._current_scene_id]

    def change_scene(self, scene_id: str) -> None:
        """Switch to another registered scene."""
        if scene_id not in self._scenes:
            raise ValueError(f"Scene does not exist: {scene_id}")

        self._current_scene_id = scene_id

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Pass an event to the active scene and return whether it was consumed."""
        result = self.current_scene.handle_event(event)

        if result.target_scene_id is not None:
            self.change_scene(result.target_scene_id)

        return result.consumed or result.target_scene_id is not None

    def update(self, delta_time: float) -> None:
        """Update the active scene."""
        self.current_scene.update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the active scene."""
        self.current_scene.draw(surface)
