import pygame
import pytest

from game.content.demo_world import create_demo_content
from game.content.flag_ids import DEMO_COMPLETED, TOWER_UNLOCKED, WITCH_RECEIVED_TEA
from game.content.interaction_ids import OLD_WELL_INTERACTION
from game.content.item_ids import EMPTY_CUP
from game.content.pickup_ids import EMPTY_CUP_PICKUP, MOON_HERB_PICKUP
from game.content.scene_ids import STARTING_SCENE_ID
from game.game_session import create_game_session
from game.game_state import GameState
from game.ui.resources import UIResources

pygame.font.init()


def test_demo_content_exposes_static_registries() -> None:
    content = create_demo_content()

    assert content.starting_scene_id == STARTING_SCENE_ID
    assert EMPTY_CUP in content.items_by_id
    assert content.items_by_id[EMPTY_CUP].name == "Empty Cup"
    assert content.recipes == content.recipe_book.recipes
    assert STARTING_SCENE_ID in content.scenes_by_id
    assert content.flag_ids == frozenset(
        {
            DEMO_COMPLETED,
            TOWER_UNLOCKED,
            WITCH_RECEIVED_TEA,
        }
    )
    assert content.pickup_ids == frozenset(
        {
            EMPTY_CUP_PICKUP,
            MOON_HERB_PICKUP,
        }
    )
    assert content.interaction_ids == frozenset({OLD_WELL_INTERACTION})


def test_demo_content_registries_are_read_only() -> None:
    content = create_demo_content()

    with pytest.raises(TypeError):
        content.items_by_id["new_item"] = content.items_by_id[EMPTY_CUP]  # type: ignore[index]

    with pytest.raises(TypeError):
        content.scenes_by_id["new_scene"] = content.scenes_by_id[STARTING_SCENE_ID]  # type: ignore[index]


def test_two_sessions_share_content_without_sharing_state() -> None:
    content = create_demo_content()
    first_session = create_game_session(content, UIResources())
    second_session = create_game_session(content, UIResources())

    empty_cup = content.items_by_id[EMPTY_CUP]
    first_session.game_state.inventory.add(empty_cup)
    first_session.game_state.inventory.select(empty_cup.item_id)
    first_session.game_state.set_flag("temporary_flag")
    first_session.game_state.collect_pickup("temporary_pickup")
    first_session.game_state.complete_interaction("temporary_interaction")

    assert first_session.game_state.inventory.contains(EMPTY_CUP)
    assert first_session.game_state.inventory.selected_item == empty_cup
    assert first_session.game_state.has_flag("temporary_flag")
    assert first_session.game_state.has_collected_pickup("temporary_pickup")
    assert first_session.game_state.has_completed_interaction("temporary_interaction")

    assert not second_session.game_state.inventory.contains(EMPTY_CUP)
    assert second_session.game_state.inventory.selected_item is None
    assert not second_session.game_state.has_flag("temporary_flag")
    assert not second_session.game_state.has_collected_pickup("temporary_pickup")
    assert not second_session.game_state.has_completed_interaction("temporary_interaction")

    assert first_session.scene_manager.current_scene is not second_session.scene_manager.current_scene


def test_scenes_share_ui_resources_without_duplicate_font_construction() -> None:
    content = create_demo_content()
    resources = UIResources()

    scenes = content.build_scenes(GameState(), resources)
    scene_values = tuple(scenes.values())

    assert scene_values[0].body_font is resources.body_font
    assert scene_values[1].body_font is resources.body_font
    assert scene_values[0].body_font is scene_values[1].body_font
