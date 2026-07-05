import pygame

from game.content.scene_ids import FOREST_PATH, VILLAGE_SQUARE
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item import Item
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.scenes.adventure_scene import AdventureScene
from game.scenes.base_scene import BaseScene
from game.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from game.systems.inventory import Inventory


def create_demo_scenes(
    inventory: Inventory,
) -> dict[str, BaseScene]:
    """Create all scenes used by the first playable demo."""
    empty_cup = Item(
        item_id="empty_cup",
        name="Empty Cup",
        description=("A chipped cup that looks ready for a suspicious beverage."),
    )

    moon_herb = Item(
        item_id="moon_herb",
        name="Moon Herb",
        description=("A glowing herb with an unreasonable amount of confidence."),
    )

    village_square = AdventureScene(
        name="Village Square",
        description=("A peaceful square with a suspicious lack of villagers."),
        background_color=(63, 48, 78),
        exits=[
            ExitHotspot(
                rect=pygame.Rect(
                    WINDOW_WIDTH - 240,
                    WINDOW_HEIGHT // 2 - 50,
                    190,
                    100,
                ),
                target_scene_id=FOREST_PATH,
                label="To Forest",
            )
        ],
        hotspots=[
            Hotspot(
                rect=pygame.Rect(120, 250, 240, 120),
                label="Notice Board",
                inspect_text=("The notice says: Beware the forest. Also, bake sale Friday."),
            ),
            Hotspot(
                rect=pygame.Rect(450, 300, 180, 100),
                label="Old Well",
                inspect_text=("The well whispers something about unpaid rent."),
            ),
        ],
        item_hotspots=[
            ItemHotspot(
                rect=pygame.Rect(390, 460, 180, 80),
                item=empty_cup,
                pickup_text=("You pick up the Empty Cup. It smells faintly of adventure."),
            )
        ],
        npcs=[
            NPC(
                rect=pygame.Rect(760, 240, 190, 180),
                name="Retired Witch",
                dialogue_lines=(
                    "I am retired. Completely retired.",
                    "The floating broom is merely a gardening tool.",
                    "Please stop looking at the glowing vegetables.",
                ),
            )
        ],
        inventory=inventory,
    )

    forest_path = AdventureScene(
        name="Forest Path",
        description=("The trees appear to be discussing you quietly."),
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
                item=moon_herb,
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
        inventory=inventory,
    )

    return {
        VILLAGE_SQUARE: village_square,
        FOREST_PATH: forest_path,
    }
