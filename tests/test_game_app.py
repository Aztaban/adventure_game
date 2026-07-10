import pygame
import pytest

from game.app import GameApp
from game.content.demo_world import create_demo_content
from game.content.item_ids import EMPTY_CUP
from game.content.scene_ids import STARTING_SCENE_ID
from game.game_session import create_demo_game_session

pygame.font.init()


class DummySceneManager:
    """Scene manager double used for global app event tests."""

    def __init__(self) -> None:
        self.handled_events = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Record scene event handling."""
        del event
        self.handled_events += 1

        return False


class DummySession:
    """Session double used for global app event tests."""

    def __init__(self) -> None:
        self.scene_manager = DummySceneManager()


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
    app.session = create_demo_game_session(app.content)
    old_session = app.session

    empty_cup = app.content.items_by_id[EMPTY_CUP]
    old_session.game_state.inventory.add(empty_cup)
    old_session.game_state.inventory.select(empty_cup.item_id)
    old_session.game_state.set_flag("temporary_flag")

    app.start_new_game()

    assert app.session is not old_session
    assert app.session.scene_manager.current_scene_id == STARTING_SCENE_ID
    assert len(app.session.game_state.inventory) == 0
    assert app.session.game_state.inventory.selected_item is None
    assert not app.session.game_state.has_flag("temporary_flag")
