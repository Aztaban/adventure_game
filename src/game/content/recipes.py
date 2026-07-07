from game.content.item_ids import EMPTY_CUP, MOON_HERB
from game.content.items import create_glowing_tea
from game.systems.recipe import Recipe, RecipeBook


def create_demo_recipe_book() -> RecipeBook:
    """Create all item-combination recipes for the demo."""
    return RecipeBook(
        recipes=[
            Recipe(
                first_item_id=EMPTY_CUP,
                second_item_id=MOON_HERB,
                result_item=create_glowing_tea(),
                success_text=(
                    "You place the Moon Herb into the Empty Cup. "
                    "It somehow becomes Glowing Tea without water, "
                    "heat, or respect for chemistry."
                ),
            )
        ]
    )
