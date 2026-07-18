import pygame
import pytest

from game.app import AppMode, GameApp
from game.asset_ids import SCENE_TRANSITION_SOUND
from game.content.demo_world import create_demo_content
from game.content.item_ids import EMPTY_CUP
from game.content.scene_ids import STARTING_SCENE_ID
from game.game_session import create_game_session
from game.game_state import GameState
from game.ui.menu_screen import MenuScreen
from game.ui.resources import UIResources

pygame.font.init()


class DummySceneManager:
    """Scene manager double used for global app event tests."""

    def __init__(self) -> None:
        self.handled_events = 0
        self.current_scene_id = "first"
        self.transition_on_handle = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Record scene event handling and optionally transition."""
        del event
        self.handled_events += 1

        if self.transition_on_handle:
            self.current_scene_id = "second"

        return False


class DummySession:
    """Session double used for global app event tests."""

    def __init__(self) -> None:
        self.scene_manager = DummySceneManager()
        self.game_state = GameState()


class RecordingResources:
    """Small sound-only UI resource double."""

    def __init__(self) -> None:
        self.played_sound_ids: list[str | None] = []

    def play_sound(self, asset_id: str | None, *, volume: float = 0.55) -> None:
        del volume
        self.played_sound_ids.append(asset_id)


def create_menu_test_app() -> GameApp:
    """Create an app instance without opening a display window."""
    app = object.__new__(GameApp)
    app.screen = pygame.Surface((1280, 720))
    app.is_running = True
    app.ui_resources = UIResources()
    app.content = create_demo_content(app.ui_resources)
    app.session = create_game_session(app.content, app.ui_resources)
    app.mode = AppMode.TITLE
    app.title_screen = MenuScreen(
        title="Title",
        subtitle="Start the game.",
        primary_label="Start Game",
    )
    app.ending_screen = MenuScreen(
        title="Complete",
        subtitle="Play again.",
        primary_label="Play Again",
        overlay_gameplay=True,
    )
    return app


def test_app_new_game_event_replaces_session_before_scene_handling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = object.__new__(GameApp)
    old_session = DummySession()
    new_session = DummySession()
    reset_calls = 0

    def start_new_game() -> None:
        nonlocal reset_calls
        reset_calls += 1
        app.session = new_session

    app.is_running = True
    app.session = old_session
    app.start_new_game = start_new_game

    monkeypatch.setattr(
        pygame.event,
        "get",
        lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_n)],
    )

    app._handle_events()

    assert reset_calls == 1
    assert app.session is new_session
    assert old_session.scene_manager.handled_events == 0


def test_app_start_new_game_replaces_current_session() -> None:
    app = object.__new__(GameApp)
    app.content = create_demo_content()
    app.ui_resources = UIResources()
    app.session = create_game_session(app.content, app.ui_resources)
    app.mode = AppMode.ENDING
    old_session = app.session

    empty_cup = app.content.items_by_id[EMPTY_CUP]
    old_session.game_state.inventory.add(empty_cup)
    old_session.game_state.inventory.select(empty_cup.item_id)
    old_session.game_state.set_flag("temporary_flag")

    app.start_new_game()

    assert app.session is not old_session
    assert app.mode is AppMode.PLAYING
    assert app.session.scene_manager.current_scene_id == STARTING_SCENE_ID
    assert len(app.session.game_state.inventory) == 0
    assert app.session.game_state.inventory.selected_item is None
    assert not app.session.game_state.has_flag("temporary_flag")


def test_title_primary_action_starts_game(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_menu_test_app()
    old_session = app.session
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.PLAYING
    assert app.session is not old_session


def test_title_escape_quits(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_menu_test_app()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert not app.is_running


def test_ending_primary_action_starts_fresh_game(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.ENDING
    app.session.game_state.set_flag("completed_run")
    old_session = app.session
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.PLAYING
    assert app.session is not old_session
    assert not app.session.game_state.has_flag("completed_run")


def test_ending_menu_can_quit(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.ENDING
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN),
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: events)

    app._handle_events()

    assert not app.is_running


def test_gameplay_transition_plays_sound_and_opens_ending(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = object.__new__(GameApp)
    app.screen = pygame.Surface((1280, 720))
    app.is_running = True
    app.mode = AppMode.PLAYING
    app.session = DummySession()
    app.session.scene_manager.transition_on_handle = True
    app.session.game_state.mark_ending_reached()
    app.ui_resources = RecordingResources()
    app.ending_screen = MenuScreen(
        title="Complete",
        subtitle="Done.",
        primary_label="Play Again",
        overlay_gameplay=True,
    )
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0))
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.ENDING
    assert app.ui_resources.played_sound_ids == [SCENE_TRANSITION_SOUND]
