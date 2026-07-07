from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.theme import BORDER_DEFAULT, EXIT_BACKGROUND, EXIT_LOCKED_BACKGROUND, TEXT_PRIMARY


@dataclass
class ExitHotspot:
    """Clickable area that leads to another scene."""

    rect: pygame.Rect
    target_scene_id: str
    label: str
    required_flag: str | None = None
    locked_text: str = "The way is blocked."
    locked_label: str | None = None
    completion_flag: str | None = None

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return True when the position is inside the exit."""
        return self.rect.collidepoint(position)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, is_locked: bool = False) -> None:
        """Draw a visible placeholder exit."""
        background_color = EXIT_LOCKED_BACKGROUND if is_locked else EXIT_BACKGROUND

        displayed_label = self.label

        if is_locked and self.locked_label is not None:
            displayed_label = self.locked_label

        pygame.draw.rect(surface, background_color, self.rect)
        pygame.draw.rect(surface, BORDER_DEFAULT, self.rect, width=2)

        label_surface = font.render(displayed_label, True, TEXT_PRIMARY)
        label_rect = label_surface.get_rect(center=self.rect.center)

        surface.blit(label_surface, label_rect)
