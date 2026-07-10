from __future__ import annotations

from dataclasses import dataclass

from game.content.demo_world import create_demo_scenes
from game.content.recipes import create_demo_recipe_book
from game.content.scene_ids import STARTING_SCENE_ID
from game.game_state import GameState
from game.scene_manager import SceneManager
from game.systems.recipe import RecipeBook


@dataclass(frozen=True)
class GameSession:
    """One fresh playable run of the game."""

    game_state: GameState
    recipe_book: RecipeBook
    scene_manager: SceneManager


def create_demo_game_session(
    recipe_book: RecipeBook | None = None
) -> GameSession:
    """Create a fresh demo session with new runtime state and scenes."""
    active_recipe_book = recipe_book or create_demo_recipe_book()
    game_state = GameState()
    scene_manager = SceneManager(
        scenes=create_demo_scenes(game_state, active_recipe_book),
        starting_scene_id=STARTING_SCENE_ID,
    )

    return GameSession(
        game_state=game_state,
        recipe_book=active_recipe_book,
        scene_manager=scene_manager,
    )
