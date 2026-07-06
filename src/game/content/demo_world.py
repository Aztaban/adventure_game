from game.content.scene_ids import FOREST_PATH, VILLAGE_SQUARE
from game.content.scenes.forest_path import create_forest_path
from game.content.scenes.village_square import create_village_square
from game.game_state import GameState
from game.scenes.base_scene import BaseScene


def create_demo_scenes(
    game_state: GameState,
) -> dict[str, BaseScene]:
    """Create all scenes used by the first playable demo."""
    return {
        VILLAGE_SQUARE: create_village_square(game_state),
        FOREST_PATH: create_forest_path(game_state),
    }
