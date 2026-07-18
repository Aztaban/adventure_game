from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pygame

from game.theme import (
    BORDER_DEFAULT,
    MENU_BUTTON_BACKGROUND,
    MENU_BUTTON_HOVERED,
    MENU_OVERLAY,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from game.ui.resources import UIResources
from game.ui.text import wrap_text


class MenuAction(Enum):
    """Actions emitted by the small title and ending menus."""

    PRIMARY = "primary"
    QUIT = "quit"


@dataclass(frozen=True)
class MenuButtonLayout:
    """one menu action and its current button rectangle."""

    label: str
    action: MenuAction
    rect: pygame.Rect


class MenuScreen:
    """A focused two-button screen used for title and ending presentation."""

    BUTTON_WIDTH = 340
    BUTTON_HEIGHT = 64
    BUTTON_GAP = 18
    BUTTON_START_Y = 430

    def __init__(
        self,
        *,
        title: str,
        subtitle: str,
        primary_label: str,
        background_asset_id: str | None = None,
        overlay_gameplay: bool = False,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.primary_label = primary_label
        self.background_asset_id = background_asset_id
        self.overlay_gameplay = overlay_gameplay
        self.selected_index = 0

    def reset_selection(self) -> None:
        """Restore the primary action as the selected button."""
        self.selected_index = 0

    def handle_event(
        self,
        event: pygame.event.Event,
        surface_size: tuple[int, int],
    ) -> MenuAction | None:
        """Handle keyboard or mouse menu input."""
        buttons = self.layout(surface_size)

        if event.type == pygame.MOUSEMOTION:
            hovered_index = self._button_index_at(event.pos, buttons)

            if hovered_index is not None:
                self.selected_index = hovered_index

            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_index = self._button_index_at(event.pos, buttons)

            if clicked_index is None:
                return None

            self.selected_index = clicked_index
            return buttons[clicked_index].action

        if event.type != pygame.KEYDOWN:
            return None

        if event.key in {pygame.K_UP, pygame.K_w}:
            self.selected_index = (self.selected_index - 1) % len(buttons)
            return None

        if event.key in {pygame.K_DOWN, pygame.K_s}:
            self.selected_index = (self.selected_index + 1) % len(buttons)
            return None

        if event.key in {pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE}:
            return buttons[self.selected_index].action

        if event.key == pygame.K_ESCAPE:
            return MenuAction.QUIT

        return None

    def draw(
        self,
        surface: pygame.Surface,
        resources: UIResources,
    ) -> None:
        """Draw the title or ending menu."""
        if self.overlay_gameplay:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill(MENU_OVERLAY)
            surface.blit(overlay, (0, 0))
        else:
            background = resources.image(
                self.background_asset_id,
                surface.get_size(),
            )

            if background is None:
                surface.fill((35, 30, 52))
            else:
                surface.blit(background, (0, 0))

        title_surface = resources.menu_title_font.render(self.title, True, TEXT_HIGHLIGHT)
        title_rect = title_surface.get_rect(center=(surface.get_width() // 2, 190))
        surface.blit(title_surface, title_rect)

        subtitle_width = 760
        subtitle_y = title_rect.bottom + 28

        for line in wrap_text(resources.menu_subtitle_font, self.subtitle, subtitle_width):
            line_surface = resources.menu_subtitle_font.render(line, True, TEXT_PRIMARY)
            line_rect = line_surface.get_rect(center=(surface.get_width() // 2, subtitle_y))
            surface.blit(line_surface, line_rect)
            subtitle_y += resources.menu_subtitle_font.get_linesize() + 6

        for index, button in enumerate(self.layout(surface.get_size())):
            is_selected = index == self.selected_index
            fill_color = MENU_BUTTON_HOVERED if is_selected else MENU_BUTTON_BACKGROUND
            border_color = TEXT_HIGHLIGHT if is_selected else BORDER_DEFAULT

            pygame.draw.rect(surface, fill_color, button.rect, border_radius=10)
            pygame.draw.rect(surface, border_color, button.rect, width=2, border_radius=10)

            button_surface = resources.menu_button_font.render(button.label, True, TEXT_PRIMARY)
            surface.blit(button_surface, button_surface.get_rect(center=button.rect.center))

        hint_surface = resources.hint_font.render(
            "Mouse or Arrow Keys | Enter to select | Esc to quit",
            True,
            TEXT_SECONDARY,
        )
        hint_rect = hint_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() - 52))
        surface.blit(hint_surface, hint_rect)

    def layout(self, surface_size: tuple[int, int]) -> tuple[MenuButtonLayout, ...]:
        """Return deterministic button geometry for drawing and hit testing."""
        width, _ = surface_size
        button_x = width // 2 - self.BUTTON_WIDTH // 2

        return (
            MenuButtonLayout(
                label=self.primary_label,
                action=MenuAction.PRIMARY,
                rect=pygame.Rect(
                    button_x,
                    self.BUTTON_START_Y,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                ),
            ),
            MenuButtonLayout(
                label="Quit",
                action=MenuAction.QUIT,
                rect=pygame.Rect(
                    button_x,
                    self.BUTTON_START_Y + self.BUTTON_HEIGHT + self.BUTTON_GAP,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                ),
            ),
        )

    @staticmethod
    def _button_index_at(
        position: tuple[int, int],
        buttons: tuple[MenuButtonLayout, ...],
    ) -> int | None:
        """Return the button index under a position."""
        for index, button in enumerate(buttons):
            if button.rect.collidepoint(position):
                return index

        return None
