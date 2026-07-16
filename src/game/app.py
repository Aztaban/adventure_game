from __future__ import annotations

import pygame

from game.content.demo_world import create_demo_content
from game.game_session import GameSession, create_game_session
from game.input.bindings import is_cancel, is_new_game
from game.settings import (
    FPS,
    GAME_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from game.theme import TEXT_SECONDARY
from game.ui.resources import UIResources


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

    def _create_new_session(self) -> GameSession:
        """Create a fresh playable session using static demo content."""
        return create_game_session(self.content, self.ui_resources)

    def start_new_game(self) -> None:
        """Reset the current run by replacing the whole game session."""
        self.session = self._create_new_session()

    def run(self) -> None:
        """Run the main game loop."""
        try:
            while self.is_running:
                delta_time = self.clock.tick(FPS) / 1000.0

                self._handle_events()
                self.session.scene_manager.update(delta_time)
                self._draw()
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Handle window events, scene input, and global cancellation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                continue

            if is_new_game(event):
                self.start_new_game()
                continue

            event_consumed = self.session.scene_manager.handle_event(event)

            if event_consumed:
                continue

            if is_cancel(event):
                self.is_running = False

    def _draw(self) -> None:
        """Draw the active scene and debug information."""
        self.session.scene_manager.draw(self.screen)

        fps = int(self.clock.get_fps())
        scene_id = self.session.scene_manager.current_scene_id
        debug_text = f"Scene: {scene_id} | FPS: {fps}"
        debug_surface = self.ui_resources.debug_font.render(
            debug_text,
            True,
            TEXT_SECONDARY,
        )

        self.screen.blit(debug_surface, (20, WINDOW_HEIGHT - 35))

        pygame.display.flip()
