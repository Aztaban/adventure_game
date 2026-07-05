from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.theme import (
    BORDER_DEFAULT,
    HOTSPOT_BACKGROUND,
    HOTSPOT_BACKGROUND_HOVERED,
    TEXT_HIGHLIGHT,
)


@dataclass
class Hotspot:
    """Clickable scene object that can be inspected."""

    rect: pygame.Rect
    label: str
    inspect_text: str

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return True when a point is inside the hotspot."""
        return self.rect.collidepoint(position)

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        is_hovered: bool,
    ) -> None:
        """Draw a visible placeholder for the hotspot."""
        fill_color = HOTSPOT_BACKGROUND_HOVERED if is_hovered else HOTSPOT_BACKGROUND
        border_color = TEXT_HIGHLIGHT if is_hovered else BORDER_DEFAULT

        pygame.draw.rect(surface, fill_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, width=2)

        label_surface = font.render(self.label, True, (245, 245, 245))
        label_rect = label_surface.get_rect(center=self.rect.center)

        surface.blit(label_surface, label_rect)
