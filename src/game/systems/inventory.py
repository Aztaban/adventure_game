from __future__ import annotations

from game.entities.item import Item


class Inventory:
    """Store the player's collected items."""

    def __init__(self) -> None:
        self._items: dict[str, Item] = {}
        self._selected_item_id: str | None = None

    @property
    def items(self) -> tuple[Item, ...]:
        """Return all inventory items in collection order."""
        return tuple(self._items.values())

    @property
    def item_ids(self) -> tuple[str, ...]:
        """Return all inventory item IDs in collection order."""
        return tuple(self._items)

    @property
    def selected_item_id(self) -> str | None:
        """Return the selected item ID when one is selected."""
        return self._selected_item_id

    @property
    def selected_item(self) -> Item | None:
        """Return the currently selected item."""
        if self._selected_item_id is None:
            return None

        return self._items.get(self._selected_item_id)

    def add(self, item: Item) -> bool:
        """Add an item and return whether it was newly added."""
        if item.item_id in self._items:
            return False

        self._items[item.item_id] = item
        return True

    def get(self, item_id: str) -> Item | None:
        """Return an inventory item by ID when present."""
        return self._items.get(item_id)

    def remove(self, item_id: str) -> Item | None:
        """Remove and return an item, if it exists."""
        removed_item = self._items.pop(item_id, None)

        if self._selected_item_id == item_id:
            self.clear_selection()

        return removed_item

    def contains(self, item_id: str) -> bool:
        """Return whether an item is present."""
        return item_id in self._items

    def select(self, item_id: str) -> bool:
        """Select an existing inventory item."""
        if item_id not in self._items:
            return False

        self._selected_item_id = item_id
        return True

    def toggle_selection(self, item_id: str) -> bool:
        """Select and item or deselect it when already selected."""
        if item_id not in self._items:
            return False

        if self._selected_item_id == item_id:
            self.clear_selection()
            return False

        self._selected_item_id = item_id
        return True

    def clear_selection(self) -> None:
        """Clear the currently selected item."""
        self._selected_item_id = None

    def __len__(self) -> int:
        """Return the number of collected items."""
        return len(self._items)
