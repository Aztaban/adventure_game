from __future__ import annotations

import pygame

from game.theme import BORDER_DEFAULT, PANEL_BACKGROUND, TEXT_PRIMARY


class MessageBox:
    """Draw short interaction messages near the bottom of the screen."""

    MAXIMUM_WIDTH = 900
    HORIZONTAL_MARGIN = 30
    BOTTOM_MARGIN = 48
    HORIZONTAL_PADDING = 24
    VERTICAL_PADDING = 14
    LINE_SPACING = 5

    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 30)

    def draw(self, surface: pygame.Surface, text: str) -> None:
        """Draw a wrapped interaction message."""
        available_width = surface.get_width() - self.HORIZONTAL_MARGIN * 2 - self.HORIZONTAL_PADDING * 2
        maximum_text_width = min(
            self.MAXIMUM_WIDTH - self.HORIZONTAL_PADDING * 2,
            available_width,
        )

        lines = self._wrap_text(text, maximum_text_width)
        line_height = self.font.get_linesize()

        text_width = max(self.font.size(line)[0] for line in lines)
        text_height = len(lines) * line_height + max(0, len(lines) - 1) * self.LINE_SPACING

        panel_width = text_width + self.HORIZONTAL_PADDING * 2
        panel_height = text_height + self.VERTICAL_PADDING * 2

        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.midbottom = (
            surface.get_width() // 2,
            surface.get_height() - self.BOTTOM_MARGIN,
        )

        pygame.draw.rect(surface, PANEL_BACKGROUND, panel_rect, border_radius=8)
        pygame.draw.rect(surface, BORDER_DEFAULT, panel_rect, width=2, border_radius=8)

        text_y = panel_rect.y + self.VERTICAL_PADDING

        for line in lines:
            line_surface = self.font.render(line, True, TEXT_PRIMARY)
            line_rect = line_surface.get_rect(centerx=panel_rect.centerx, y=text_y)
            surface.blit(line_surface, line_rect)
            text_y += line_height + self.LINE_SPACING

    def _wrap_text(self, text: str, maximum_width: int) -> list[str]:
        """Split text into lines that fit inside the message box."""
        words = text.split()

        if not words:
            return [""]

        lines: list[str] = []
        current_line = words[0]

        for word in words[1:]:
            candidate = f"{current_line} {word}"

            if self.font.size(candidate)[0] <= maximum_width:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines
