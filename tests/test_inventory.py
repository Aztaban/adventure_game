from game.entities.item import Item
from game.systems.inventory import Inventory


def create_test_item() -> Item:
    return Item(
        item_id="test_item",
        name="Test Item",
        description="An item used by automated tests.",
    )


def test_inventory_starts_empty() -> None:
    inventory = Inventory()

    assert len(inventory) == 0
    assert inventory.items == ()


def test_inventory_adds_item() -> None:
    inventory = Inventory()
    item = create_test_item()

    was_added = inventory.add(item)

    assert was_added
    assert len(inventory) == 1
    assert inventory.contains("test_item")
    assert inventory.items == (item,)


def test_inventory_rejects_duplicate_item() -> None:
    inventory = Inventory()
    item = create_test_item()

    first_result = inventory.add(item)
    second_result = inventory.add(item)

    assert first_result
    assert not second_result
    assert len(inventory) == 1


def test_inventory_removes_item() -> None:
    inventory = Inventory()
    item = create_test_item()
    inventory.add(item)

    removed_item = inventory.remove("test_item")

    assert removed_item is item
    assert not inventory.contains("test_item")
    assert len(inventory) == 0


def test_inventory_returns_none_for_missing_item() -> None:
    inventory = Inventory()

    removed_item = inventory.remove("missing")

    assert removed_item is None
