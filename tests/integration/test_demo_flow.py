import pygame

from game.content.demo_world import create_demo_content
from game.content.flag_ids import (
    DEMO_COMPLETED,
    TOWER_UNLOCKED,
    WITCH_RECEIVED_TEA,
)
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
    TOWER_INTERIOR,
    VILLAGE_SQUARE,
)
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_session import create_game_session
from game.scene_manager import SceneManager
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


def current_adventure_scene(manager: SceneManager) -> AdventureScene:
    """Return the manager's current scene as an AdventureScene."""
    scene = manager.current_scene

    assert isinstance(scene, AdventureScene)

    return scene


def find_pickup(scene: AdventureScene, item_id: str) -> ItemHotspot:
    """Find a real demo pickup by item ID."""
    return next(pickup for pickup in scene.item_hotspots if pickup.item.item_id == item_id)


def find_hotspot(scene: AdventureScene, label: str) -> Hotspot:
    """Find a real demo hotspot by label."""
    return next(hotspot for hotspot in scene.hotspots if hotspot.label == label)


def find_exit(
    scene: AdventureScene,
    target_scene_id: str,
) -> ExitHotspot:
    """Find a real demo exit by its destination."""
    return next(exit_hotspot for exit_hotspot in scene.exits if exit_hotspot.target_scene_id == target_scene_id)


def find_npc(scene: AdventureScene, name: str) -> NPC:
    """Find a real demo NPC by name."""
    return next(npc for npc in scene.npcs if npc.name == name)


def inventory_item_position(
    scene: AdventureScene,
    item_id: str,
) -> tuple[int, int]:
    """Return the clickable inventory position for an item ID."""
    return next(
        row_rect.center
        for item, row_rect in scene.inventory_bar.layout_for_items(scene.game_state.inventory.items).item_rows
        if item.item_id == item_id
    )


def click(manager: SceneManager, position: tuple[int, int]) -> None:
    """Send one primary click through the real scene manager."""
    assert manager.handle_event(create_primary_click(position))


def test_complete_key_based_demo_flow_uses_real_content() -> None:
    content = create_demo_content()
    session = create_game_session(content, UIResources())
    game_state = session.game_state
    manager = session.scene_manager

    assert manager.current_scene_id == VILLAGE_SQUARE

    village = current_adventure_scene(manager)
    empty_cup_pickup = find_pickup(village, EMPTY_CUP)
    click(manager, empty_cup_pickup.rect.center)

    assert game_state.inventory.contains(EMPTY_CUP)
    assert game_state.has_collected_pickup(EMPTY_CUP_PICKUP)

    old_well = find_hotspot(village, "Old Well")
    click(manager, inventory_item_position(village, EMPTY_CUP))
    click(manager, old_well.rect.center)

    assert not game_state.inventory.contains(EMPTY_CUP)
    assert game_state.inventory.contains(WATER_CUP)
    assert game_state.inventory.selected_item is None

    forest_exit = find_exit(village, FOREST_PATH)
    click(manager, forest_exit.rect.center)

    assert manager.current_scene_id == FOREST_PATH

    forest = current_adventure_scene(manager)
    tower_exit = find_exit(forest, TOWER_INTERIOR)
    click(manager, tower_exit.rect.center)

    assert manager.current_scene_id == FOREST_PATH
    assert forest.interaction_text == tower_exit.locked_text
    assert not game_state.has_flag(TOWER_UNLOCKED)
    assert not game_state.has_flag(DEMO_COMPLETED)

    moon_herb_pickup = find_pickup(forest, MOON_HERB)
    click(manager, moon_herb_pickup.rect.center)

    assert game_state.inventory.contains(MOON_HERB)

    click(manager, inventory_item_position(forest, WATER_CUP))
    click(manager, inventory_item_position(forest, MOON_HERB))

    assert not game_state.inventory.contains(WATER_CUP)
    assert not game_state.inventory.contains(MOON_HERB)
    assert game_state.inventory.contains(GLOWING_TEA)
    assert game_state.inventory.selected_item is None

    village_exit = find_exit(forest, VILLAGE_SQUARE)
    click(manager, village_exit.rect.center)

    assert manager.current_scene_id == VILLAGE_SQUARE

    village = current_adventure_scene(manager)
    assert game_state.has_collected_pickup(EMPTY_CUP_PICKUP)

    click(manager, inventory_item_position(village, GLOWING_TEA))
    witch = find_npc(village, "Retired Witch")
    click(manager, witch.rect.center)

    assert not game_state.inventory.contains(GLOWING_TEA)
    assert game_state.inventory.contains(RUSTY_KEY)
    assert game_state.inventory.selected_item is None
    assert game_state.has_flag(WITCH_RECEIVED_TEA)
    assert not game_state.has_flag(TOWER_UNLOCKED)

    forest_exit = find_exit(village, FOREST_PATH)
    click(manager, forest_exit.rect.center)

    forest = current_adventure_scene(manager)
    tower_exit = find_exit(forest, TOWER_INTERIOR)
    click(manager, inventory_item_position(forest, RUSTY_KEY))
    click(manager, tower_exit.rect.center)

    assert manager.current_scene_id == FOREST_PATH
    assert not game_state.inventory.contains(RUSTY_KEY)
    assert game_state.inventory.selected_item is None
    assert game_state.has_flag(TOWER_UNLOCKED)
    assert not game_state.has_flag(DEMO_COMPLETED)

    click(manager, tower_exit.rect.center)

    assert manager.current_scene_id == TOWER_INTERIOR
    assert game_state.has_flag(DEMO_COMPLETED)
    assert game_state.ending_reached
