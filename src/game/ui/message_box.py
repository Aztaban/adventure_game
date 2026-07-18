from __future__ import annotations

import pygame

from game.theme import BORDER_DEFAULT, PANEL_BACKGROUND, TEXT_PRIMARY
from game.ui.text import wrap_text


class MessageBox:
    """Draw short interaction messages near the bottom of the screen."""

    MAXIMUM_WIDTH = 820
    HORIZONTAL_MARGIN = 30
    BOTTOM_MARGIN = 34
    HORIZONTAL_PADDING = 24
    VERTICAL_PADDING = 16
    LINE_SPACING = 6

    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def draw(
        self,
        surface: pygame.Surface,
        text: str,
        *,
        available_rect: pygame.rect | None,
    ) -> None:
        """Draw a wrapped interaction message inside an optional content area."""
        content_rect = available_rect or surface.get_rect()
        available_width = content_rect.width - self.HORIZONTAL_MARGIN * 2 - self.HORIZONTAL_PADDING * 2
        maximum_text_width = min(
            self.MAXIMUM_WIDTH - self.HORIZONTAL_PADDING * 2,
            available_width,
        )

        lines = wrap_text(self.font, text, maximum_text_width)
        line_height = self.font.get_linesize()

        text_width = max(self.font.size(line)[0] for line in lines)
        text_height = len(lines) * line_height + max(0, len(lines) - 1) * self.LINE_SPACING

        panel_width = text_width + self.HORIZONTAL_PADDING * 2
        panel_height = text_height + self.VERTICAL_PADDING * 2

        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.midbottom = (
            content_rect.centerx,
            content_rect.bottom - self.BOTTOM_MARGIN,
        )

        pygame.draw.rect(surface, PANEL_BACKGROUND, panel_rect, border_radius=10)
        pygame.draw.rect(surface, BORDER_DEFAULT, panel_rect, width=2, border_radius=10)

        text_y = panel_rect.y + self.VERTICAL_PADDING

        for line in lines:
            line_surface = self.font.render(line, True, TEXT_PRIMARY)
            line_rect = line_surface.get_rect(centerx=panel_rect.centerx, y=text_y)
            surface.blit(line_surface, line_rect)
            text_y += line_height + self.LINE_SPACING
