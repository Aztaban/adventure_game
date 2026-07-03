from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class BaseScene(ABC):
    """Interface shared by all game scenes."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle an event and optinally request a scene change."""

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update scene state."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene."""
