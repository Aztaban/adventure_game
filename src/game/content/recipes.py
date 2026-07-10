from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from game.content.items import create_demo_items
from game.content.json_loader import (
    ContentLoadError,
    load_json_file,
    require_string,
)
from game.entities.item import Item
from game.systems.recipe import Recipe, RecipeBook

DEFAULT_RECIPES_PATH = Path(__file__).with_name("data") / "recipes.json"


def create_demo_recipe_book(
    items_by_id: Mapping[str, Item] | None = None,
) -> RecipeBook:
    """Load all item-combination recipes for the demo."""
    item_registry = items_by_id or {
        item.item_id: item
        for item in create_demo_items()
    }

    return load_recipe_book_from_json(
        path=DEFAULT_RECIPES_PATH,
        items_by_id=item_registry,
    )


def load_recipe_book_from_json(
    *,
    path: Path | str,
    items_by_id: Mapping[str, Item],
) -> RecipeBook:
    """Load recipe definitions from JSON using an item registry."""
    source_path = Path(path)
    data = load_json_file(source_path)

    if not isinstance(data, list):
        raise ContentLoadError(
            f"{source_path}: expected top-level list of recipe definitions."
        )

    recipes: list[Recipe] = []
    seen_keys: set[tuple[str, str]] = set()

    for index, entry in enumerate(data):
        context = f"{source_path}: recipe[{index}]"

        if not isinstance(entry, dict):
            raise ContentLoadError(f"{context}: expected object.")

        recipe = _create_recipe(
            entry=entry,
            context=context,
            items_by_id=items_by_id,
        )

        recipe_key = tuple(sorted((recipe.first_item_id, recipe.second_item_id)))

        if recipe_key in seen_keys:
            raise ContentLoadError(
                f"{context}: duplicate recipe for item pair "
                f"'{recipe_key[0]}' + '{recipe_key[1]}'."
            )

        seen_keys.add(recipe_key)
        recipes.append(recipe)

    return RecipeBook(recipes=recipes)


def _create_recipe(
    *,
    entry: dict[str, Any],
    context: str,
    items_by_id: Mapping[str, Item],
) -> Recipe:
    """Create one recipe from a validated JSON object."""
    first_item_id = require_string(entry, "first_item_id", context)
    second_item_id = require_string(entry, "second_item_id", context)
    result_item_id = require_string(entry, "result_item_id", context)
    success_text = require_string(entry, "success_text", context)

    _validate_known_item(
        item_id=first_item_id,
        field_name="first_item_id",
        items_by_id=items_by_id,
        context=context,
    )
    _validate_known_item(
        item_id=second_item_id,
        field_name="second_item_id",
        items_by_id=items_by_id,
        context=context,
    )
    _validate_known_item(
        item_id=result_item_id,
        field_name="result_item_id",
        items_by_id=items_by_id,
        context=context,
    )

    try:
        return Recipe(
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            result_item=items_by_id[result_item_id],
            success_text=success_text,
        )
    except ValueError as error:
        raise ContentLoadError(f"{context}: {error}") from error


def _validate_known_item(
    *,
    item_id: str,
    field_name: str,
    items_by_id: Mapping[str, Item],
    context: str,
) -> None:
    """Raise a content load error if an item reference is unknown."""
    if item_id in items_by_id:
        return

    raise ContentLoadError(
        f"{context}: field '{field_name}' references unknown item ID "
        f"'{item_id}'."
    )
