from __future__ import annotations

import pygame
from game.entities.exit_hotspot import ExitHotspot
from game.scenes.base_scene import BaseScene


class AdventureScene(BaseScene):
    """Simple placeholder adventure scene."""

    def __init__(
        self,
        name: str,
        description: str,
        background_color: tuple[int, int, int],
        exits: list[ExitHotspot],
    ) -> None:
        self.name = name
        self.description = description
        self.background_color = background_color
        self.exits = exits

        self.title_font = pygame.font.Font(None, 52)
        self.body_font = pygame.font.Font(None, 30)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Return the destination scene when an exit is clicked."""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        for exit_hotspot in self.exits:
            if exit_hotspot.contains_point(event.pos):
                return exit_hotspot.target_scene_id

        return None

    def update(self, delta_time: float) -> None:
        """Update the scene.

        The placeholder scenes currently have no animated state.
        """
        del delta_time

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene and its exits."""
        surface.fill(self.background_color)

        title_surface = self.title_font.render(self.name, True, (245, 245, 245))
        description_surface = self.body_font.render(self.description, True, (225, 225, 225))

        surface.blit(title_surface, (40, 40))
        surface.blit(description_surface, (40, 100))

        for exit_hotspot in self.exits:
            exit_hotspot.draw(surface, self.body_font)
