from game.entities.item import Item
from game.systems.inventory import Inventory
from game.systems.item_combination import combine_inventory_items
from game.systems.recipe import Recipe, RecipeBook


def create_item(
    item_id: str,
    name: str,
) -> Item:
    """Create a test item."""
    return Item(
        item_id=item_id,
        name=name,
        description="A test item.",
    )


def create_recipe_book(
    first_item: Item,
    second_item: Item,
    result_item: Item,
) -> RecipeBook:
    """Create a recipe book with one test recipe."""
    return RecipeBook(
        [
            Recipe(
                first_item_id=first_item.item_id,
                second_item_id=second_item.item_id,
                result_item=result_item,
                success_text="Combination succeeded.",
            )
        ]
    )


def test_valid_recipe_combines_items_without_rendering() -> None:
    inventory = Inventory()
    first_item = create_item("first", "First Item")
    second_item = create_item("second", "Second Item")
    result_item = create_item("result", "Result Item")
    recipe_book = create_recipe_book(first_item, second_item, result_item)
    inventory.add(first_item)
    inventory.add(second_item)
    inventory.select(first_item.item_id)

    result = combine_inventory_items(
        inventory=inventory,
        recipe_book=recipe_book,
        first_item_id=first_item.item_id,
        second_item_id=second_item.item_id,
    )

    assert result.success
    assert result.result_item is result_item
    assert result.message == "Combination succeeded."
    assert not inventory.contains(first_item.item_id)
    assert not inventory.contains(second_item.item_id)
    assert inventory.contains(result_item.item_id)
    assert inventory.selected_item is None


def test_invalid_recipe_leaves_inventory_unchanged() -> None:
    inventory = Inventory()
    first_item = create_item("first", "First Item")
    second_item = create_item("second", "Second Item")
    inventory.add(first_item)
    inventory.add(second_item)
    inventory.select(first_item.item_id)

    result = combine_inventory_items(
        inventory=inventory,
        recipe_book=RecipeBook(),
        first_item_id=first_item.item_id,
        second_item_id=second_item.item_id,
    )

    assert not result.success
    assert result.result_item is None
    assert result.message == "First Item and Second Item do not combine."
    assert inventory.items == (first_item, second_item)
    assert inventory.selected_item is first_item


def test_missing_ingredient_cannot_cause_partial_mutation() -> None:
    inventory = Inventory()
    first_item = create_item("first", "First Item")
    second_item = create_item("second", "Second Item")
    result_item = create_item("result", "Result Item")
    recipe_book = create_recipe_book(first_item, second_item, result_item)
    inventory.add(first_item)
    inventory.select(first_item.item_id)

    result = combine_inventory_items(
        inventory=inventory,
        recipe_book=recipe_book,
        first_item_id=first_item.item_id,
        second_item_id=second_item.item_id,
    )

    assert not result.success
    assert result.result_item is None
    assert result.message == "You do not have both items."
    assert inventory.items == (first_item,)
    assert inventory.selected_item is first_item


def test_existing_result_item_keeps_ingredients_and_clears_selection() -> None:
    inventory = Inventory()
    first_item = create_item("first", "First Item")
    second_item = create_item("second", "Second Item")
    result_item = create_item("result", "Result Item")
    recipe_book = create_recipe_book(first_item, second_item, result_item)
    inventory.add(first_item)
    inventory.add(second_item)
    inventory.add(result_item)
    inventory.select(first_item.item_id)

    result = combine_inventory_items(
        inventory=inventory,
        recipe_book=recipe_book,
        first_item_id=first_item.item_id,
        second_item_id=second_item.item_id,
    )

    assert not result.success
    assert result.result_item is result_item
    assert result.message == "You already have Result Item."
    assert inventory.items == (first_item, second_item, result_item)
    assert inventory.selected_item is None
