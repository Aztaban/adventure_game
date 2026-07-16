import pygame

from game.content.demo_world import create_demo_content
from game.content.interaction_ids import OLD_WELL_INTERACTION
from game.content.item_ids import EMPTY_CUP, WATER_CUP
from game.content.pickup_ids import EMPTY_CUP_PICKUP
from game.content.scenes.village_square import create_village_square
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.game_state import GameState
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


def find_pickup(scene: AdventureScene, item_id: str) -> ItemHotspot:
    """Find a pickup definition by its item ID."""
    return next(
        pickup
        for pickup in scene.item_hotspots
        if pickup.item.item_id == item_id
    )


def find_hotspot(scene: AdventureScene, label: str) -> Hotspot:
    """Find a hotspot definition by its label."""
    return next(
        hotspot
        for hotspot in scene.hotspots
        if hotspot.label == label
    )


def test_recreated_scene_hides_already_collected_pickup() -> None:
    game_state = GameState()
    ui_resources = UIResources()
    content = create_demo_content(ui_resources)
    first_scene = create_village_square(
        game_state,
        content.recipe_book,
        content.items_by_id,
        ui_resources,
    )
    empty_cup_pickup = find_pickup(first_scene, EMPTY_CUP)

    first_result = first_scene.handle_event(
        create_primary_click(empty_cup_pickup.rect.center)
    )

    recreated_scene = create_village_square(
        game_state,
        content.recipe_book,
        content.items_by_id,
        ui_resources,
    )
    recreated_pickup = find_pickup(recreated_scene, EMPTY_CUP)
    second_result = recreated_scene.handle_event(
        create_primary_click(recreated_pickup.rect.center)
    )

    assert first_result.consumed
    assert game_state.has_collected_pickup(EMPTY_CUP_PICKUP)
    assert not second_result.consumed
    assert len(game_state.inventory) == 1


def test_completed_interaction_survives_scene_reconstruction() -> None:
    game_state = GameState()
    ui_resources = UIResources()
    content = create_demo_content(ui_resources)
    first_scene = create_village_square(
        game_state,
        content.recipe_book,
        content.items_by_id,
        ui_resources,
    )
    empty_cup_pickup = find_pickup(first_scene, EMPTY_CUP)
    old_well = find_hotspot(first_scene, "Old Well")

    first_scene.handle_event(create_primary_click(empty_cup_pickup.rect.center))
    game_state.inventory.select(EMPTY_CUP)
    first_scene.handle_event(create_primary_click(old_well.rect.center))

    assert game_state.has_completed_interaction(OLD_WELL_INTERACTION)
    assert not game_state.inventory.contains(EMPTY_CUP)
    assert game_state.inventory.contains(WATER_CUP)

    recreated_scene = create_village_square(
        game_state,
        content.recipe_book,
        content.items_by_id,
        ui_resources,
    )
    recreated_well = find_hotspot(recreated_scene, "Old Well")
    result = recreated_scene.handle_event(
        create_primary_click(recreated_well.rect.center)
    )

    assert result.consumed
    assert recreated_scene.interaction_text == (
        "The well is now pretending it cannot hear you."
    )
