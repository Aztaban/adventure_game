from game.content.item_ids import MOON_HERB, WATER_CUP
from game.content.items import create_glowing_tea
from game.systems.recipe import Recipe, RecipeBook


def create_demo_recipe_book() -> RecipeBook:
    """Create all item-combination recipes for the demo."""
    return RecipeBook(
        recipes=[
            Recipe(
                first_item_id=WATER_CUP,
                second_item_id=MOON_HERB,
                result_item=create_glowing_tea(),
                success_text=(
                    "You steep the Moon Herb in the Cup of Water. "
                    "It glows, bubbles, and becomes Glowing Tea."
                ),
            )
        ]
    )
