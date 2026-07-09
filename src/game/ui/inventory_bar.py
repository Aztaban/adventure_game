from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

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


@dataclass(frozen=True)
class InventoryBarLayout:
    """Calculated inventory geometry for drawing and hit testing."""

    panel_rect: pygame.Rect
    item_rows: tuple[tuple[Item, pygame.Rect], ...]


class InventoryBar:
    """Render inventory items and handle item selection."""

    PANEL_WIDTH = 290
    PANEL_MARGIN = 20
    INNER_PADDING = 16

    ROW_HEIGHT = 32
    SECTION_GAP = 8
    ITEM_SECTION_GAP = 24

    MINIMUM_HEIGHT = 180

    def __init__(self, window_width: int) -> None:
        self.window_width = window_width

        self.title_font = pygame.font.Font(None, 32)
        self.item_font = pygame.font.Font(None, 26)
        self.status_font = pygame.font.Font(None, 22)

    def draw(
        self,
        surface: pygame.Surface,
        items: Sequence[Item],
        selected_item: Item | None,
    ) -> None:
        """Draw the inventory and current selection."""
        layout = self.layout_for_items(items)
        panel_rect = layout.panel_rect

        pygame.draw.rect(
            surface,
            PANEL_BACKGROUND,
            panel_rect,
            border_radius=8,
        )
        pygame.draw.rect(
            surface,
            BORDER_DEFAULT,
            panel_rect,
            width=2,
            border_radius=8,
        )

        content_x = panel_rect.x + self.INNER_PADDING
        content_y = panel_rect.y + self.INNER_PADDING

        title_surface = self.title_font.render(
            "Inventory",
            True,
            TEXT_HIGHLIGHT,
        )
        surface.blit(
            title_surface,
            (content_x, content_y),
        )

        content_y += self.title_font.get_height() + self.SECTION_GAP

        selected_name = selected_item.name if selected_item is not None else "None"

        status_surface = self.status_font.render(
            f"Selected: {selected_name}",
            True,
            TEXT_SECONDARY,
        )
        surface.blit(
            status_surface,
            (content_x, content_y),
        )

        content_y += self.status_font.get_height() + self.SECTION_GAP

        instruction = (
            "Click another item to combine"
            if selected_item is not None
            else "Click an item to select"
        )

        instruction_surface = self.status_font.render(
            instruction,
            True,
            TEXT_SECONDARY,
        )
        surface.blit(
            instruction_surface,
            (content_x, content_y),
        )

        if not items:
            empty_surface = self.item_font.render(
                "Empty",
                True,
                TEXT_SECONDARY,
            )
            surface.blit(
                empty_surface,
                (
                    content_x,
                    panel_rect.y + self._items_start_y(),
                ),
            )
            return

        for item, row_rect in layout.item_rows:
            is_selected = (
                selected_item is not None
                and selected_item.item_id == item.item_id
            )

            if is_selected:
                pygame.draw.rect(
                    surface,
                    INVENTORY_SELECTION_BACKGROUND,
                    row_rect,
                    border_radius=5,
                )
                pygame.draw.rect(
                    surface,
                    TEXT_HIGHLIGHT,
                    row_rect,
                    width=1,
                    border_radius=5,
                )

            prefix = "> " if is_selected else "• "

            item_surface = self.item_font.render(
                f"{prefix}{item.name}",
                True,
                TEXT_PRIMARY,
            )
            item_rect = item_surface.get_rect(
                midleft=(
                    row_rect.x + 6,
                    row_rect.centery,
                )
            )

            surface.blit(item_surface, item_rect)

    def item_at_position(
        self,
        position: tuple[int, int],
        items: Sequence[Item],
    ) -> Item | None:
        """Return the inventory item at a mouse position."""
        for item, row_rect in self.layout_for_items(items).item_rows:
            if row_rect.collidepoint(position):
                return item

        return None

    def layout_for_items(
        self,
        items: Sequence[Item],
    ) -> InventoryBarLayout:
        """Return inventory panel and row geometry for the supplied items."""
        content_rows = max(1, len(items))
        panel_height = max(
            self.MINIMUM_HEIGHT,
            self._items_start_y()
            + content_rows * self.ROW_HEIGHT
            + self.INNER_PADDING,
        )
        panel_rect = pygame.Rect(
            self.window_width - self.PANEL_WIDTH - self.PANEL_MARGIN,
            self.PANEL_MARGIN,
            self.PANEL_WIDTH,
            panel_height,
        )

        row_x = panel_rect.x + self.INNER_PADDING
        row_y = panel_rect.y + self._items_start_y()
        row_width = panel_rect.width - self.INNER_PADDING * 2
        item_rows: list[tuple[Item, pygame.Rect]] = []

        for item in items:
            row_rect = pygame.Rect(
                row_x,
                row_y,
                row_width,
                self.ROW_HEIGHT,
            )

            item_rows.append((item, row_rect))
            row_y += self.ROW_HEIGHT

        return InventoryBarLayout(
            panel_rect=panel_rect,
            item_rows=tuple(item_rows),
        )

    def _items_start_y(self) -> int:
        """Return the item-list offset relative to the panel."""
        return (
            self.INNER_PADDING
            + self.title_font.get_height()
            + self.SECTION_GAP
            + self.status_font.get_height()
            + self.SECTION_GAP
            + self.status_font.get_height()
            + self.ITEM_SECTION_GAP
        )
