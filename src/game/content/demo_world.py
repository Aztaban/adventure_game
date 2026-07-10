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
    create_item_registry,
    create_scene_registry,
)
from game.game_state import GameState
from game.scenes.base_scene import BaseScene
from game.systems.recipe import RecipeBook


def create_demo_content() -> GameContent:
    """Create and validate reusable content for the demo adventure."""
    content = GameContent(
        items_by_id=create_item_registry(create_demo_items()),
        recipe_book=create_demo_recipe_book(),
        scenes_by_id=create_scene_registry(
            {
                VILLAGE_SQUARE: create_village_square,
                FOREST_PATH: create_forest_path,
                TOWER_INTERIOR: create_tower_interior,
            }
        ),
        starting_scene_id=STARTING_SCENE_ID,
    )

    _validate_game_content(content)

    return content


def create_demo_scenes(
    game_state: GameState,
    recipe_book: RecipeBook,
) -> dict[str, BaseScene]:
    """Create and validate all scenes used by the first playable demo."""
    content = GameContent(
        items_by_id=create_item_registry(create_demo_items()),
        recipe_book=recipe_book,
        scenes_by_id=create_scene_registry(
            {
                VILLAGE_SQUARE: create_village_square,
                FOREST_PATH: create_forest_path,
                TOWER_INTERIOR: create_tower_interior,
            }
        ),
        starting_scene_id=STARTING_SCENE_ID,
    )

    _validate_game_content(content)

    return content.build_scenes(game_state)


def _validate_game_content(content: GameContent) -> None:
    """Validate reusable content once before it is used by sessions."""
    validation_state = GameState()

    validate_content(
        scene_entries=content.build_scenes(validation_state).items(),
        starting_scene_id=content.starting_scene_id,
        items=content.items,
        recipes=content.recipe_book.recipes,
    )
