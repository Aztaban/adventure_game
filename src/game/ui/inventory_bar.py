from __future__ import annotations

from collections.abc import Sequence

import pygame

from game.entities.item import Item
from game.theme import (
    BORDER_DEFAULT,
    PANEL_BACKGROUND,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class InventoryBar:
    """Render the player's inventory in the top-right corner."""

    PANEL_WIDTH = 250
    PANEL_MARGIN = 20
    INNER_PADDING = 18
    ROW_HEIGHT = 28
    MINIMUM_HEIGHT = 110

    def __init__(self) -> None:
        self.title_font = pygame.font.Font(None, 32)
        self.item_font = pygame.font.Font(None, 26)

    def draw(self, surface: pygame.Surface, items: Sequence[Item]) -> None:
        """Draw the inventory panel and collected item names."""
        content_rows = max(1, len(items))

        panel_height = max(
            self.MINIMUM_HEIGHT,
            self.INNER_PADDING * 2 + self.title_font.get_linesize() + 10 + content_rows * self.ROW_HEIGHT,
        )

        panel_rect = pygame.Rect(
            surface.get_width() - self.PANEL_WIDTH - self.PANEL_MARGIN,
            self.PANEL_MARGIN,
            self.PANEL_WIDTH,
            panel_height,
        )

        pygame.draw.rect(surface, PANEL_BACKGROUND, panel_rect, border_radius=8)
        pygame.draw.rect(surface, BORDER_DEFAULT, panel_rect, width=2, border_radius=8)

        title_surface = self.title_font.render("Inventory", True, TEXT_HIGHLIGHT)
        surface.blit(
            title_surface,
            (
                panel_rect.x + self.INNER_PADDING,
                panel_rect.y + self.INNER_PADDING,
            ),
        )

        item_x = panel_rect.x + self.INNER_PADDING
        item_y = panel_rect.y + self.INNER_PADDING + self.title_font.get_linesize() + 10

        if not items:
            empty_surface = self.item_font.render("Empty", True, TEXT_SECONDARY)
            surface.blit(empty_surface, (item_x, item_y))
            return

        for item in items:
            item_surface = self.item_font.render(
                f"• {item.name}",
                True,
                TEXT_PRIMARY,
            )
            surface.blit(item_surface, (item_x, item_y))
            item_y += self.ROW_HEIGHT
