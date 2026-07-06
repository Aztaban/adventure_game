from __future__ import annotations

from collections.abc import Sequence

import pygame

from game.entities.item import Item
from game.theme import (
    BORDER_DEFAULT,
    INVENTORY_SELECTION_BACKGROUND,
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
    ITEM_START_OFFSET = 82
    MINIMUM_HEIGHT = 110

    def __init__(self, window_width: int) -> None:
        self.window_width = window_width

        self.title_font = pygame.font.Font(None, 32)
        self.item_font = pygame.font.Font(None, 26)
        self.status_font = pygame.font.Font(None, 22)

    def draw(self, surface: pygame.Surface, items: Sequence[Item], selected_item: Item | None) -> None:
        """Draw the inventory and its current selection."""
        panel_rect = self._create_panel_rect(len(items))

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

        selected_name = selected_item.name if selected_item is not None else "None"
        status_surface = self.status_font.render(f"Selected: {selected_name}", True, TEXT_SECONDARY)
        surface.blit(
            status_surface,
            (
                panel_rect.x + self.INNER_PADDING,
                panel_rect.y + 48,
            ),
        )

        item_x = panel_rect.x + self.INNER_PADDING
        item_y = panel_rect.y + self.ITEM_START_OFFSET

        if not items:
            empty_surface = self.item_font.render("Empty", True, TEXT_SECONDARY)
            surface.blit(empty_surface, (item_x, item_y))
            return

        for item, row_rect in self._create_item_rows(items):
            is_selected = selected_item is not None and selected_item.item_id == item.item_id

            if is_selected:
                pygame.draw.rect(surface, INVENTORY_SELECTION_BACKGROUND, row_rect, border_radius=5)
                pygame.draw.rect(surface, TEXT_HIGHLIGHT, row_rect, width=1, border_radius=5)

            prefix = "> " if is_selected else "• "

            item_surface = self.item_font.render(f"{prefix}{item.name}", True, TEXT_PRIMARY)
            surface.blit(item_surface, (row_rect.x + 6, row_rect.y + 3))

    def item_at_position(self, position: tuple[int, int], items: Sequence[Item]) -> Item | None:
        """Return the inventory item at a mouse position."""
        for item, row_rect in self._create_item_rows(items):
            if row_rect.collidepoint(position):
                return item

        return None

    def _create_panel_rect(self, item_count: int) -> pygame.Rect:
        """Create the inventroy panel rectangle."""
        content_rows = max(1, item_count)

        panel_height = max(
            self.MINIMUM_HEIGHT,
            self.ITEM_START_OFFSET + content_rows * self.ROW_HEIGHT + self.INNER_PADDING,
        )

        return pygame.Rect(
            self.window_width - self.PANEL_WIDTH - self.PANEL_MARGIN,
            self.PANEL_MARGIN,
            self.PANEL_WIDTH,
            panel_height,
        )

    def _create_item_rows(self, items: Sequence[Item]) -> list[tuple[Item, pygame.Rect]]:
        """Create clickable rectangles for inventory items."""
        panel_rect = self._create_panel_rect(len(items))
        rows: list[tuple[Item, pygame.Rect]] = []

        row_x = panel_rect.x + self.INNER_PADDING
        row_width = panel_rect.width - self.INNER_PADDING * 2
        row_y = panel_rect.y = self.ITEM_START_OFFSET

        for item in items:
            row_rect = pygame.Rect(row_x, row_y, row_width, self.ROW_HEIGHT)
            rows.append((item, row_rect))
            row_y += self.ROW_HEIGHT

        return rows
