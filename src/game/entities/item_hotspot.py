from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.entities.item import Item
from game.theme import (
    BORDER_DEFAULT,
    ITEM_BACKGROUND,
    ITEM_BACKGROUND_HOVERED,
    TEXT_HIGHLIGHT,
)
from game.ui.asset_panel import draw_labeled_asset


@dataclass
class ItemHotspot:
    """A collectible item placed inside a scene."""

    pickup_id: str
    rect: pygame.Rect
    item: Item
    pickup_text: str
    image_asset_id: str | None = None

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return whether a position is inside the item area."""
        return self.rect.collidepoint(position)

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        is_hovered: bool,
        image: pygame.Surface | None = None,
    ) -> None:
        """Draw an image-backed or fallback item pickup."""
        background_color = ITEM_BACKGROUND_HOVERED if is_hovered else ITEM_BACKGROUND
        border_color = TEXT_HIGHLIGHT if is_hovered else BORDER_DEFAULT

        draw_labeled_asset(
            surface,
            self.rect,
            font,
            self.item.name,
            image,
            background_color=background_color,
            border_color=border_color,
            border_radius=6,
        )
