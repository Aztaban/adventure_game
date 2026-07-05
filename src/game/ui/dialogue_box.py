from __future__ import annotations

import pygame

from game.theme import (
    DIALOGUE_BACKGROUND,
    DIALOGUE_BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class DialogueBox:
    """Render dialogue text in a panel at the bottom of the screen."""

    PANEL_MARGIN = 30
    PANEL_HEIGHT = 180
    INNER_PADDING = 24
    LINE_SPACING = 8

    def __init__(self) -> None:
        self.text_font = pygame.font.Font(None, 32)
        self.hint_font = pygame.font.Font(None, 23)

    def draw(
        self,
        surface: pygame.Surface,
        speaker_name: str,
        text: str,
    ) -> None:
        """Draw the active dialogue panel."""
        panel_rect = pygame.Rect(
            self.PANEL_MARGIN,
            surface.get_height() - self.PANEL_HEIGHT - self.PANEL_MARGIN,
            surface.get_width() - self.PANEL_MARGIN * 2,
            self.PANEL_HEIGHT,
        )

        pygame.draw.rect(
            surface,
            DIALOGUE_BACKGROUND,
            panel_rect,
            border_radius=10,
        )
        pygame.draw.rect(
            surface,
            DIALOGUE_BORDER,
            panel_rect,
            width=2,
            border_radius=10,
        )

        speaker_surface = self.text_font.render(
            speaker_name,
            True,
            TEXT_PRIMARY,
        )
        surface.blit(
            speaker_surface,
            (
                panel_rect.x + self.INNER_PADDING,
                panel_rect.y + self.INNER_PADDING,
            ),
        )

        text_x = panel_rect.x + self.INNER_PADDING
        text_y = panel_rect.y + self.INNER_PADDING + 42
        maximum_width = panel_rect.width - self.INNER_PADDING * 2

        for line in self._wrap_text(text, maximum_width):
            line_surface = self.text_font.render(
                line,
                True,
                TEXT_PRIMARY,
            )
            surface.blit(line_surface, (text_x, text_y))
            text_y += self.text_font.get_linesize() + self.LINE_SPACING

        hint_surface = self.hint_font.render(
            "Click, Space or Enter to continue | Esc to close",
            True,
            TEXT_SECONDARY,
        )
        hint_rect = hint_surface.get_rect(
            bottomright=(
                panel_rect.right - self.INNER_PADDING,
                panel_rect.bottom - 14,
            )
        )
        surface.blit(hint_surface, hint_rect)

    def _wrap_text(
        self,
        text: str,
        maximum_width: int,
    ) -> list[str]:
        """Split text into lines that fit inside the panel."""
        words = text.split()

        if not words:
            return [""]

        lines: list[str] = []
        current_line = words[0]

        for word in words[1:]:
            candidate = f"{current_line} {word}"

            if self.text_font.size(candidate)[0] <= maximum_width:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines
