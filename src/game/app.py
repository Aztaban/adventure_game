from __future__ import annotations

import pygame

from game.content.demo_world import create_demo_scenes
from game.scene_manager import SceneManager
from game.scenes.adventure_scene import AdventureScene
from game.settings import (
    FPS,
    GAME_TITLE,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class GameApp:
    """Main game application.

    - initialize Pygame
    - open a window
    - run a stable game loop
    - handle quit / ESC
    - draw a simple background and text
    """

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.debug_font = pygame.font.Font(None, 26)

        self.scene_manager = SceneManager(
            scenes=create_demo_scenes(),
            starting_scene_id="village_square",
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
        """Handle window events and forward input to the active scene."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_scene = self.scene_manager.current_scene

                if isinstance(current_scene, AdventureScene) and current_scene.dialogue.is_active:
                    self.scene_manager.handle_event(event)
                else:
                    self.is_running = False

                continue

            self.scene_manager.handle_event(event)

    def _draw(self) -> None:
        """Draw the active scene and debug information."""
        self.scene_manager.draw(self.screen)

        fps = int(self.clock.get_fps())
        debug_text = f"Scene: {self.scene_manager.current_scene_id} | FPS: {fps}"
        debug_surface = self.debug_font.render(debug_text, True, TEXT_COLOR)

        self.screen.blit(debug_surface, (20, WINDOW_HEIGHT - 35))

        pygame.display.flip()
