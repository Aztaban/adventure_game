import pytest

from game.entities.item import Item
from game.systems.recipe import Recipe, RecipeBook


def create_result_item() -> Item:
    return Item(
        item_id="result",
        name="Result",
        description="Combined test item.",
    )


def create_recipe() -> Recipe:
    return Recipe(
        first_item_id="first",
        second_item_id="second",
        result_item=create_result_item(),
        success_text="Items combined.",
    )


def test_recipe_book_finds_recipe() -> None:
    recipe = create_recipe()
    recipe_book = RecipeBook([recipe])

    result = recipe_book.find("first", "second")

    assert result is recipe


def test_recipe_order_does_not_matter() -> None:
    recipe = create_recipe()
    recipe_book = RecipeBook([recipe])

    result = recipe_book.find("second", "first")

    assert result is recipe


def test_recipe_book_returns_none_for_missing_recipe() -> None:
    recipe_book = RecipeBook([create_recipe()])

    result = recipe_book.find("first", "missing")

    assert result is None


def test_recipe_book_rejects_duplicate_recipe() -> None:
    recipe_book = RecipeBook([create_recipe()])

    reversed_recipe = Recipe(
        first_item_id="second",
        second_item_id="first",
        result_item=create_result_item(),
        success_text="Duplicate.",
    )

    with pytest.raises(
        ValueError,
        match="already exists",
    ):
        recipe_book.add(reversed_recipe)


def test_recipe_rejects_same_item_twice() -> None:
    with pytest.raises(
        ValueError,
        match="different items",
    ):
        Recipe(
            first_item_id="same",
            second_item_id="same",
            result_item=create_result_item(),
            success_text="Invalid.",
        )
