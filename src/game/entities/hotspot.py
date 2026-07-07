from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

from game.systems.item_use import ItemUseInteraction
from game.theme import (
    BORDER_DEFAULT,
    HOTSPOT_BACKGROUND,
    HOTSPOT_BACKGROUND_HOVERED,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
)


@dataclass
class Hotspot:
    """Clickable scene object that can be inspected or used."""

    rect: pygame.Rect
    label: str
    inspect_text: str
    item_use: ItemUseInteraction | None = None
    completed_inspect_text: str | None = None
    inspect_flag: str | None = None
    flagged_inspect_text: str | None = None

    @property
    def current_inspect_text(self) -> str:
        """Return inspection text matching item-use state."""
        if self.item_use is not None and self.item_use.is_completed and self.completed_inspect_text is not None:
            return self.completed_inspect_text

        return self.inspect_text

    def inspect_text_for(self, has_flag: Callable[[str], bool]) -> str:
        """Return inspection text matching the current game flags."""
        if self.inspect_flag is not None and self.flagged_inspect_text is not None and has_flag(self.inspect_flag):
            return self.flagged_inspect_text

        return self.flagged_inspect_text

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

        label_surface = font.render(self.label, True, TEXT_PRIMARY)
        label_rect = label_surface.get_rect(center=self.rect.center)

        surface.blit(label_surface, label_rect)
