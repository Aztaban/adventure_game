from __future__ import annotations

from game.entities.item import Item


class Inventory:
    """Store the player's collected items."""

    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    @property
    def items(self) -> tuple[Item, ...]:
        """Return all inventory items in collection order."""
        return tuple(self._items.values())

    def add(self, item: Item) -> bool:
        """Add an item and return whether it was newly added."""
        if item.item_id in self._items:
            return False

        self._items[item.item_id] = item
        return True

    def remove(self, item_id: str) -> Item | None:
        """Remove and return an item, if it exists."""
        return self._items.pop(item_id, None)

    def contains(self, item_id: str) -> bool:
        """Return whether an item is present."""
        return item_id in self._items

    def __len__(self) -> int:
        """Return the number of collected items."""
        return len(self._items)
