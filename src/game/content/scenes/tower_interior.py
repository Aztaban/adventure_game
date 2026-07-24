from collections.abc import Mapping

import pygame

from game.asset_ids import (
    ANCIENT_PEDESTAL_IMAGE,
    PATH_EXIT_IMAGE,
    TOWER_INTERIOR_BACKGROUND,
)
from game.content.flag_ids import DEMO_COMPLETED
from game.content.scene_ids import FOREST_PATH
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item import Item
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.settings import LOGICAL_HEIGHT
from game.systems.recipe import RecipeBook
from game.ui.resources import UIResources


def create_tower_interior(
    game_state: GameState,
    recipe_book: RecipeBook,
    items_by_id: Mapping[str, Item],
    ui_resources: UIResources,
) -> AdventureScene:
    """Create the final tower scene."""
    del items_by_id

    return AdventureScene(
        name="Ancient Tower",
        description=("The tower smells of dust, magic, and recently brewed tea."),
        background_color=(45, 42, 62),
        exits=[
            ExitHotspot(
                rect=pygame.Rect(
                    50,
                    LOGICAL_HEIGHT // 2 - 50,
                    190,
                    100,
                ),
                target_scene_id=FOREST_PATH,
                label="Leave Tower",
                image_asset_id=PATH_EXIT_IMAGE,
            )
        ],
        hotspots=[
            Hotspot(
                rect=pygame.Rect(470, 250, 320, 180),
                label="Ancient Pedestal",
                inspect_text=("The pedestal waits for someone to finish the demo."),
                inspect_flag=DEMO_COMPLETED,
                flagged_inspect_text=("The pedestal glows warmly. Demo complete. The tower will remember this."),
                image_asset_id=ANCIENT_PEDESTAL_IMAGE,
            )
        ],
        item_hotspots=[],
        npcs=[],
        game_state=game_state,
        recipe_book=recipe_book,
        ui_resources=ui_resources,
        background_image_id=TOWER_INTERIOR_BACKGROUND,
    )
