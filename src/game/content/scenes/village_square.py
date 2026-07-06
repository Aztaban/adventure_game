import pygame

from game.content.item_ids import EMPTY_CUP, MOON_HERB
from game.content.items import create_empty_cup
from game.content.scene_ids import FOREST_PATH
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from game.systems.item_use import ItemUseInteraction


def create_village_square(
    game_state: GameState,
) -> AdventureScene:
    """Create the Village Square scene."""
    return AdventureScene(
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
                item_use=ItemUseInteraction(
                    required_item_id=EMPTY_CUP,
                    success_text=("You lower the Empty Cup into the well. The well reluctantly provides water."),
                    failure_text=("The well refuses that item with unnecessary confidence."),
                    completed_text=("The well has already contributed enough for one day."),
                    consume_item=False,
                ),
                completed_inspect_text=("The well is now pretending it cannot hear you."),
            ),
        ],
        item_hotspots=[
            ItemHotspot(
                rect=pygame.Rect(390, 460, 180, 80),
                item=create_empty_cup(),
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
                item_use=ItemUseInteraction(
                    required_item_id=MOON_HERB,
                    success_text=("The witch accepts the Moon Herb. Her retirement appears temporarily suspended."),
                    failure_text=("The witch examines the item and hands it back."),
                    completed_text=("The witch already has the Moon Herb."),
                    consume_item=True,
                ),
                completed_dialogue_lines=(
                    "Fine. The Moon Herb is exactly what I needed.",
                    ("This does not mean I have returned to professional witchcraft."),
                    "It is merely an aggressively magical hobby.",
                ),
            )
        ],
        game_state=game_state,
    )
