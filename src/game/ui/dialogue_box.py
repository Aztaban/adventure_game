from __future__ import annotations

import pygame

from game.input.bindings import InputAction, input_summary_for
from game.theme import (
    DIALOGUE_BACKGROUND,
    DIALOGUE_BORDER,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from game.ui.text import wrap_text


class DialogueBox:
    """Render dialogue text in a spacious panel at the bottom of the screen."""

    PANEL_HEIGHT = 198
    PANEL_MARGIN = 22
    INNER_PADDING = 22
    LINE_SPACING = 7
    SPEAKER_GAP = 12
    HINT_TOP_GAP = 10

    def __init__(
        self,
        text_font: pygame.font.Font,
        hint_font: pygame.font.Font,
    ) -> None:
        self.text_font = text_font
        self.hint_font = hint_font

    @staticmethod
    def input_hint() -> str:
        """Return dialogue controls derived from the binding catalog."""
        advance = input_summary_for(InputAction.PRIMARY, InputAction.DIALOGUE_ADVANCE)
        cancel = input_summary_for(InputAction.CANCEL)

        return f"{advance} to continue  •  {cancel} to close"

    def draw(
        self,
        surface: pygame.Surface,
        speaker_name: str,
        text: str,
    ) -> None:
        """Draw the dialogue box."""
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
            border_radius=12,
        )
        pygame.draw.rect(
            surface,
            DIALOGUE_BORDER,
            panel_rect,
            width=2,
            border_radius=12,
        )

        speaker_surface = self.text_font.render(
            speaker_name,
            True,
            TEXT_HIGHLIGHT,
        )
        surface.blit(
            speaker_surface,
            (
                panel_rect.x + self.INNER_PADDING,
                panel_rect.y + self.INNER_PADDING,
            ),
        )

        separator_y = panel_rect.y + self.INNER_PADDING + speaker_surface.get_height() + self.SPEAKER_GAP
        pygame.draw.line(
            surface,
            DIALOGUE_BORDER,
            (panel_rect.x + self.INNER_PADDING, separator_y),
            (panel_rect.right - self.INNER_PADDING, separator_y),
            width=1,
        )

        text_x = panel_rect.x + self.INNER_PADDING
        text_y = separator_y + self.SPEAKER_GAP
        hint_height = self.hint_font.get_linesize()
        maximum_width = panel_rect.width - self.INNER_PADDING * 2
        maximum_text_bottom = panel_rect.bottom - self.INNER_PADDING - hint_height - self.HINT_TOP_GAP

        for line in wrap_text(self.text_font, text, maximum_width):
            if text_y + self.text_font.get_linesize() > maximum_text_bottom:
                break

            line_surface = self.text_font.render(
                line,
                True,
                TEXT_PRIMARY,
            )
            surface.blit(line_surface, (text_x, text_y))
            text_y += self.text_font.get_linesize() + self.LINE_SPACING

        hint_surface = self.hint_font.render(
            self.input_hint(),
            True,
            TEXT_SECONDARY,
        )
        hint_rect = hint_surface.get_rect(
            bottomright=(
                panel_rect.right - self.INNER_PADDING,
                panel_rect.bottom - self.INNER_PADDING,
            )
        )
        surface.blit(hint_surface, hint_rect)
