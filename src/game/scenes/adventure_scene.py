from __future__ import annotations

import pygame

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.scenes.base_scene import BaseScene


class AdventureScene(BaseScene):
    """Simple placeholder adventure scene."""

    def __init__(
        self,
        name: str,
        description: str,
        background_color: tuple[int, int, int],
        exits: list[ExitHotspot],
        hotspots: list[Hotspot],
    ) -> None:
        self.name = name
        self.description = description
        self.background_color = background_color
        self.exits = exits
        self.hotspots = hotspots

        self.interaction_text: str | None = None

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

        hotspot = self._find_hotspot(event.pos)

        if hotspot is not None:
            self.interaction_text = hotspot.inspect_text

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

        mouse_position = pygame.mouse.get_pos()
        hovered_hotspot = self._find_hotspot(mouse_position)

        for hotspot in self.hotspots:
            hotspot.draw(surface, self.body_font, is_hovered=hotspot is hovered_hotspot)

        for exit_hotspot in self.exits:
            exit_hotspot.draw(surface, self.body_font)

        if hovered_hotspot is not None:
            hover_surface = self.body_font.render(f"Inspect: {hovered_hotspot.label}", True, (255, 240, 180))
            surface.blit(hover_surface, (40, 150))

        if self.interaction_text is not None:
            interaction_surface = self.body_font.render(
                self.interaction_text,
                True,
                (245, 245, 245),
            )
            interaction_rect = interaction_surface.get_rect(
                center=(surface.get_width() // 2, surface.get_height() - 80)
            )

            background_rect = interaction_rect.inflate(40, 24)

            pygame.draw.rect(surface, (25, 22, 35), background_rect, border_radius=8)
            pygame.draw.rect(surface, (220, 215, 230), background_rect, width=2, border_radius=8)

            surface.blit(interaction_surface, interaction_rect)

    def _find_hotspot(self, position: tuple[int, int]) -> Hotspot | None:
        """Return the hotspot at a position, if one exists."""
        for hotspot in self.hotspots:
            if hotspot.contains_point(position):
                return hotspot

        return None
