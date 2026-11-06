import argparse

from game.app import GameApp


def main() -> None:
    parser = argparse.ArgumentParser(description="Mysterious Forest")
    parser.add_argument("--smoke-test", action="store_true", help="Validate bundled startup and exit.")
    args = parser.parse_args()
    app = GameApp()
    if args.smoke_test:
        # Exercise startup, content JSON, rendering, font data and the real event loop.
        # QUIT is handled before another frame; no interaction or persistent writes.
        import pygame

        pygame.event.post(pygame.event.Event(pygame.QUIT))
    app.run()


if __name__ == "__main__":
    main()
