from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.entities.item import Item
from game.theme import (
    BORDER_DEFAULT,
    ITEM_BACKGROUND,
    ITEM_BACKGROUND_HOVERED,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
)


@dataclass
class ItemHotspot:
    """A collectible item placed inside a scene."""

    rect: pygame.Rect
    item: Item
    pickup_text: str

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return whether a position is inside the item area."""
        return self.rect.collidepoint(position)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, is_hovered: bool) -> None:
        """Draw a placeholder representation of the item."""
        background_color = ITEM_BACKGROUND_HOVERED if is_hovered else ITEM_BACKGROUND
        border_color = TEXT_HIGHLIGHT if is_hovered else BORDER_DEFAULT

        pygame.draw.rect(surface, background_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=6)

        label_surface = font.render(self.item.name, True, TEXT_PRIMARY)

        label_rect = label_surface.get_rect(center=self.rect.center)

        surface.blit(label_surface, label_rect)
