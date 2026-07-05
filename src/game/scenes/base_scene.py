from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

from game.scene_event_result import SceneEventResult


class BaseScene(ABC):
    """Interface shared by all game scenes."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> SceneEventResult:
        """Handle an event and report whether it was consumed."""

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update scene state."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene."""
