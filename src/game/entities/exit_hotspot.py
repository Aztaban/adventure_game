from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.systems.item_use import ItemUseInteraction
from game.theme import (
    BORDER_DEFAULT,
    EXIT_BACKGROUND,
    EXIT_LOCKED_BACKGROUND,
    EXIT_LOCKED_OVERLAY,
    TEXT_HIGHLIGHT,
)
from game.ui.asset_panel import draw_labeled_asset


@dataclass
class ExitHotspot:
    """Clickable area that leads to another scene."""

    rect: pygame.Rect
    target_scene_id: str
    label: str
    required_flag: str | None = None
    locked_text: str = "The way is blocked."
    locked_label: str | None = None
    completion_flag: str | None = None
    item_use: ItemUseInteraction | None = None
    ends_game: bool = False
    image_asset_id: str | None = None
    unlock_sound_id: str | None = None

    def contains_point(self, position: tuple[int, int]) -> bool:
        """Return True when the position is inside the exit."""
        return self.rect.collidepoint(position)

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        is_locked: bool = False,
        is_hovered: bool = False,
        image: pygame.Surface | None = None,
    ) -> None:
        """Draw an image-backed or fallback exit."""
        background_color = EXIT_LOCKED_BACKGROUND if is_locked else EXIT_BACKGROUND
        border_color = TEXT_HIGHLIGHT if is_hovered else BORDER_DEFAULT
        displayed_label = self.label

        if is_locked and self.locked_label is not None:
            displayed_label = self.locked_label

        draw_labeled_asset(
            surface,
            self.rect,
            font,
            displayed_label,
            image,
            background_color=background_color,
            border_color=border_color,
            overlay_color=EXIT_LOCKED_OVERLAY if is_locked and image is not None else None,
        )
