import pygame

from game.content.demo_world import create_demo_content
from game.content.flag_ids import (
    DEMO_COMPLETED,
    TOWER_UNLOCKED,
    WITCH_RECEIVED_TEA,
)
from game.content.interaction_ids import OLD_WELL_INTERACTION
from game.content.item_ids import (
    EMPTY_CUP,
    GLOWING_TEA,
    MOON_HERB,
    RUSTY_KEY,
    WATER_CUP,
)
from game.content.pickup_ids import EMPTY_CUP_PICKUP
from game.content.scene_ids import (
    FOREST_PATH,
    STARTING_SCENE_ID,
    TOWER_INTERIOR,
    VILLAGE_SQUARE,
)
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_session import GameSession, create_demo_game_session
from game.scenes.adventure_scene import AdventureScene
from game.ui.resources import UIResources

pygame.font.init()


def create_primary_click(position: tuple[int, int]) -> pygame.event.Event:
    """Create a primary mouse click event at a position."""
    return pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=position,
    )


def current_adventure_scene(session: GameSession) -> AdventureScene:
    """Return the session's current scene as an AdventureScene."""
    scene = session.scene_manager.current_scene

    assert isinstance(scene, AdventureScene)

    return scene


def find_pickup(scene: AdventureScene, item_id: str) -> ItemHotspot:
    """Find a pickup by item ID."""
    return next(
        pickup for pickup in scene.item_hotspots if pickup.item.item_id == item_id
    )


def find_hotspot(scene: AdventureScene, label: str) -> Hotspot:
    """Find a hotspot by label."""
    return next(hotspot for hotspot in scene.hotspots if hotspot.label == label)


def find_exit(scene: AdventureScene, target_scene_id: str) -> ExitHotspot:
    """Find an exit by its target scene ID."""
    return next(
        exit_hotspot
        for exit_hotspot in scene.exits
        if exit_hotspot.target_scene_id == target_scene_id
    )


def find_npc(scene: AdventureScene, name: str) -> NPC:
    """Find an NPC by name."""
    return next(npc for npc in scene.npcs if npc.name == name)


def inventory_item_position(
    scene: AdventureScene,
    item_id: str,
) -> tuple[int, int]:
    """Return the clickable inventory position for an item ID."""
    return next(
        row_rect.center
        for item, row_rect in scene.inventory_bar.layout_for_items(
            scene.game_state.inventory.items
        ).item_rows
        if item.item_id == item_id
    )


def click(session: GameSession, position: tuple[int, int]) -> None:
    """Send one primary click through the real scene manager."""
    assert session.scene_manager.handle_event(create_primary_click(position))


def fill_cup_at_well(session: GameSession) -> None:
    """Collect the Empty Cup and fill it at the Old Well."""
    village = current_adventure_scene(session)
    empty_cup_pickup = find_pickup(village, EMPTY_CUP)
    click(session, empty_cup_pickup.rect.center)

    old_well = find_hotspot(village, "Old Well")
    click(session, inventory_item_position(village, EMPTY_CUP))
    click(session, old_well.rect.center)

    assert session.game_state.inventory.contains(WATER_CUP)


def complete_demo(session: GameSession) -> None:
    """Complete the real demo flow in one session."""
    fill_cup_at_well(session)

    village = current_adventure_scene(session)
    click(session, find_exit(village, FOREST_PATH).rect.center)

    forest = current_adventure_scene(session)
    moon_herb_pickup = find_pickup(forest, MOON_HERB)
    click(session, moon_herb_pickup.rect.center)

    click(session, inventory_item_position(forest, WATER_CUP))
    click(session, inventory_item_position(forest, MOON_HERB))

    assert session.game_state.inventory.contains(GLOWING_TEA)

    click(session, find_exit(forest, VILLAGE_SQUARE).rect.center)

    village = current_adventure_scene(session)
    witch = find_npc(village, "Retired Witch")
    click(session, inventory_item_position(village, GLOWING_TEA))
    click(session, witch.rect.center)

    assert session.game_state.inventory.contains(RUSTY_KEY)
    assert session.game_state.has_flag(WITCH_RECEIVED_TEA)

    click(session, find_exit(village, FOREST_PATH).rect.center)

    forest = current_adventure_scene(session)
    tower_exit = find_exit(forest, TOWER_INTERIOR)
    click(session, inventory_item_position(forest, RUSTY_KEY))
    click(session, tower_exit.rect.center)

    assert session.game_state.has_flag(TOWER_UNLOCKED)

    click(session, tower_exit.rect.center)

    assert session.scene_manager.current_scene_id == TOWER_INTERIOR
    assert session.game_state.has_flag(DEMO_COMPLETED)
    assert session.game_state.ending_reached


def assert_fresh_session(session: GameSession) -> None:
    """Assert that a session starts from a clean beginning state."""
    game_state = session.game_state
    scene = current_adventure_scene(session)

    assert session.scene_manager.current_scene_id == STARTING_SCENE_ID
    assert len(game_state.inventory) == 0
    assert game_state.inventory.selected_item is None
    assert not game_state.has_flag(WITCH_RECEIVED_TEA)
    assert not game_state.has_flag(TOWER_UNLOCKED)
    assert not game_state.has_flag(DEMO_COMPLETED)
    assert not game_state.ending_reached
    assert not game_state.has_collected_pickup(EMPTY_CUP_PICKUP)
    assert not game_state.has_completed_interaction(OLD_WELL_INTERACTION)
    assert scene.interaction_text is None
    assert not scene.dialogue.is_active


def test_partially_progressed_game_can_reset_to_fresh_session() -> None:
    content = create_demo_content()
    session = create_demo_game_session(content, UIResources())
    fill_cup_at_well(session)

    village = current_adventure_scene(session)
    click(session, find_exit(village, FOREST_PATH).rect.center)

    forest = current_adventure_scene(session)
    tower_exit = find_exit(forest, TOWER_INTERIOR)
    click(session, tower_exit.rect.center)

    assert session.scene_manager.current_scene_id == FOREST_PATH
    assert session.game_state.has_collected_pickup(EMPTY_CUP_PICKUP)
    assert session.game_state.has_completed_interaction(OLD_WELL_INTERACTION)
    assert forest.interaction_text == tower_exit.locked_text

    mushroom_guard = find_npc(forest, "Mushroom Guard")
    click(session, mushroom_guard.rect.center)

    assert forest.dialogue.is_active

    reset_session = create_demo_game_session(content, UIResources())

    assert_fresh_session(reset_session)


def test_completed_game_can_reset_and_complete_again_in_same_process() -> None:
    content = create_demo_content()
    first_session = create_demo_game_session(content, UIResources())
    complete_demo(first_session)

    assert first_session.game_state.has_flag(DEMO_COMPLETED)

    second_session = create_demo_game_session(content, UIResources())

    assert_fresh_session(second_session)

    complete_demo(second_session)

    assert second_session.game_state.has_flag(DEMO_COMPLETED)


def test_two_sessions_do_not_leak_runtime_state() -> None:
    content = create_demo_content()
    first_session = create_demo_game_session(content, UIResources())
    second_session = create_demo_game_session(content, UIResources())

    fill_cup_at_well(first_session)

    assert first_session.game_state.inventory.contains(WATER_CUP)
    assert first_session.game_state.has_collected_pickup(EMPTY_CUP_PICKUP)
    assert first_session.game_state.has_completed_interaction(OLD_WELL_INTERACTION)

    assert_fresh_session(second_session)
