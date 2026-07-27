from __future__ import annotations

from types import SimpleNamespace

import pygame
import pytest

import game.app as app_module
from game.app import AppMode, GameApp
from game.display import DisplayModeChangeError, calculate_destination_rect
from game.settings import (
    DEFAULT_WINDOWED_SIZE,
    LOGICAL_SIZE,
    WINDOWED_PRESETS,
)


class RecordingSceneManager:
    """Record whether a display action leaks into gameplay event handling."""

    def __init__(self) -> None:
        self.current_scene_id = "scene"
        self.handled_events = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        del event
        self.handled_events += 1
        return False


class RecordingResources:
    """Minimal resource double for app-level display tests."""

    def play_sound(self, asset_id: str | None, *, volume: float = 0.55) -> None:
        del asset_id, volume


class DisplaySurfaceFactory:
    """Record requested display modes and return matching surfaces."""

    def __init__(self) -> None:
        self.calls: list[tuple[tuple[int, int], bool]] = []

    def __call__(
        self,
        size: tuple[int, int],
        *,
        fullscreen: bool,
    ) -> pygame.Surface:
        self.calls.append((size, fullscreen))
        return pygame.Surface(size)


def create_display_test_app(
    *,
    mode: AppMode = AppMode.TITLE,
    fullscreen: bool = True,
    output_size: tuple[int, int] = (2560, 1440),
) -> GameApp:
    """Create an app shell with display state but no real window."""
    app = object.__new__(GameApp)
    app.logical_surface = pygame.Surface(LOGICAL_SIZE)
    app.screen = pygame.Surface(output_size)
    app.presentation_rect = calculate_destination_rect(LOGICAL_SIZE, output_size)
    app.is_fullscreen = fullscreen
    app.last_windowed_preset = DEFAULT_WINDOWED_SIZE
    app.display_error_message = None
    app.is_running = True
    app.mode = mode
    app.ui_resources = RecordingResources()
    app.session = SimpleNamespace(
        scene_manager=RecordingSceneManager(),
        game_state=SimpleNamespace(ending_reached=False),
    )
    return app


def test_approved_windowed_presets_match_display_decision() -> None:
    assert WINDOWED_PRESETS == (
        (1280, 720),
        (1600, 900),
        (1920, 1080),
    )
    assert DEFAULT_WINDOWED_SIZE == (1280, 720)


def test_fresh_app_starts_at_primary_desktop_size_in_fullscreen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    display_factory = DisplaySurfaceFactory()
    dummy_content = object()
    dummy_session = object()

    monkeypatch.setattr(pygame, "init", lambda: None)
    monkeypatch.setattr(pygame.display, "set_caption", lambda title: None)
    monkeypatch.setattr(app_module, "primary_desktop_size", lambda: (2560, 1440))
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)
    monkeypatch.setattr(app_module, "UIResources", lambda: object())
    monkeypatch.setattr(app_module, "create_demo_content", lambda resources: dummy_content)
    monkeypatch.setattr(
        app_module,
        "create_game_session",
        lambda content, resources: dummy_session,
    )

    app = GameApp()

    assert display_factory.calls == [((2560, 1440), True)]
    assert app.screen.get_size() == (2560, 1440)
    assert app.is_fullscreen
    assert app.last_windowed_preset == DEFAULT_WINDOWED_SIZE
    assert app.presentation_rect == pygame.Rect(0, 0, 2560, 1440)
    assert app.content is dummy_content
    assert app.session is dummy_session


def test_leaving_fullscreen_uses_initial_1280_by_720_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app()
    display_factory = DisplaySurfaceFactory()
    session = app.session
    mode = app.mode
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)

    changed = app.toggle_fullscreen()

    assert changed
    assert display_factory.calls == [(DEFAULT_WINDOWED_SIZE, False)]
    assert not app.is_fullscreen
    assert app.screen.get_size() == DEFAULT_WINDOWED_SIZE
    assert app.last_windowed_preset == DEFAULT_WINDOWED_SIZE
    assert app.presentation_rect == pygame.Rect(0, 0, *DEFAULT_WINDOWED_SIZE)
    assert app.session is session
    assert app.mode is mode


@pytest.mark.parametrize("preset", WINDOWED_PRESETS)
def test_approved_windowed_presets_can_be_selected_without_resetting_game(
    preset: tuple[int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app(mode=AppMode.PLAYING)
    display_factory = DisplaySurfaceFactory()
    session = app.session
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)

    changed = app.set_windowed_preset(preset)

    assert changed
    assert display_factory.calls == [(preset, False)]
    assert app.screen.get_size() == preset
    assert not app.is_fullscreen
    assert app.last_windowed_preset == preset
    assert app.session is session
    assert app.mode is AppMode.PLAYING


def test_fullscreen_toggle_restores_last_session_windowed_preset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app()
    display_factory = DisplaySurfaceFactory()
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)
    monkeypatch.setattr(app_module, "primary_desktop_size", lambda: (3440, 1440))

    assert app.set_windowed_preset((1600, 900))
    assert app.toggle_fullscreen()
    assert app.toggle_fullscreen()

    assert display_factory.calls == [
        ((1600, 900), False),
        ((3440, 1440), True),
        ((1600, 900), False),
    ]
    assert not app.is_fullscreen
    assert app.last_windowed_preset == (1600, 900)
    assert app.screen.get_size() == (1600, 900)


