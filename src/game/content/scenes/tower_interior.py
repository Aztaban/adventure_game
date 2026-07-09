import pygame

from game.content.flag_ids import DEMO_COMPLETED
from game.content.scene_ids import FOREST_PATH
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.settings import WINDOW_HEIGHT
from game.systems.recipe import RecipeBook


def create_tower_interior(
    game_state: GameState,
    recipe_book: RecipeBook,
) -> AdventureScene:
    """Create the final tower scene."""
    return AdventureScene(
        name="Ancient Tower",
        description=("The tower smells of dust, magic, and recently brewed tea."),
        background_color=(45, 42, 62),
        exits=[
            ExitHotspot(
                rect=pygame.Rect(
                    50,
                    WINDOW_HEIGHT // 2 - 50,
                    190,
                    100,
                ),
                target_scene_id=FOREST_PATH,
                label="Leave Tower",
            )
        ],
        hotspots=[
            Hotspot(
                rect=pygame.Rect(470, 250, 320, 180),
                label="Ancient Pedestal",
                inspect_text=("The pedestal waits for someone to finish the demo."),
                inspect_flag=DEMO_COMPLETED,
                flagged_inspect_text=("The pedestal glows warmly. Demo complete. The tower will remember this."),
            )
        ],
        item_hotspots=[],
        npcs=[],
        game_state=game_state,
        recipe_book=recipe_book,
    )
