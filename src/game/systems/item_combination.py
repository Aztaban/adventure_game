from __future__ import annotations

from dataclasses import dataclass

from game.entities.item import Item
from game.systems.inventory import Inventory
from game.systems.recipe import RecipeBook


@dataclass(frozen=True)
class ItemCombinationResult:
    """Result of attempting to combine two inventory items."""

    success: bool
    message: str
    result_item: Item | None = None


def combine_inventory_items(
    *,
    inventory: Inventory,
    recipe_book: RecipeBook,
    first_item_id: str,
    second_item_id: str,
) -> ItemCombinationResult:
    """Combine two inventory items through a validated atomic transaction."""
    first_item = inventory.get(first_item_id)
    second_item = inventory.get(second_item_id)

    if first_item is None or second_item is None:
        return ItemCombinationResult(
            success=False,
            message="You do not have both items.",
        )

    recipe = recipe_book.find(first_item_id, second_item_id)

    if recipe is None:
        return ItemCombinationResult(
            success=False,
            message=f"{first_item.name} and {second_item.name} do not combine."
        )

    result_item = recipe.result_item

    if inventory.contains(result_item.item_id):
        inventory.clear_selection()

        return ItemCombinationResult(
            success=False,
            message=f"You already have {result_item.name}.",
            result_item=result_item,
        )

    inventory.remove(first_item_id)
    inventory.remove(second_item_id)
    inventory.add(result_item)

    return ItemCombinationResult(
        success=True,
        message=recipe.success_text,
        result_item=result_item,
    )
