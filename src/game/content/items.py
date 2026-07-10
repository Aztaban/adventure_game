from __future__ import annotations

from pathlib import Path

from game.content.json_loader import (
    ContentLoadError,
    load_json_file,
    require_string,
)
from game.entities.item import Item

DEFAULT_ITEMS_PATH = Path(__file__).with_name("data") / "items.json"


def create_demo_items() -> tuple[Item, ...]:
    """Load the complete item catalog used by the demo."""
    return load_items_from_json(DEFAULT_ITEMS_PATH)


def load_items_from_json(path: Path | str) -> tuple[Item, ...]:
    """Load item definitions from a JSON file."""
    source_path = Path(path)
    data = load_json_file(source_path)

    if not isinstance(data, list):
        raise ContentLoadError(f"{source_path}: expected top-level list of item definitions.")

    items: list[Item] = []
    seen_ids: set[str] = set()

    for index, entry in enumerate(data):
        context = f"{source_path}: item[{index}]"

        if not isinstance(entry, dict):
            raise ContentLoadError(f"{context}: expected object.")

        item_id = require_string(entry, "id", context)
        name = require_string(entry, "name", context)
        description = require_string(entry, "description", context)

        if item_id in seen_ids:
            raise ContentLoadError(f"{context}: duplicate item ID '{item_id}'.")

        seen_ids.add(item_id)
        items.append(
            Item(
                item_id=item_id,
                name=name,
                description=description,
            )
        )

    return tuple(items)
