from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pygame

from game.input.bindings import InputAction, actions_for_event, binding_for
from game.theme import (
    BORDER_DEFAULT,
    MENU_BUTTON_BACKGROUND,
    MENU_BUTTON_HOVERED,
    MENU_OVERLAY,
    PANEL_BACKGROUND,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from game.ui.resources import UIResources
from game.ui.text import wrap_text


class ControlsResult(Enum):
    """Local outcomes emitted by the read-only Controls screen."""

    BACK = "back"


@dataclass(frozen=True)
class ControlBindingRow:
    """One player-facing action label and its authoritative input summary."""

    action: InputAction
    action_label: str
    input_summary: str


class ControlsScreen:
    """Read-only control reference with one reusable Back action."""

    ACTION_ORDER = (
        InputAction.PRIMARY,
        InputAction.DIALOGUE_ADVANCE,
        InputAction.MENU_CONFIRM,
        InputAction.CANCEL,
        InputAction.MENU_UP,
        InputAction.MENU_DOWN,
        InputAction.NEW_GAME,
        InputAction.FULLSCREEN_TOGGLE,
    )

    PANEL_MARGIN_X = 150
    PANEL_TOP = 58
    PANEL_BOTTOM = 674
    TITLE_Y = 105
    SUBTITLE_Y = 151
    HEADER_Y = 197
    ROW_START_Y = 233
    ROW_HEIGHT = 43
    ACTION_COLUMN_X = 230
    ACTION_COLUMN_WIDTH = 380
    INPUT_COLUMN_X = 650
    INPUT_COLUMN_WIDTH = 390
    BACK_BUTTON_WIDTH = 280
    BACK_BUTTON_HEIGHT = 58
    BACK_BUTTON_Y = 592

    def __init__(self, *, background_asset_id: str | None = None) -> None:
        self.background_asset_id = background_asset_id
        self.back_selected = True

    def reset_selection(self) -> None:
        """Restore keyboard focus to the only local action."""
        self.back_selected = True

    def binding_rows(self) -> tuple[ControlBindingRow, ...]:
        """Return display rows derived from the authoritative binding catalog."""
        return tuple(
            ControlBindingRow(
                action=action,
                action_label=binding_for(action).display_name,
                input_summary=binding_for(action).input_summary,
            )
            for action in self.ACTION_ORDER
        )

    def back_button_rect(self, surface_size: tuple[int, int]) -> pygame.Rect:
        """Return deterministic Back-button geometry for drawing and hit testing."""
        width, _ = surface_size
        return pygame.Rect(
            width // 2 - self.BACK_BUTTON_WIDTH // 2,
            self.BACK_BUTTON_Y,
            self.BACK_BUTTON_WIDTH,
            self.BACK_BUTTON_HEIGHT,
        )

    def handle_event(
        self,
        event: pygame.event.Event,
        surface_size: tuple[int, int],
    ) -> ControlsResult | None:
        """Handle local Controls-screen navigation without owning app navigation."""
        actions = actions_for_event(event)
        back_rect = self.back_button_rect(surface_size)

        if event.type == pygame.MOUSEMOTION:
            position = getattr(event, "pos", None)
            self.back_selected = position is not None and back_rect.collidepoint(position)
            return None

        if InputAction.PRIMARY in actions:
            position = getattr(event, "pos", None)

            if position is not None and back_rect.collidepoint(position):
                self.back_selected = True
                return ControlsResult.BACK

            return None

        if InputAction.MENU_UP in actions or InputAction.MENU_DOWN in actions:
            self.back_selected = True
            return None

        if InputAction.MENU_CONFIRM in actions or InputAction.CANCEL in actions:
            return ControlsResult.BACK

        return None

    def draw(self, surface: pygame.Surface, resources: UIResources) -> None:
        """Draw the current bindings and local Back actions."""
        background = resources.image(self.background_asset_id, surface.get_size())

        if background is None:
            surface.fill((35, 30, 52))
        else:
            surface.blit(background, (0, 0))

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill(MENU_OVERLAY)
        surface.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(
            self.PANEL_MARGIN_X,
            self.PANEL_TOP,
            surface.get_width() - self.PANEL_MARGIN_X * 2,
            self.PANEL_BOTTOM - self.PANEL_TOP,
        )
        pygame.draw.rect(surface, PANEL_BACKGROUND, panel_rect, border_radius=14)
        pygame.draw.rect(
            surface,
            BORDER_DEFAULT,
            panel_rect,
            width=2,
            border_radius=14,
        )

        title_surface = resources.title_font.render("Controls", True, TEXT_HIGHLIGHT)
        surface.blit(title_surface, title_surface.get_rect(center=(surface.get_width() // 2, self.TITLE_Y)))

        subtitle_surface = resources.hint_font.render("Current bindings are read-only.", True, TEXT_SECONDARY)
        surface.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(surface.get_width() // 2, self.SUBTITLE_Y)),
        )

        action_header = resources.small_font.render("Action", True, TEXT_HIGHLIGHT)
        input_header = resources.small_font.render("Input", True, TEXT_HIGHLIGHT)
        surface.blit(action_header, (self.ACTION_COLUMN_X, self.HEADER_Y))
        surface.blit(input_header, (self.INPUT_COLUMN_X, self.HEADER_Y))

        for index, row in enumerate(self.binding_rows()):
            row_y = self.ROW_START_Y + index * self.ROW_HEIGHT
            self._draw_wrapped_column(
                surface,
                resources,
                row.action_label,
                self.ACTION_COLUMN_X,
                row_y,
                self.ACTION_COLUMN_WIDTH,
            )
            self._draw_wrapped_column(
                surface,
                resources,
                row.input_summary,
                self.INPUT_COLUMN_X,
                row_y,
                self.INPUT_COLUMN_WIDTH,
            )

        back_rect = self.back_button_rect(surface.get_size())
        fill_color = MENU_BUTTON_HOVERED if self.back_selected else MENU_BUTTON_BACKGROUND
        border_color = TEXT_HIGHLIGHT if self.back_selected else BORDER_DEFAULT
        pygame.draw.rect(surface, fill_color, back_rect, border_radius=10)
        pygame.draw.rect(surface, border_color, back_rect, width=2, border_radius=10)

        back_surface = resources.menu_button_font.render("Back", True, TEXT_PRIMARY)
        surface.blit(back_surface, back_surface.get_rect(center=back_rect.center))

    @staticmethod
    def _draw_wrapped_column(
        surface: pygame.Surface,
        resources: UIResources,
        text: str,
        x: int,
        y: int,
        width: int,
    ) -> None:
        """Draw one compact column value while keeping long labels readable."""
        line_y = y

        for line in wrap_text(resources.small_font, text, width):
            line_surface = resources.small_font.render(line, True, TEXT_PRIMARY)
            surface.blit(line_surface, (x, line_y))
            line_y += resources.small_font.get_linesize()
