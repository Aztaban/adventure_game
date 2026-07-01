from __future__ import annotations

import pygame

from game.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    GAME_TITLE,
    BACKGROUND_COLOR,
    TEXT_COLOR,
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
        self.font = pygame.font.Font(None, 36)

    def run(self) -> None:
        """Run the main game loop."""
        while self.is_running:
            self._handle_events()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self) -> None:
        """Handle global window/game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False

    def _draw(self) -> None:
        """Draw the current frame."""
        self.screen.fill(BACKGROUND_COLOR)

        fps = int(self.clock.get_fps())
        title_surface = self.font.render("Adventure Game Prototype", True, TEXT_COLOR)
        info_surface = self.font.render("Milestone v0.1 - ESC to quit", True, TEXT_COLOR)
        fps_surface = self.font.render(f"FPS: {fps}", True, TEXT_COLOR)

        self.screen.blit(title_surface, (40, 40))
        self.screen.blit(info_surface, (40, 90))
        self.screen.blit(fps_surface, (40, 140))

        pygame.display.flip()