def test_new_app_display_state_does_not_reuse_previous_session_choice() -> None:
    previous_app = create_display_test_app(fullscreen=False, output_size=(1920, 1080))
    previous_app.last_windowed_preset = (1920, 1080)

    fresh_app = create_display_test_app()

    assert previous_app.last_windowed_preset == (1920, 1080)
    assert fresh_app.is_fullscreen
    assert fresh_app.last_windowed_preset == DEFAULT_WINDOWED_SIZE


@pytest.mark.parametrize("mode", [AppMode.CONTROLS, AppMode.PLAYING])
def test_f11_is_global_and_preserves_the_active_mode(
    mode: AppMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app(mode=mode)
    display_factory = DisplaySurfaceFactory()
    session = app.session
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)
    monkeypatch.setattr(
        pygame.event,
        "get",
        lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11)],
    )

    app._handle_events()

    assert display_factory.calls == [(DEFAULT_WINDOWED_SIZE, False)]
    assert app.session is session
    assert app.mode is mode
    assert app.session.scene_manager.handled_events == 0


@pytest.mark.parametrize(
    "mode",
    [AppMode.TITLE, AppMode.CONTROLS, AppMode.PLAYING, AppMode.ENDING],
)
def test_repeated_mode_changes_preserve_top_level_mode_and_session(
    mode: AppMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app(mode=mode)
    display_factory = DisplaySurfaceFactory()
    session = app.session
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)
    monkeypatch.setattr(app_module, "primary_desktop_size", lambda: (1920, 1200))

    for _ in range(3):
        assert app.toggle_fullscreen()
        assert app.toggle_fullscreen()

    assert app.session is session
    assert app.mode is mode
    assert app.is_fullscreen
    assert app.presentation_rect == pygame.Rect(0, 60, 1920, 1080)


def test_mode_change_preserves_scene_dialogue_and_inventory_selection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app(mode=AppMode.PLAYING)
    display_factory = DisplaySurfaceFactory()
    dialogue = SimpleNamespace(is_active=True, current_line="Still talking.")
    selected_item = object()
    active_scene = SimpleNamespace(dialogue=dialogue)
    app.session.scene_manager.current_scene = active_scene
    app.session.game_state.inventory = SimpleNamespace(selected_item=selected_item)
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)

    assert app.toggle_fullscreen()

    assert app.session.scene_manager.current_scene is active_scene
    assert active_scene.dialogue is dialogue
    assert dialogue.is_active
    assert app.session.game_state.inventory.selected_item is selected_item
    assert app.mode is AppMode.PLAYING


def test_display_recreation_error_keeps_existing_presentation_and_game_state(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    app = create_display_test_app(mode=AppMode.PLAYING)
    original_screen = app.screen
    original_rect = app.presentation_rect.copy()
    session = app.session

    def fail_display_change(
        size: tuple[int, int],
        *,
        fullscreen: bool,
    ) -> pygame.Surface:
        del size, fullscreen
        raise DisplayModeChangeError("Could not switch display mode.")

    monkeypatch.setattr(app_module, "create_display_surface", fail_display_change)

    changed = app.toggle_fullscreen()

    assert not changed
    assert app.screen is original_screen
    assert app.presentation_rect == original_rect
    assert app.is_fullscreen
    assert app.last_windowed_preset == DEFAULT_WINDOWED_SIZE
    assert app.session is session
    assert app.mode is AppMode.PLAYING
    assert app.display_error_message == "Could not switch display mode."
    assert "Could not switch display mode." in capsys.readouterr().err


def test_successful_display_change_clears_previous_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app()
    app.display_error_message = "Previous display error."
    monkeypatch.setattr(
        app_module,
        "create_display_surface",
        DisplaySurfaceFactory(),
    )

    assert app.toggle_fullscreen()
    assert app.display_error_message is None


def test_unapproved_windowed_size_is_rejected_before_display_recreation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_display_test_app()
    display_factory = DisplaySurfaceFactory()
    monkeypatch.setattr(app_module, "create_display_surface", display_factory)

    with pytest.raises(ValueError, match="Unsupported windowed size"):
        app.set_windowed_preset((1024, 768))

    assert display_factory.calls == []
    assert app.is_fullscreen
    assert app.last_windowed_preset == DEFAULT_WINDOWED_SIZE
