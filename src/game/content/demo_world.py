from game.content.items import create_demo_items
from game.content.recipes import create_demo_recipe_book
from game.content.scene_ids import (
    FOREST_PATH,
    STARTING_SCENE_ID,
    TOWER_INTERIOR,
    VILLAGE_SQUARE,
)
from game.content.scenes.forest_path import create_forest_path
from game.content.scenes.tower_interior import create_tower_interior
from game.content.scenes.village_square import create_village_square
from game.content.validation import validate_content
from game.game_content import (
    GameContent,
    collect_content_id_registries,
    create_item_registry,
    create_scene_registry,
)
from game.game_state import GameState
from game.scenes.base_scene import BaseScene
from game.systems.recipe import RecipeBook
from game.ui.resources import UIResources


def create_demo_content(
    ui_resources: UIResources | None = None,
) -> GameContent:
    """Create and validate reusable content for the demo adventure."""
    base_content = _create_base_demo_content()
    validation_scenes = base_content.build_scenes(
        GameState(),
        ui_resources or UIResources(),
    )

    _validate_game_content(
        content=base_content,
        scenes=validation_scenes,
    )
    registries = collect_content_id_registries(validation_scenes)

    return GameContent(
        items_by_id=base_content.items_by_id,
        recipe_book=base_content.recipe_book,
        scenes_by_id=base_content.scenes_by_id,
        starting_scene_id=base_content.starting_scene_id,
        flag_ids=registries.flag_ids,
        pickup_ids=registries.pickup_ids,
        interaction_ids=registries.interaction_ids,
    )


def _create_base_demo_content(
    *,
    recipe_book: RecipeBook | None = None,
) -> GameContent:
    """Create demo content before validation registries are attached."""
    items_by_id = create_item_registry(create_demo_items())

    return GameContent(
        items_by_id=items_by_id,
        recipe_book=recipe_book or create_demo_recipe_book(items_by_id),
        scenes_by_id=create_scene_registry(
            {
                VILLAGE_SQUARE: create_village_square,
                FOREST_PATH: create_forest_path,
                TOWER_INTERIOR: create_tower_interior,
            }
        ),
        starting_scene_id=STARTING_SCENE_ID,
    )


def _validate_game_content(
    *,
    content: GameContent,
    scenes: dict[str, BaseScene],
) -> None:
    """Validate reusable content once before it is used by sessions."""
    validate_content(
        scene_entries=scenes.items(),
        starting_scene_id=content.starting_scene_id,
        items=content.items,
        recipes=content.recipe_book.recipes,
    )
