from game.content.items import create_demo_items
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
from game.game_state import GameState
from game.scenes.base_scene import BaseScene


def create_demo_scenes(
    game_state: GameState,
) -> dict[str, BaseScene]:
    """Create and validate all scenes used by the first playable demo."""
    scene_entries = (
        (VILLAGE_SQUARE, create_village_square(game_state)),
        (FOREST_PATH, create_forest_path(game_state)),
        (TOWER_INTERIOR, create_tower_interior(game_state)),
    )

    validate_content(
        scene_entries=scene_entries,
        starting_scene_id=STARTING_SCENE_ID,
        items=create_demo_items(),
        recipes=game_state.recipe_book.recipes,
    )

    return dict(scene_entries)
