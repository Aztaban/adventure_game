import pygame
import pytest

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
from game.content.pickup_ids import EMPTY_CUP_PICKUP, MOON_HERB_PICKUP
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
from game.game_session import GameSession, create_game_session
from game.scenes.adventure_scene import AdventureScene
from game.state_snapshot import (
    SAVE_DATA_VERSION,
    SnapshotValidationError,
    create_state_snapshot,
    restore_session_from_snapshot,
)
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


def test_fresh_state_snapshot_round_trip() -> None:
    content = create_demo_content()
    session = create_game_session(content, UIResources())

    snapshot = create_state_snapshot(session)
    restored_session = restore_session_from_snapshot(
        content=content,
        snapshot=snapshot,
        ui_resources=UIResources(),
    )

    assert snapshot == {
        "save_version": SAVE_DATA_VERSION,
        "current_scene_id": STARTING_SCENE_ID,
        "inventory_item_ids": [],
        "selected_item_id": None,
        "flags": [],
        "collected_pickup_ids": [],
        "completed_interaction_ids": [],
        "ending_reached": False,
    }
    assert create_state_snapshot(restored_session) == snapshot


def test_mid_quest_state_snapshot_round_trip() -> None:
    content = create_demo_content()
    session = create_game_session(content, UIResources())
    fill_cup_at_well(session)

    village = current_adventure_scene(session)
    click(session, find_exit(village, FOREST_PATH).rect.center)

    snapshot = create_state_snapshot(session)
    restored_session = restore_session_from_snapshot(
        content=content,
        snapshot=snapshot,
        ui_resources=UIResources(),
    )

    assert snapshot["current_scene_id"] == FOREST_PATH
    assert snapshot["inventory_item_ids"] == [WATER_CUP]
    assert snapshot["collected_pickup_ids"] == [EMPTY_CUP_PICKUP]
    assert snapshot["completed_interaction_ids"] == [OLD_WELL_INTERACTION]
    assert snapshot["ending_reached"] is False
    assert create_state_snapshot(restored_session) == snapshot

    restored_forest = current_adventure_scene(restored_session)
    assert restored_session.scene_manager.current_scene_id == FOREST_PATH
    assert restored_session.game_state.inventory.contains(WATER_CUP)
    assert restored_session.game_state.has_collected_pickup(EMPTY_CUP_PICKUP)
    assert restored_session.game_state.has_completed_interaction(OLD_WELL_INTERACTION)
    assert not restored_session.game_state.ending_reached
    assert find_pickup(restored_forest, MOON_HERB).pickup_id == MOON_HERB_PICKUP


def test_completed_demo_state_snapshot_round_trip() -> None:
    content = create_demo_content()
    session = create_game_session(content, UIResources())
    complete_demo(session)

    snapshot = create_state_snapshot(session)
    restored_session = restore_session_from_snapshot(
        content=content,
        snapshot=snapshot,
        ui_resources=UIResources(),
    )

    assert snapshot["current_scene_id"] == TOWER_INTERIOR
    assert snapshot["inventory_item_ids"] == []
    assert snapshot["selected_item_id"] is None
    assert snapshot["flags"] == [
        DEMO_COMPLETED,
        TOWER_UNLOCKED,
        WITCH_RECEIVED_TEA,
    ]
    assert snapshot["collected_pickup_ids"] == [
        MOON_HERB_PICKUP,
        EMPTY_CUP_PICKUP,
    ]
    assert snapshot["completed_interaction_ids"] == [OLD_WELL_INTERACTION]
    assert snapshot["ending_reached"] is True
    assert create_state_snapshot(restored_session) == snapshot
    assert restored_session.game_state.has_flag(DEMO_COMPLETED)
    assert restored_session.game_state.ending_reached


def test_selected_item_snapshot_round_trip() -> None:
    content = create_demo_content()
    session = create_game_session(content, UIResources())
    village = current_adventure_scene(session)
    empty_cup_pickup = find_pickup(village, EMPTY_CUP)
    click(session, empty_cup_pickup.rect.center)
    click(session, inventory_item_position(village, EMPTY_CUP))

    snapshot = create_state_snapshot(session)
    restored_session = restore_session_from_snapshot(
        content=content,
        snapshot=snapshot,
        ui_resources=UIResources(),
    )

    assert snapshot["inventory_item_ids"] == [EMPTY_CUP]
    assert snapshot["selected_item_id"] == EMPTY_CUP
    assert create_state_snapshot(restored_session) == snapshot
    assert restored_session.game_state.inventory.selected_item_id == EMPTY_CUP


def test_snapshot_with_unknown_scene_id_fails_clearly() -> None:
    content = create_demo_content()
    snapshot = create_state_snapshot(create_game_session(content, UIResources()))
    snapshot["current_scene_id"] = "missing_scene"

    with pytest.raises(
        SnapshotValidationError,
        match="Unknown scene ID 'missing_scene'",
    ):
        restore_session_from_snapshot(
            content=content,
            snapshot=snapshot,
            ui_resources=UIResources(),
        )


def test_snapshot_with_unknown_item_id_fails_clearly() -> None:
    content = create_demo_content()
    snapshot = create_state_snapshot(create_game_session(content, UIResources()))
    snapshot["inventory_item_ids"] = ["missing_item"]

    with pytest.raises(
        SnapshotValidationError,
        match="Unknown inventory item ID 'missing_item'",
    ):
        restore_session_from_snapshot(
            content=content,
            snapshot=snapshot,
            ui_resources=UIResources(),
        )


def test_snapshot_with_unknown_interaction_id_fails_clearly() -> None:
    content = create_demo_content()
    snapshot = create_state_snapshot(create_game_session(content, UIResources()))
    snapshot["completed_interaction_ids"] = ["missing_interaction"]

    with pytest.raises(
        SnapshotValidationError,
        match="Unknown completed interaction ID 'missing_interaction'",
    ):
        restore_session_from_snapshot(
            content=content,
            snapshot=snapshot,
            ui_resources=UIResources(),
        )


def test_snapshot_with_unknown_flag_id_fails_clearly() -> None:
    content = create_demo_content()
    snapshot = create_state_snapshot(create_game_session(content, UIResources()))
    snapshot["flags"] = ["missing_flag"]

    with pytest.raises(
        SnapshotValidationError,
        match="Unknown flag ID 'missing_flag'",
    ):
        restore_session_from_snapshot(
            content=content,
            snapshot=snapshot,
            ui_resources=UIResources(),
        )


def test_snapshot_with_selected_item_not_in_inventory_fails_clearly() -> None:
    content = create_demo_content()
    snapshot = create_state_snapshot(create_game_session(content, UIResources()))
    snapshot["selected_item_id"] = EMPTY_CUP

    with pytest.raises(
        SnapshotValidationError,
        match="Selected item ID 'empty_cup' is not present",
    ):
        restore_session_from_snapshot(
            content=content,
            snapshot=snapshot,
            ui_resources=UIResources(),
        )
