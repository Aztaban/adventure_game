import pygame
import pytest

from game.content.demo_world import create_demo_scenes
from game.content.item_ids import EMPTY_CUP, MOON_HERB
from game.content.items import (
    create_demo_items,
    create_empty_cup,
    create_glowing_tea,
)
from game.content.recipes import create_demo_recipe_book
from game.content.scene_ids import (
    FOREST_PATH,
    STARTING_SCENE_ID,
    VILLAGE_SQUARE,
)
from game.content.validation import (
    ContentValidationError,
    StableContentId,
    validate_content,
)
from game.entities.item import Item
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.systems.recipe import Recipe

pygame.font.init()


def create_valid_demo_content() -> tuple[
    dict[str, AdventureScene],
    GameState,
]:
    """Create the real demo content used by validation tests."""
    game_state = GameState(recipe_book=create_demo_recipe_book())
    scenes = create_demo_scenes(game_state)

    return scenes, game_state


def validate_demo_content(
    scenes: dict[str, AdventureScene],
    game_state: GameState,
    *,
    starting_scene_id: str = STARTING_SCENE_ID,
    stable_ids: tuple[StableContentId, ...] = (),
) -> None:
    """Validate real demo objects with optional test overrides."""
    validate_content(
        scene_entries=scenes.items(),
        starting_scene_id=starting_scene_id,
        items=create_demo_items(),
        recipes=game_state.recipe_book.recipes,
        stable_ids=stable_ids,
    )


def test_valid_demo_content_passes_validation() -> None:
    scenes, game_state = create_valid_demo_content()

    validate_demo_content(scenes, game_state)


def test_unknown_starting_scene_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()

    with pytest.raises(
        ContentValidationError,
        match="Starting scene ID 'missing_scene' does not exist",
    ):
        validate_demo_content(
            scenes,
            game_state,
            starting_scene_id="missing_scene",
        )


def test_duplicate_scene_id_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()
    scene_entries = [
        *scenes.items(),
        (VILLAGE_SQUARE, scenes[VILLAGE_SQUARE]),
    ]

    with pytest.raises(
        ContentValidationError,
        match="Duplicate scene ID 'village_square'",
    ):
        validate_content(
            scene_entries=scene_entries,
            starting_scene_id=STARTING_SCENE_ID,
            items=create_demo_items(),
            recipes=game_state.recipe_book.recipes,
        )


def test_unknown_exit_target_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()
    forest = scenes[FOREST_PATH]
    forest.exits[0].target_scene_id = "missing_scene"

    with pytest.raises(
        ContentValidationError,
        match=("Scene 'forest_path' exit 'To Village' targets unknown scene ID 'missing_scene'"),
    ):
        validate_demo_content(scenes, game_state)


def test_duplicate_item_id_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()

    with pytest.raises(
        ContentValidationError,
        match="Duplicate item ID 'empty_cup'",
    ):
        validate_content(
            scene_entries=scenes.items(),
            starting_scene_id=STARTING_SCENE_ID,
            items=(*create_demo_items(), create_empty_cup()),
            recipes=game_state.recipe_book.recipes,
        )


def test_unknown_pickup_item_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()
    village = scenes[VILLAGE_SQUARE]
    village.item_hotspots[0].item = Item(
        item_id="missing_pickup_item",
        name="Missing Pickup",
        description="Not part of the item catalog.",
    )

    with pytest.raises(
        ContentValidationError,
        match=("Scene 'village_square' pickup 'Missing Pickup' references unknown item ID 'missing_pickup_item'"),
    ):
        validate_demo_content(scenes, game_state)


def test_unknown_recipe_ingredient_fails_clearly() -> None:
    scenes, _ = create_valid_demo_content()
    invalid_recipe = Recipe(
        first_item_id="missing_ingredient",
        second_item_id=MOON_HERB,
        result_item=create_glowing_tea(),
        success_text="Invalid recipe.",
    )

    with pytest.raises(
        ContentValidationError,
        match=(
            r"Recipe 'missing_ingredient \+ moon_herb -> glowing_tea' "
            "references unknown ingredient item ID 'missing_ingredient'"
        ),
    ):
        validate_content(
            scene_entries=scenes.items(),
            starting_scene_id=STARTING_SCENE_ID,
            items=create_demo_items(),
            recipes=(invalid_recipe,),
        )


def test_unknown_recipe_result_fails_clearly() -> None:
    scenes, _ = create_valid_demo_content()
    invalid_recipe = Recipe(
        first_item_id=EMPTY_CUP,
        second_item_id=MOON_HERB,
        result_item=Item(
            item_id="missing_result",
            name="Missing Result",
            description="Not part of the item catalog.",
        ),
        success_text="Invalid recipe.",
    )

    with pytest.raises(
        ContentValidationError,
        match=(
            r"Recipe 'empty_cup \+ moon_herb -> missing_result' "
            "references unknown result item ID 'missing_result'"
        ),
    ):
        validate_content(
            scene_entries=scenes.items(),
            starting_scene_id=STARTING_SCENE_ID,
            items=create_demo_items(),
            recipes=(invalid_recipe,),
        )


def test_unknown_required_item_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()
    village = scenes[VILLAGE_SQUARE]
    old_well = next(hotspot for hotspot in village.hotspots if hotspot.label == "Old Well")
    assert old_well.item_use is not None
    old_well.item_use.required_item_id = "missing_required_item"

    with pytest.raises(
        ContentValidationError,
        match=("Scene 'village_square' hotspot 'Old Well' requires unknown item ID 'missing_required_item'"),
    ):
        validate_demo_content(scenes, game_state)


def test_duplicate_stable_id_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()

    with pytest.raises(
        ContentValidationError,
        match=("Duplicate stable ID 'shared_id' used by 'Village Square pickup' and 'Forest Path interaction'"),
    ):
        validate_demo_content(
            scenes,
            game_state,
            stable_ids=(
                StableContentId(
                    value="shared_id",
                    owner="Village Square pickup",
                ),
                StableContentId(
                    value="shared_id",
                    owner="Forest Path interaction",
                ),
            ),
        )


def test_duplicate_pickup_id_fails_clearly() -> None:
    scenes, game_state = create_valid_demo_content()
    village_pickup = scenes[VILLAGE_SQUARE].item_hotspots[0]
    forest_pickup = scenes[FOREST_PATH].item_hotspots[0]
    forest_pickup.pickup_id = village_pickup.pickup_id

    with pytest.raises(
        ContentValidationError,
        match=(
            "Duplicate stable ID 'pickup.village.empty_cup' used by "
            "'Scene 'village_square' pickup 'Empty Cup'' and "
            "'Scene 'forest_path' pickup 'Moon Herb''"
        ),
    ):
        validate_demo_content(scenes, game_state)
