from types import SimpleNamespace

import pygame
import pytest

import game.app as app_module
from game.app import AppMode, GameApp
from game.settings import LOGICAL_SIZE

PHYSICAL_SIZE = (1600, 900)


class RecordingDrawTarget:
    """Record which surface one top-level presenter receives."""

    def __init__(self, name: str, draw_calls: list[tuple[str, object]]) -> None:
        self.name = name
        self.draw_calls = draw_calls

    def draw(self, surface: pygame.Surface, *args: object) -> None:
        del args
        self.draw_calls.append((self.name, surface))


class RecordingViewport:
    """Record logical presentation without opening a physical display."""

    def __init__(self, draw_calls: list[tuple[str, object]]) -> None:
        self.logical_surface = pygame.Surface(LOGICAL_SIZE)
        self.logical_size = LOGICAL_SIZE
        self.output_surface = pygame.Surface(PHYSICAL_SIZE)
        self.draw_calls = draw_calls

    def present(self) -> None:
        self.draw_calls.append(
            ("present", (self.logical_surface, self.output_surface))
        )


def create_draw_test_app(
    mode: AppMode,
) -> tuple[GameApp, list[tuple[str, object]]]:
    """Create the smallest app shell needed to protect draw routing."""
    app = object.__new__(GameApp)
    draw_calls: list[tuple[str, object]] = []
    app.viewport = RecordingViewport(draw_calls)
    app.mode = mode
    app.ui_resources = object()
    app.display_error_message = None

    app.title_screen = RecordingDrawTarget("title", draw_calls)
    app.controls_screen = RecordingDrawTarget("controls", draw_calls)
    app.ending_screen = RecordingDrawTarget("ending", draw_calls)
    app.session = SimpleNamespace(
        scene_manager=RecordingDrawTarget("gameplay", draw_calls),
    )
    return app, draw_calls


def test_logical_resolution_contract_is_1280_by_720() -> None:
    assert LOGICAL_SIZE == (1280, 720)


@pytest.mark.parametrize(
    ("mode", "expected_presenters"),
    [
        (AppMode.TITLE, ["title"]),
        (AppMode.CONTROLS, ["controls"]),
        (AppMode.PLAYING, ["gameplay"]),
        (AppMode.ENDING, ["gameplay", "ending"]),
    ],
)
def test_top_level_modes_draw_to_logical_surface_before_presentation(
    mode: AppMode,
    expected_presenters: list[str],
) -> None:
    app, draw_calls = create_draw_test_app(mode)

    app._draw()

    assert [name for name, _ in draw_calls] == [*expected_presenters, "present"]
    assert all(
        surface is app.viewport.logical_surface
        for name, surface in draw_calls
        if name != "present"
    )
    assert draw_calls[-1][1] == (
        app.viewport.logical_surface,
        app.viewport.output_surface,
    )
    assert app.viewport.logical_surface.get_size() == LOGICAL_SIZE
    assert app.viewport.output_surface.get_size() == PHYSICAL_SIZE


def test_debug_overlay_draws_to_logical_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app, draw_calls = create_draw_test_app(AppMode.PLAYING)

    def record_debug(surface: pygame.Surface) -> None:
        draw_calls.append(("debug", surface))

    app._draw_debug_overlay = record_debug
    monkeypatch.setattr(app_module, "SHOW_DEBUG_OVERLAY", True)

    app._draw()

    assert [name for name, _ in draw_calls] == ["gameplay", "debug", "present"]
    assert draw_calls[1][1] is app.viewport.logical_surface
