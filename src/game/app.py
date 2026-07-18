from __future__ import annotations

from enum import Enum

import pygame

from game.asset_ids import SCENE_TRANSITION_SOUND, TITLE_BACKGROUND
from game.content.demo_world import create_demo_content
from game.game_session import GameSession, create_game_session
from game.input.bindings import is_cancel, is_new_game
from game.settings import (
    FPS,
    GAME_TITLE,
    SHOW_DEBUG_OVERLAY,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from game.theme import TEXT_SECONDARY
from game.ui.menu_screen import MenuAction, MenuScreen
from game.ui.resources import UIResources


class AppMode(Enum):
    """Top-level presentation modes outside one gameplay session."""

    TITLE = "title"
    PLAYING = "playing"
    ENDING = "ending"


class GameApp:
    """Main game application."""

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
            background_asset_id=TITLE_BACKGROUND,
        )
        self.ending_screen = MenuScreen(
            title="Demo Complete",
            subtitle=(
                "The ancient tower opens, the pedestal glows, and the forest "
                "quietly decides you may be competent after all."
            ),
            primary_label="Play Again",
            overlay_gameplay=True,
        )

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

            if is_new_game(event):
                self.start_new_game()
                continue

            if self.mode is AppMode.TITLE:
                self._handle_menu_event(self.title_screen, event)
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

            if is_cancel(event):
                self.is_running = False

    def _handle_menu_event(
        self,
        menu: MenuScreen,
        event: pygame.event.Event,
    ) -> None:
        """Apply a title or ending menu action."""
        action = menu.handle_event(event, self.screen.get_size())

        if action is MenuAction.PRIMARY:
            self.start_new_game()
        elif action is MenuAction.QUIT:
            self.is_running = False

    def _draw(self) -> None:
        """Draw the active top-level presentation mode."""
        if self.mode is AppMode.TITLE:
            self.title_screen.draw(self.screen, self.ui_resources)
        else:
            self.session.scene_manager.draw(self.screen)

            if self.mode is AppMode.ENDING:
                self.ending_screen.draw(self.screen, self.ui_resources)
            elif SHOW_DEBUG_OVERLAY:
                self._draw_debug_overlay()

        pygame.display.flip()

    def _draw_debug_overlay(self) -> None:
        """Draw optional scene and FPS diagnostics."""
        fps = int(self.clock.get_fps())
        scene_id = self.session.scene_manager.current_scene_id
        debug_text = f"Scene: {scene_id} | FPS: {fps}"
        debug_surface = self.ui_resources.debug_font.render(
            debug_text,
            True,
            TEXT_SECONDARY,
        )

        self.screen.blit(debug_surface, (20, WINDOW_HEIGHT - 35))
