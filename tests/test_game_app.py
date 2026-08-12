from pathlib import Path

import pygame
import pytest

import game.app as app_module
from game.app import AppMode, GameApp
from game.asset_ids import SCENE_TRANSITION_SOUND
from game.content.demo_world import create_demo_content
from game.content.flag_ids import DEMO_COMPLETED, TOWER_UNLOCKED, WITCH_RECEIVED_TEA
from game.content.interaction_ids import OLD_WELL_INTERACTION
from game.content.item_ids import EMPTY_CUP, MOON_HERB, WATER_CUP
from game.content.pickup_ids import EMPTY_CUP_PICKUP, MOON_HERB_PICKUP
from game.content.scene_ids import FOREST_PATH, STARTING_SCENE_ID, TOWER_INTERIOR
from game.display import DisplayViewport
from game.game_session import GameSession, create_game_session
from game.game_state import GameState
from game.save_file import (
    SaveFileInspection,
    SaveFileStatus,
    create_save_file_envelope,
    write_save_file,
)
from game.scenes.adventure_scene import AdventureScene
from game.settings import LOGICAL_SIZE
from game.state_snapshot import create_state_snapshot
from game.ui.controls_screen import ControlsScreen
from game.ui.menu_screen import MenuScreen
from game.ui.resources import UIResources

pygame.font.init()


