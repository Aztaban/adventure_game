import json
from pathlib import Path

import pytest

from game.content.item_ids import GLOWING_TEA, MOON_HERB, WATER_CUP
from game.content.items import ContentLoadError, create_demo_items, load_items_from_json
from game.content.recipes import create_demo_recipe_book, load_recipe_book_from_json


def write_json(path: Path, value: object) -> None:
    """Write test JSON content to disk."""
    path.write_text(json.dumps(value), encoding="utf-8")


def test_valid_item_file_loads_typed_items(tmp_path: Path) -> None:
    path = tmp_path / "items.json"
    write_json(
        path,
        [
            {
                "id": "test_item",
                "name": "Test Item",
                "description": "A test item.",
            }
        ],
    )

    items = load_items_from_json(path)

    assert len(items) == 1
    assert items[0].item_id == "test_item"
    assert items[0].name == "Test Item"
    assert items[0].description == "A test item."


def test_item_file_missing_field_fails_clearly(tmp_path: Path) -> None:
    path = tmp_path / "items.json"
    write_json(
        path,
        [
            {
                "id": "test_item",
                "name": "Test Item",
            }
        ],
    )

    with pytest.raises(
        ContentLoadError,
        match=r"item\[0\]: field 'description' must be a non-empty string",
    ):
        load_items_from_json(path)


def test_item_file_wrong_field_type_fails_clearly(tmp_path: Path) -> None:
    path = tmp_path / "items.json"
    write_json(
        path,
        [
            {
                "id": "test_item",
                "name": 42,
                "description": "A test item.",
            }
        ],
    )

    with pytest.raises(
        ContentLoadError,
        match=r"item\[0\]: field 'name' must be a non-empty string",
    ):
        load_items_from_json(path)


def test_duplicate_item_id_fails_clearly(tmp_path: Path) -> None:
    path = tmp_path / "items.json"
    write_json(
        path,
        [
            {
                "id": "duplicate_item",
                "name": "First",
                "description": "First item.",
            },
            {
                "id": "duplicate_item",
                "name": "Second",
                "description": "Second item.",
            },
        ],
    )

    with pytest.raises(
        ContentLoadError,
        match=r"item\[1\]: duplicate item ID 'duplicate_item'",
    ):
        load_items_from_json(path)


def test_valid_recipe_file_loads_typed_recipe_book(tmp_path: Path) -> None:
    items_by_id = {item.item_id: item for item in create_demo_items()}
    path = tmp_path / "recipes.json"
    write_json(
        path,
        [
            {
                "first_item_id": WATER_CUP,
                "second_item_id": MOON_HERB,
                "result_item_id": GLOWING_TEA,
                "success_text": "Make tea.",
            }
        ],
    )

    recipe_book = load_recipe_book_from_json(
        path=path,
        items_by_id=items_by_id,
    )

    recipe = recipe_book.find(WATER_CUP, MOON_HERB)

    assert recipe is not None
    assert recipe.result_item.item_id == GLOWING_TEA
    assert recipe.success_text == "Make tea."


def test_recipe_file_missing_field_fails_clearly(tmp_path: Path) -> None:
    items_by_id = {item.item_id: item for item in create_demo_items()}
    path = tmp_path / "recipes.json"
    write_json(
        path,
        [
            {
                "first_item_id": WATER_CUP,
                "second_item_id": MOON_HERB,
                "result_item_id": GLOWING_TEA,
            }
        ],
    )

    with pytest.raises(
        ContentLoadError,
        match=r"recipe\[0\]: field 'success_text' must be a non-empty string",
    ):
        load_recipe_book_from_json(path=path, items_by_id=items_by_id)


def test_recipe_file_unknown_reference_fails_clearly(tmp_path: Path) -> None:
    items_by_id = {item.item_id: item for item in create_demo_items()}
    path = tmp_path / "recipes.json"
    write_json(
        path,
        [
            {
                "first_item_id": WATER_CUP,
                "second_item_id": "missing_item",
                "result_item_id": GLOWING_TEA,
                "success_text": "Make tea.",
            }
        ],
    )

    with pytest.raises(
        ContentLoadError,
        match=(
            r"recipe\[0\]: field 'second_item_id' "
            "references unknown item ID 'missing_item'"
        ),
    ):
        load_recipe_book_from_json(path=path, items_by_id=items_by_id)


def test_duplicate_recipe_pair_fails_clearly(tmp_path: Path) -> None:
    items_by_id = {item.item_id: item for item in create_demo_items()}
    path = tmp_path / "recipes.json"
    write_json(
        path,
        [
            {
                "first_item_id": WATER_CUP,
                "second_item_id": MOON_HERB,
                "result_item_id": GLOWING_TEA,
                "success_text": "Make tea.",
            },
            {
                "first_item_id": MOON_HERB,
                "second_item_id": WATER_CUP,
                "result_item_id": GLOWING_TEA,
                "success_text": "Make more tea.",
            },
        ],
    )

    with pytest.raises(
        ContentLoadError,
        match=(
            r"recipe\[1\]: duplicate recipe for item pair 'moon_herb' "
            r"\+ 'water_cup'"
        ),
    ):
        load_recipe_book_from_json(path=path, items_by_id=items_by_id)


def test_demo_recipe_book_loads_from_json_definitions() -> None:
    recipe_book = create_demo_recipe_book()

    recipe = recipe_book.find(WATER_CUP, MOON_HERB)

    assert recipe is not None
    assert recipe.result_item.item_id == GLOWING_TEA
