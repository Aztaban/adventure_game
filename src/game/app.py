from __future__ import annotations

import pygame

from game.entities.exit_hotspot import ExitHotspot
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

        self.scene_manager = self._create_scene_manager()

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
        """Handle global events and forward others to the scene."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False
            else:
                self.scene_manager.handle_event(event)

    def _draw(self) -> None:
        """Draw the active scene and debug information."""
        self.scene_manager.draw(self.screen)

        fps = int(self.clock.get_fps())
        debug_text = f"Scene: {self.scene_manager.current_scene_id} | FPS: {fps}"
        debug_surface = self.debug_font.render(debug_text, True, TEXT_COLOR)

        self.screen.blit(debug_surface, (20, WINDOW_HEIGHT - 35))

        pygame.display.flip()

    def _create_scene_manager(self) -> SceneManager:
        """Create the initial placeholder scenes."""
        village_square = AdventureScene(
            name="Village Square",
            description="A peacefull square with a suspicious lack of villagers.",
            background_color=(63, 48, 78),
            exits=[
                ExitHotspot(
                    rect=pygame.Rect(WINDOW_WIDTH - 240, WINDOW_HEIGHT // 2 - 50, 190, 100),
                    target_scene_id="forest_path",
                    label="To Forest",
                )
            ],
        )

        forest_path = AdventureScene(
            name="Forest Path",
            description="The trees appear to be discussing you quietly.",
            background_color=(40, 72, 58),
            exits=[
                ExitHotspot(
                    rect=pygame.Rect(
                        50,
                        WINDOW_HEIGHT // 2 - 50,
                        190,
                        100,
                    ),
                    target_scene_id="village_square",
                    label="To Village",
                )
            ],
        )

        scenes = {
            "village_square": village_square,
            "forest_path": forest_path,
        }

        return SceneManager(scenes=scenes, starting_scene_id="village_square")
