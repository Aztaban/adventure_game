from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.theme import (
    NPC_BACKGROUND,
    NPC_BACKGROUND_HOVERED,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
)


@dataclass
class NPC:
    """Clickable non-player character with dialogue."""

    rect: pygame.Rect
    name: str
    dialogue_lines: tuple[str, ...]

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
