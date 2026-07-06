import pygame

from game.content.items import create_moon_herb
from game.content.scene_ids import VILLAGE_SQUARE
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.settings import WINDOW_HEIGHT


def create_forest_path(
    game_state: GameState,
) -> AdventureScene:
    """Create the Forest Path scene."""
    return AdventureScene(
        name="Forest Path",
        description="The trees appear to be discussing you quietly.",
        background_color=(40, 72, 58),
        exits=[
            ExitHotspot(
                rect=pygame.Rect(
                    50,
                    WINDOW_HEIGHT // 2 - 50,
                    190,
                    100,
                ),
                target_scene_id=VILLAGE_SQUARE,
                label="To Village",
            )
        ],
        hotspots=[
            Hotspot(
                rect=pygame.Rect(500, 260, 240, 120),
                label="Suspicious Stump",
                inspect_text=("The stump looks back at you. You decide not to mention it."),
            )
        ],
        item_hotspots=[
            ItemHotspot(
                rect=pygame.Rect(850, 350, 180, 100),
                item=create_moon_herb(),
                pickup_text=("You carefully collect the Moon Herb. It seems pleased with itself."),
            )
        ],
        npcs=[
            NPC(
                rect=pygame.Rect(300, 260, 170, 150),
                name="Mushroom Guard",
                dialogue_lines=(
                    "Halt. State your name and preferred soup.",
                    "No unauthorized ankles beyond this point.",
                ),
            )
        ],
        game_state=game_state,
    )
