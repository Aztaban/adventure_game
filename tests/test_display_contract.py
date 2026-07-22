from types import SimpleNamespace

import pygame
import pytest

from game.app import AppMode, GameApp
from game.settings import WINDOW_HEIGHT, WINDOW_WIDTH

LOGICAL_SIZE = (1280, 720)


class RecordingDrawTarget:
    """Record which surface one top-level presenter receives."""

    def __init__(self, name: str, draw_calls: list[tuple[str, pygame.Surface]]) -> None:
        self.name = name
        self.draw_calls = draw_calls

    def draw(self, surface: pygame.Surface, *args: object) -> None:
        del args
        self.draw_calls.append((self.name, surface))


def create_draw_test_app(
    mode: AppMode,
) -> tuple[GameApp, list[tuple[str, pygame.Surface]]]:
    """Create the smallest app shell needed to protect draw routing."""
    app = object.__new__(GameApp)
    app.screen = pygame.Surface(LOGICAL_SIZE)
    app.mode = mode
    app.ui_resources = object()

    draw_calls: list[tuple[str, pygame.Surface]] = []
    app.title_screen = RecordingDrawTarget("title", draw_calls)
    app.ending_screen = RecordingDrawTarget("ending", draw_calls)
    app.session = SimpleNamespace(
        scene_manager=RecordingDrawTarget("gameplay", draw_calls),
    )
    return app, draw_calls


def test_logical_resolution_contract_is_1280_by_720() -> None:
    assert (WINDOW_WIDTH, WINDOW_HEIGHT) == LOGICAL_SIZE


@pytest.mark.parametrize(
    ("mode", "expected_presenters"),
    [
        (AppMode.TITLE, ["title"]),
        (AppMode.PLAYING, ["gameplay"]),
        (AppMode.ENDING, ["gameplay", "ending"]),
    ],
)
def test_top_level_modes_draw_directly_to_fixed_resolution_screen(
    mode: AppMode,
    expected_presenters: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app, draw_calls = create_draw_test_app(mode)
    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    app._draw()

    assert [name for name, _ in draw_calls] == expected_presenters
    assert all(surface is app.screen for _, surface in draw_calls)
    assert app.screen.get_size() == LOGICAL_SIZE
