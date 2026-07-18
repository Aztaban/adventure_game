from __future__ import annotations

import pygame

from game.theme import (
    BORDER_DEFAULT,
    PANEL_BACKGROUND,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from game.ui.text import wrap_text


class InteractionPrompt:
    """Render a compact hover action with an explicit input hint."""

    HORIZONTAL_PADDING = 18
    VERTICAL_PADDING = 12
    LINE_SPACING = 4
    MAXIMUM_WIDTH = 720

    def __init__(
            self,
            action_font: pygame.font.Font,
            hint_font: pygame.font.Font,
    ) -> None:
        self.action_font = action_font
        self.hint_font = hint_font

    def draw(
        self,
        surface: pygame.Surface,
        action_text: str,
        hint_text: str,
        *,
        top_left: tuple[int, int] = (40, 145),
        maximum_width: int | None = None,
    ) -> None:
        """Draw the prompt within the available scene area."""
        available_width = maximum_width or self.MAXIMUM_WIDTH
        text_width = max(180, available_width - self.HORIZONTAL_PADDING * 2)
        action_lines = wrap_text(self.action_font, action_text, text_width)

        action_height = len(action_lines) * self.action_font.get_linesize()
        action_height += max(0, len(action_lines) - 1) * self.LINE_SPACING
        panel_height = self.VERTICAL_PADDING + action_height + 8 + self.hint_font.get_linesize() + self.VERTICAL_PADDING
        panel_width = min(self.MAXIMUM_WIDTH, available_width)
        panel_rect = pygame.Rect(top_left, (panel_width, panel_height))

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

        action_y = panel_rect.y + self.VERTICAL_PADDING

        for index, line in enumerate(action_lines):
            color = TEXT_HIGHLIGHT if index == 0 else TEXT_PRIMARY
            line_surface = self.action_font.render(line, True, color)
            surface.blit(
                line_surface,
                (panel_rect.x + self.HORIZONTAL_PADDING, action_y),
            )
            action_y += self.action_font.get_linesize() + self.LINE_SPACING

        hint_surface = self.hint_font.render(hint_text, True, TEXT_SECONDARY)
        surface.blit(
            hint_surface,
            (
                panel_rect.x + self.HORIZONTAL_PADDING,
                panel_rect.bottom - self.VERTICAL_PADDING - hint_surface.get_height(),
            ),
        )
