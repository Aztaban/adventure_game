import pygame

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene

pygame.font.init()


def create_test_scene(
    game_state: GameState,
    exits: list[ExitHotspot] | None = None,
    hotspots: list[Hotspot] | None = None,
    npcs: list[NPC] | None = None,
) -> AdventureScene:
    """Create a minimal scene for quest-flag tests."""
    return AdventureScene(
        name="Test Scene",
        description="A test scene.",
        background_color=(0, 0, 0),
        exits=exits or [],
        hotspots=hotspots or [],
        item_hotspots=[],
        npcs=npcs or [],
        game_state=game_state,
    )


def create_click(
    position: tuple[int, int],
) -> pygame.event.Event:
    """Create a primary mouse click event."""
    return pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=position,
    )


def test_locked_exit_blocks_without_required_flag() -> None:
    game_state = GameState()
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(100, 100, 150, 100),
        target_scene_id="target",
        label="Enter",
        required_flag="door_unlocked",
        locked_text="The door is locked.",
    )
    scene = create_test_scene(
        game_state,
        exits=[exit_hotspot],
    )

    result = scene.handle_event(create_click((110, 110)))

    assert result.consumed
    assert result.target_scene_id is None
    assert scene.interaction_text == "The door is locked."


def test_unlocked_exit_changes_scene_and_sets_completion_flag() -> None:
    game_state = GameState()
    game_state.set_flag("door_unlocked")

    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(100, 100, 150, 100),
        target_scene_id="target",
        label="Enter",
        required_flag="door_unlocked",
        completion_flag="demo_completed",
    )
    scene = create_test_scene(
        game_state,
        exits=[exit_hotspot],
    )

    result = scene.handle_event(create_click((110, 110)))

    assert result.consumed
    assert result.target_scene_id == "target"
    assert game_state.has_flag("demo_completed")


def test_hotspot_inspection_reacts_to_flag() -> None:
    game_state = GameState()
    game_state.set_flag("world_changed")

    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 150, 100),
        label="Object",
        inspect_text="Before text.",
        inspect_flag="world_changed",
        flagged_inspect_text="After text.",
    )
    scene = create_test_scene(
        game_state,
        hotspots=[hotspot],
    )

    scene.handle_event(create_click((110, 110)))

    assert scene.interaction_text == "After text."


def test_npc_dialogue_reacts_to_flag() -> None:
    game_state = GameState()
    game_state.set_flag("quest_finished")

    npc = NPC(
        rect=pygame.Rect(100, 100, 150, 100),
        name="Test NPC",
        dialogue_lines=("Before dialogue.",),
        dialogue_flag="quest_finished",
        flagged_dialogue_lines=("After dialogue.",),
    )
    scene = create_test_scene(
        game_state,
        npcs=[npc],
    )

    scene.handle_event(create_click((110, 110)))

    assert scene.dialogue.current_line == "After dialogue."
