import pygame

from game.content.flag_ids import (
    TOWER_UNLOCKED,
    WITCH_RECEIVED_TEA,
)
from game.content.interaction_ids import OLD_WELL_INTERACTION
from game.content.item_ids import EMPTY_CUP, GLOWING_TEA
from game.content.items import (
    create_empty_cup,
    create_rusty_key,
    create_water_cup,
)
from game.content.pickup_ids import EMPTY_CUP_PICKUP
from game.content.scene_ids import FOREST_PATH
from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import RecipeBook


def create_village_square(
    game_state: GameState,
    recipe_book: RecipeBook,
) -> AdventureScene:
    """Create the Village Square scene."""
    return AdventureScene(
        name="Village Square",
        description="A peaceful square with a suspicious lack of villagers.",
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
                inspect_text="The notice says: Beware the forest. Also, bake sale Friday.",
                inspect_flag=TOWER_UNLOCKED,
                flagged_inspect_text="A new message has appeared: The old tower path is open again.",
            ),
            Hotspot(
                rect=pygame.Rect(450, 300, 180, 100),
                label="Old Well",
                inspect_text="The well whispers something about unpaid rent.",
                item_use=ItemUseInteraction(
                    required_item_id=EMPTY_CUP,
                    success_text=(
                        "You lower the Empty Cup into the well. "
                        "It comes back as a Cup of Water."
                    ),
                    failure_text="The well refuses that item with unnecessary confidence.",
                    completed_text="The well has already filled your cup once today.",
                    consume_item=True,
                    result_item=create_water_cup(),
                    interaction_id=OLD_WELL_INTERACTION,
                ),
                completed_inspect_text="The well is now pretending it cannot hear you.",
            ),
        ],
        item_hotspots=[
            ItemHotspot(
                pickup_id=EMPTY_CUP_PICKUP,
                rect=pygame.Rect(390, 460, 180, 80),
                item=create_empty_cup(),
                pickup_text="You pick up the Empty Cup. It smells faintly of adventure.",
            )
        ],
        npcs=[
            NPC(
                rect=pygame.Rect(760, 240, 190, 180),
                name="Retired Witch",
                dialogue_lines=(
                    "I am retired. Completely retired.",
                    "Still, a cup of Glowing Tea might improve my mood.",
                    "The tower key remains safely with me until then.",
                ),
                item_use=ItemUseInteraction(
                    required_item_id=GLOWING_TEA,
                    success_text=(
                        "The witch drinks the Glowing Tea and smiles. "
                        "She gives you a Rusty Key for the tower gate."
                    ),
                    failure_text=(
                        "The witch examines the item and hands it back. "
                        "That is definitely not Glowing Tea."
                    ),
                    completed_text="The witch has already finished the tea and given you the key.",
                    consume_item=True,
                    flags_to_set=(WITCH_RECEIVED_TEA,),
                    result_item=create_rusty_key(),
                    completion_flag=WITCH_RECEIVED_TEA,
                ),
                dialogue_flag=WITCH_RECEIVED_TEA,
                flagged_dialogue_lines=(
                    "That tea was alarmingly effective.",
                    "Try the Rusty Key on the tower gate.",
                    "If anything inside has too many eyes, be polite.",
                ),
            )
        ],
        game_state=game_state,
        recipe_book=recipe_book,
    )