class DummySceneManager:
    """Scene manager double used for global app event tests."""

    def __init__(self) -> None:
        self.handled_events = 0
        self.handled_event_positions: list[tuple[int, int] | None] = []
        self.current_scene_id = "first"
        self.transition_on_handle = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Record scene event handling and optionally transition."""
        self.handled_events += 1
        self.handled_event_positions.append(getattr(event, "pos", None))

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
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface(LOGICAL_SIZE))
    app.is_running = True
    app.ui_resources = UIResources()
    app.content = create_demo_content(app.ui_resources)
    app.session = create_game_session(app.content, app.ui_resources)
    app.mode = AppMode.TITLE
    app.title_screen = MenuScreen(
        title="Title",
        subtitle="Start the game.",
        primary_label="Start Game",
        secondary_label="Controls",
    )
    app.controls_screen = ControlsScreen()
    app.controls_return_mode = AppMode.TITLE
    app.ending_screen = MenuScreen(
        title="Complete",
        subtitle="Play again.",
        primary_label="Play Again",
        overlay_gameplay=True,
    )
    return app


def current_adventure_scene(session: GameSession) -> AdventureScene:
    """Return the current real gameplay scene for load-state assertions."""
    scene = session.scene_manager.current_scene

    assert isinstance(scene, AdventureScene)
    return scene


def write_session_save(path: Path, session: GameSession) -> None:
    """Write one valid manual save for application-level load tests."""
    envelope = create_save_file_envelope(create_state_snapshot(session))
    result = write_save_file(path=path, envelope=envelope)

    assert result.is_success


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
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface(LOGICAL_SIZE))
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


def test_title_controls_action_opens_reusable_controls_screen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_menu_test_app()
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN),
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: events)

    app._handle_events()

    assert app.mode is AppMode.CONTROLS
    assert app.controls_return_mode is AppMode.TITLE


def test_controls_escape_returns_to_opening_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.CONTROLS
    app.controls_return_mode = AppMode.TITLE
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.TITLE
    assert app.is_running


def test_controls_back_click_returns_to_opening_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.CONTROLS
    app.controls_return_mode = AppMode.TITLE
    back_rect = app.controls_screen.back_button_rect(LOGICAL_SIZE)
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=back_rect.center,
    )
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.TITLE
    assert app.is_running


def test_global_new_game_action_still_works_from_controls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.CONTROLS
    old_session = app.session
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_n)
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
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface(LOGICAL_SIZE))
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


def test_scaled_title_mouse_click_is_converted_before_menu_hit_testing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_menu_test_app()
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface((1600, 900)))
    old_session = app.session
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(800, 528),
    )
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.PLAYING
    assert app.session is not old_session


def test_letterbox_click_does_not_activate_title_menu(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_menu_test_app()
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface((1000, 1000)))
    old_session = app.session
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(500, 100),
    )
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.mode is AppMode.TITLE
    assert app.session is old_session
    assert app.is_running


def test_gameplay_receives_logical_pointer_coordinates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = object.__new__(GameApp)
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface((1600, 900)))
    app.is_running = True
    app.mode = AppMode.PLAYING
    app.session = DummySession()
    app.ui_resources = RecordingResources()
    app.ending_screen = MenuScreen(
        title="Complete",
        subtitle="Done.",
        primary_label="Play Again",
        overlay_gameplay=True,
    )
    event = pygame.event.Event(
        pygame.MOUSEMOTION,
        pos=(800, 450),
        rel=(0, 0),
        buttons=(0, 0, 0),
    )
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.session.scene_manager.handled_event_positions == [(640, 360)]


def test_gameplay_receives_non_interactive_pointer_outside_frame(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = object.__new__(GameApp)
    app.viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface((1000, 1000)))
    app.is_running = True
    app.mode = AppMode.PLAYING
    app.session = DummySession()
    app.ui_resources = RecordingResources()
    app.ending_screen = MenuScreen(
        title="Complete",
        subtitle="Done.",
        primary_label="Play Again",
        overlay_gameplay=True,
    )
    event = pygame.event.Event(
        pygame.MOUSEMOTION,
        pos=(500, 100),
        rel=(0, 0),
        buttons=(0, 0, 0),
    )
    monkeypatch.setattr(pygame.event, "get", lambda: [event])

    app._handle_events()

    assert app.session.scene_manager.handled_event_positions == [None]


def test_load_fresh_save_replaces_session_and_resets_local_navigation_state(
    tmp_path: Path,
) -> None:
    app = create_menu_test_app()
    saved_session = create_game_session(app.content, app.ui_resources)
    save_path = tmp_path / "save.json"
    write_session_save(save_path, saved_session)
    old_session = app.session

    app.mode = AppMode.CONTROLS
    app.title_screen.selected_index = 2
    app.controls_screen.back_selected = False
    app.controls_return_mode = AppMode.ENDING
    app.ending_screen.selected_index = 1

    status = app.load_session_from_save(save_path)

    assert status is SaveFileStatus.VALID
    assert app.session is not old_session
    assert app.mode is AppMode.PLAYING
    assert create_state_snapshot(app.session) == create_state_snapshot(saved_session)
    assert app.title_screen.selected_index == 0
    assert app.controls_screen.back_selected
    assert app.controls_return_mode is AppMode.TITLE
    assert app.ending_screen.selected_index == 0


def test_load_mid_quest_save_preserves_persistent_state(tmp_path: Path) -> None:
    app = create_menu_test_app()
    saved_session = create_game_session(app.content, app.ui_resources)
    saved_session.game_state.inventory.add(app.content.items_by_id[WATER_CUP])
    saved_session.game_state.collect_pickup(EMPTY_CUP_PICKUP)
    saved_session.game_state.complete_interaction(OLD_WELL_INTERACTION)
    saved_session.scene_manager.change_scene(FOREST_PATH)
    save_path = tmp_path / "save.json"
    expected_snapshot = create_state_snapshot(saved_session)
    write_session_save(save_path, saved_session)

    status = app.load_session_from_save(save_path)

    assert status is SaveFileStatus.VALID
    assert app.mode is AppMode.PLAYING
    assert create_state_snapshot(app.session) == expected_snapshot


def test_load_selected_item_save_preserves_inventory_order_and_selection(
    tmp_path: Path,
) -> None:
    app = create_menu_test_app()
    saved_session = create_game_session(app.content, app.ui_resources)
    saved_session.game_state.inventory.add(app.content.items_by_id[EMPTY_CUP])
    saved_session.game_state.inventory.add(app.content.items_by_id[MOON_HERB])
    saved_session.game_state.inventory.select(MOON_HERB)
    save_path = tmp_path / "save.json"
    write_session_save(save_path, saved_session)

    status = app.load_session_from_save(save_path)

    assert status is SaveFileStatus.VALID
    assert app.session.game_state.inventory.item_ids == (EMPTY_CUP, MOON_HERB)
    assert app.session.game_state.inventory.selected_item_id == MOON_HERB


def test_load_changed_scene_save_builds_fresh_scene_presentation_state(
    tmp_path: Path,
) -> None:
    app = create_menu_test_app()
    saved_session = create_game_session(app.content, app.ui_resources)
    saved_session.scene_manager.change_scene(FOREST_PATH)
    saved_scene = current_adventure_scene(saved_session)
    saved_scene.interaction_text = "Stale interaction text."
    saved_scene.active_speaker_name = "Stale speaker"
    saved_scene.pointer_position = (321, 123)
    saved_scene.dialogue.start(("Stale dialogue.",))
    save_path = tmp_path / "save.json"
    write_session_save(save_path, saved_session)

    status = app.load_session_from_save(save_path)
    restored_scene = current_adventure_scene(app.session)

    assert status is SaveFileStatus.VALID
    assert app.mode is AppMode.PLAYING
    assert app.session.scene_manager.current_scene_id == FOREST_PATH
    assert restored_scene is not saved_scene
    assert restored_scene.interaction_text is None
    assert restored_scene.active_speaker_name == ""
    assert restored_scene.pointer_position is None
    assert not restored_scene.dialogue.is_active


def test_load_completed_save_enters_ending_with_complete_persistent_state(
    tmp_path: Path,
) -> None:
    app = create_menu_test_app()
    saved_session = create_game_session(app.content, app.ui_resources)
    saved_session.scene_manager.change_scene(TOWER_INTERIOR)
    saved_session.game_state.set_flag(WITCH_RECEIVED_TEA)
    saved_session.game_state.set_flag(TOWER_UNLOCKED)
    saved_session.game_state.set_flag(DEMO_COMPLETED)
    saved_session.game_state.collect_pickup(EMPTY_CUP_PICKUP)
    saved_session.game_state.collect_pickup(MOON_HERB_PICKUP)
    saved_session.game_state.complete_interaction(OLD_WELL_INTERACTION)
    saved_session.game_state.mark_ending_reached()
    save_path = tmp_path / "save.json"
    expected_snapshot = create_state_snapshot(saved_session)
    write_session_save(save_path, saved_session)

    status = app.load_session_from_save(save_path)

    assert status is SaveFileStatus.VALID
    assert app.mode is AppMode.ENDING
    assert create_state_snapshot(app.session) == expected_snapshot


def test_invalid_json_load_keeps_previous_session_and_mode(tmp_path: Path) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.ENDING
    old_session = app.session
    save_path = tmp_path / "save.json"
    save_path.write_text("{not valid json", encoding="utf-8")

    status = app.load_session_from_save(save_path)

    assert status is SaveFileStatus.INVALID_JSON
    assert app.session is old_session
    assert app.mode is AppMode.ENDING


@pytest.mark.parametrize(
    "status",
    [
        SaveFileStatus.MISSING,
        SaveFileStatus.INVALID_JSON,
        SaveFileStatus.INVALID_ENVELOPE,
        SaveFileStatus.UNSUPPORTED_FILE_VERSION,
        SaveFileStatus.INVALID_SNAPSHOT,
        SaveFileStatus.UNREADABLE_FILE,
    ],
)
def test_failed_load_status_keeps_previous_session_and_mode(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    status: SaveFileStatus,
) -> None:
    app = create_menu_test_app()
    app.mode = AppMode.CONTROLS
    old_session = app.session

    monkeypatch.setattr(
        app_module,
        "inspect_save_file",
        lambda **kwargs: SaveFileInspection(status),
    )

    result = app.load_session_from_save(tmp_path / "save.json")

    assert result is status
    assert app.session is old_session
    assert app.mode is AppMode.CONTROLS


def test_restore_failure_keeps_previous_session_and_mode(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    app = create_menu_test_app()
    saved_session = create_game_session(app.content, app.ui_resources)
    save_path = tmp_path / "save.json"
    write_session_save(save_path, saved_session)
    app.mode = AppMode.TITLE
    old_session = app.session

    def fail_restore(**kwargs: object) -> GameSession:
        del kwargs
        raise RuntimeError("restoration failed")

    monkeypatch.setattr(app_module, "restore_session_from_snapshot", fail_restore)

    with pytest.raises(RuntimeError, match="restoration failed"):
        app.load_session_from_save(save_path)

    assert app.session is old_session
    assert app.mode is AppMode.TITLE
