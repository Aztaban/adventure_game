from __future__ import annotations

import sys
from enum import Enum

import pygame

from game.asset_ids import SCENE_TRANSITION_SOUND, TITLE_BACKGROUND
from game.content.demo_world import create_demo_content
from game.display import (
    LETTERBOX_COLOR,
    DisplayModeChangeError,
    DisplayViewport,
    primary_desktop_size,
)
from game.game_session import GameSession, create_game_session
from game.input.bindings import InputAction, actions_for_event
from game.settings import (
    DEFAULT_WINDOWED_SIZE,
    FPS,
    GAME_TITLE,
    LOGICAL_HEIGHT,
    LOGICAL_SIZE,
    SHOW_DEBUG_OVERLAY,
    WINDOWED_PRESETS,
)
from game.theme import TEXT_SECONDARY
from game.ui.controls_screen import ControlsResult, ControlsScreen
from game.ui.menu_screen import MenuAction, MenuScreen
from game.ui.message_box import MessageBox
from game.ui.resources import UIResources


class AppMode(Enum):
    """Top-level presentation modes outside one gameplay session."""

    TITLE = "title"
    CONTROLS = "controls"
    PLAYING = "playing"
    ENDING = "ending"


class GameApp:
    """Main game application."""

    def __init__(self) -> None:
        pygame.init()

        self.is_fullscreen = True
        self.last_windowed_preset = DEFAULT_WINDOWED_SIZE
        self.display_error_message: str | None = None
        self.viewport = DisplayViewport.create(
            LOGICAL_SIZE,
            primary_desktop_size(),
            fullscreen=True,
        )
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.ui_resources = UIResources()

        self.content = create_demo_content(self.ui_resources)
        self.session = self._create_new_session()
        self.mode = AppMode.TITLE

        self.title_screen = MenuScreen(
            title="Mysterious Forest",
            subtitle=(
                "A tiny point-and-click adventure about suspicious trees, "
                "retired magic, and one very important cup of tea."
            ),
            primary_label="Start Game",
            secondary_label="Controls",
            background_asset_id=TITLE_BACKGROUND,
        )
        self.controls_screen = ControlsScreen(background_asset_id=TITLE_BACKGROUND)
        self.controls_return_mode = AppMode.TITLE
        self.ending_screen = MenuScreen(
            title="Demo Complete",
            subtitle=(
                "The ancient tower opens, the pedestal glows, and the forest "
                "quietly decides you may be competent after all."
            ),
            primary_label="Play Again",
            overlay_gameplay=True,
        )
        self._draw()

    def _create_new_session(self) -> GameSession:
        """Create a fresh playable session using static demo content."""
        return create_game_session(self.content, self.ui_resources)

    def start_new_game(self) -> None:
        """Reset the current run and enter gameplay from Village Square."""
        self.session = self._create_new_session()
        self.mode = AppMode.PLAYING

        if hasattr(self, "title_screen"):
            self.title_screen.reset_selection()

        if hasattr(self, "ending_screen"):
            self.ending_screen.reset_selection()

        if hasattr(self, "controls_screen"):
            self.controls_screen.reset_selection()

    def set_windowed_preset(self, size: tuple[int, int]) -> bool:
        """Switch to one approved windowed size for the current session."""
        if size not in WINDOWED_PRESETS:
            approved_sizes = ", ".join(
                f"{width} x {height}" for width, height in WINDOWED_PRESETS
            )
            raise ValueError(
                f"Unsupported windowed size {size!r}. Approved sizes: {approved_sizes}."
            )

        return self._change_display_mode(
            size,
            fullscreen=False,
            windowed_preset=size,
        )

    def toggle_fullscreen(self) -> bool:
        """Toggle fullscreen while remembering the current-session windowed preset."""
        if self.is_fullscreen:
            return self.set_windowed_preset(self.last_windowed_preset)

        try:
            desktop_size = primary_desktop_size()
        except DisplayModeChangeError as error:
            self._report_display_error(str(error))
            return False

        return self._change_display_mode(desktop_size, fullscreen=True)

    def _change_display_mode(
        self,
        size: tuple[int, int],
        *,
        fullscreen: bool,
        windowed_preset: tuple[int, int] | None = None,
    ) -> bool:
        """Recreate only the physical display while preserving gameplay state."""
        if self.is_fullscreen is fullscreen and self.viewport.output_size == size:
            if windowed_preset is not None:
                self.last_windowed_preset = windowed_preset

            self.display_error_message = None
            return True
        try:
            self.viewport.recreate_output(size, fullscreen=fullscreen)
        except DisplayModeChangeError as error:
            self._report_display_error(str(error))
            return False

        self.is_fullscreen = fullscreen

        if windowed_preset is not None:
            self.last_windowed_preset = windowed_preset

        self.display_error_message = None
        self._draw()
        return True

    def _report_display_error(self, message: str) -> None:
        """Keep the current session alive and expose a clear display error."""
        self.display_error_message = message
        print(message, file=sys.stderr)

    def run(self) -> None:
        """Run the main game loop."""
        try:
            while self.is_running:
                delta_time = self.clock.tick(FPS) / 1000.0

                self._handle_events()

                if self.mode is AppMode.PLAYING:
                    self.session.scene_manager.update(delta_time)

                self._draw()
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Handle window, menu, gameplay, and global events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                continue

            event = self.viewport.convert_pointer_event(event)
            actions = actions_for_event(event)

            if InputAction.FULLSCREEN_TOGGLE in actions:
                self.toggle_fullscreen()
                continue

            if InputAction.NEW_GAME in actions:
                self.start_new_game()
                continue

            if self.mode is AppMode.TITLE:
                self._handle_menu_event(self.title_screen, event)
                continue

            if self.mode is AppMode.CONTROLS:
                self._handle_controls_event(event)
                continue

            if self.mode is AppMode.ENDING:
                self._handle_menu_event(self.ending_screen, event)
                continue

            previous_scene_id = self.session.scene_manager.current_scene_id
            event_consumed = self.session.scene_manager.handle_event(event)

            if self.session.scene_manager.current_scene_id != previous_scene_id:
                self.ui_resources.play_sound(SCENE_TRANSITION_SOUND, volume=0.45)

            if self.session.game_state.ending_reached:
                self.mode = AppMode.ENDING
                self.ending_screen.reset_selection()

            if event_consumed:
                continue

            if InputAction.CANCEL in actions:
                self.is_running = False

    def _handle_menu_event(
        self,
        menu: MenuScreen,
        event: pygame.event.Event,
    ) -> None:
        """Apply a title or ending menu action."""
        action = menu.handle_event(event, self.viewport.logical_size)

        if action is MenuAction.PRIMARY:
            self.start_new_game()
        elif action is MenuAction.CONTROLS:
            self.controls_return_mode = self.mode
            self.controls_screen.reset_selection()
            self.mode = AppMode.CONTROLS
        elif action is MenuAction.QUIT:
            self.is_running = False

    def _handle_controls_event(self, event: pygame.event.Event) -> None:
        """Apply one local Controls-screen result through app-owned navigation."""
        result = self.controls_screen.handle_event(
            event,
            self.viewport.logical_size,
        )

        if result is ControlsResult.BACK:
            self.mode = self.controls_return_mode

    def _draw(self) -> None:
        """Draw one logical frame and present it to the physical display."""
        logical_surface = self.viewport.logical_surface
        logical_surface.fill(LETTERBOX_COLOR)

        if self.mode is AppMode.TITLE:
            self.title_screen.draw(logical_surface, self.ui_resources)
        elif self.mode is AppMode.CONTROLS:
            self.controls_screen.draw(logical_surface, self.ui_resources)
        else:
            self.session.scene_manager.draw(logical_surface)

            if self.mode is AppMode.ENDING:
                self.ending_screen.draw(logical_surface, self.ui_resources)
            elif SHOW_DEBUG_OVERLAY:
                self._draw_debug_overlay(logical_surface)

        display_error_message = getattr(self, "display_error_message", None)

        if display_error_message:
            MessageBox(self.ui_resources.small_font).draw(
                logical_surface,
                display_error_message,
                available_rect=pygame.Rect(0, 0, *LOGICAL_SIZE),
            )

        self.viewport.present()

    def _draw_debug_overlay(self, surface: pygame.Surface) -> None:
        """Draw optional scene and FPS diagnostics onto the logical frame."""
        fps = int(self.clock.get_fps())
        scene_id = self.session.scene_manager.current_scene_id
        debug_text = f"Scene: {scene_id} | FPS: {fps}"
        debug_surface = self.ui_resources.debug_font.render(
            debug_text,
            True,
            TEXT_SECONDARY,
        )

        surface.blit(debug_surface, (20, LOGICAL_HEIGHT - 35))
