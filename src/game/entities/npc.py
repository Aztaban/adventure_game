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
from game.ui.asset_panel import draw_labeled_asset


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
    image_asset_id: str | None = None

    def dialogue_for(
        self,
        has_flag: Callable[[str], bool],
        has_completed_interaction: Callable[[str], bool],
    ) -> tuple[str, ...]:
        """Return dialogue matching persistent world state."""
        if self.dialogue_flag is not None and self.flagged_dialogue_lines and has_flag(self.dialogue_flag):
            return self.flagged_dialogue_lines

        if (
            self.item_use is not None
            and self.completed_dialogue_lines
            and self.item_use.has_been_completed(
                has_flag,
                has_completed_interaction,
            )
        ):
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
        image: pygame.Surface | None = None,
    ) -> None:
        """Draw an image-backed or fallback NPC."""
        background_color = NPC_BACKGROUND_HOVERED if is_hovered else NPC_BACKGROUND
        border_color = TEXT_HIGHLIGHT if is_hovered else TEXT_PRIMARY

        draw_labeled_asset(
            surface,
            self.rect,
            font,
            self.name,
            image,
            background_color=background_color,
            border_color=border_color,
        )
