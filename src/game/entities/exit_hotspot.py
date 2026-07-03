from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class ExitHotspot:
    """Clickable area that leads to another scene."""

    rect: pygame.Rect
    target_scene_id: str
    label: str

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return True when the position is inside the exit."""
        return self.rect.collidepoint(position)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw a visible placeholder representation of the exit."""
        pygame.draw.rect(surface, (75, 70, 90), self.rect)
        pygame.draw.rect(surface, (220, 215, 230), self.rect, width=2)

        label_surface = font.render(self.label, True, (240, 240, 240))
        label_rect = label_surface.get_rect(center=self.rect.center)

        surface.blit(label_surface, label_rect)
