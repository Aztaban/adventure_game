from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

from game.systems.item_use import ItemUseInteraction
from game.theme import (
    NPC_BACKGROUND,
    NPC_BACKGROUND_HOVERED,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
)


@dataclass
class NPC:
    """Clickable NPC with dialogue and item interactions."""

    rect: pygame.Rect
    name: str
    dialogue_lines: tuple[str, ...]
    item_use: ItemUseInteraction | None = None
    completed_dialogue_lines: tuple[str, ...] = ()
    dialogue_flag: str | None = None
    flagged_dialogue_lines: tuple[str, ...] = ()

    def dialogue_for(self, has_flag: Callable[[str], bool]) -> tuple[str, ...]:
        """Return dialogue matching current progression flags."""
        if self.dialogue_flag is not None and self.flagged_dialogue_lines and has_flag(self.dialogue_flag):
            return self.flagged_dialogue_lines

        if self.item_use is not None and self.item_use.is_completed and self.completed_dialogue_lines:
            return self.completed_dialogue_lines

        return self.dialogue_lines

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return whether a position is inside the NPC area."""
        return self.rect.collidepoint(position)

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        is_hovered: bool,
    ) -> None:
        """Draw a placeholder NPC."""
        background_color = NPC_BACKGROUND_HOVERED if is_hovered else NPC_BACKGROUND
        border_color = TEXT_HIGHLIGHT if is_hovered else TEXT_PRIMARY

        pygame.draw.rect(surface, background_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, width=2)

        label_surface = font.render(self.name, True, TEXT_PRIMARY)
        label_rect = label_surface.get_rect(center=self.rect.center)

        surface.blit(label_surface, label_rect)
