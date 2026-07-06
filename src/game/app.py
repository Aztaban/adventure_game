from __future__ import annotations

import pygame

from game.content.demo_world import create_demo_scenes
from game.content.scene_ids import STARTING_SCENE_ID
from game.game_state import GameState
from game.input.bindings import is_cancel
from game.scene_manager import SceneManager
from game.settings import (
    FPS,
    GAME_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from game.theme import TEXT_SECONDARY


class GameApp:
    """Main game application."""

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.debug_font = pygame.font.Font(None, 26)

        self.game_state = GameState()

        self.scene_manager = SceneManager(
            scenes=create_demo_scenes(self.game_state),
            starting_scene_id=STARTING_SCENE_ID,
        )

    def run(self) -> None:
        """Run the main game loop."""
        try:
            while self.is_running:
                delta_time = self.clock.tick(FPS) / 1000.0

                self._handle_events()
                self.scene_manager.update(delta_time)
                self._draw()
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Handle window events, scene input, and global cancellation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                continue

            event_consumed = self.scene_manager.handle_event(event)

            if event_consumed:
                continue

            if is_cancel(event):
                self.is_running = False

    def _draw(self) -> None:
        """Draw the active scene and debug information."""
        self.scene_manager.draw(self.screen)

        fps = int(self.clock.get_fps())
        debug_text = f"Scene: {self.scene_manager.current_scene_id} | FPS: {fps}"
        debug_surface = self.debug_font.render(
            debug_text,
            True,
            TEXT_SECONDARY,
        )

        self.screen.blit(debug_surface, (20, WINDOW_HEIGHT - 35))

        pygame.display.flip()
