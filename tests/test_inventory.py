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
    assert inventory.selected_item is None


def test_inventory_adds_item() -> None:
    inventory = Inventory()
    item = create_test_item()

    was_added = inventory.add(item)

    assert was_added
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


def test_inventory_selects_item() -> None:
    inventory = Inventory()
    item = create_test_item()
    inventory.add(item)

    was_selected = inventory.select("test_item")

    assert was_selected
    assert inventory.selected_item is item


def test_inventory_rejects_unknown_selection() -> None:
    inventory = Inventory()

    was_selected = inventory.select("missing")

    assert not was_selected
    assert inventory.selected_item is None


def test_inventory_toggles_selection() -> None:
    inventory = Inventory()
    item = create_test_item()
    inventory.add(item)

    first_result = inventory.toggle_selection("test_item")
    second_result = inventory.toggle_selection("test_item")

    assert first_result
    assert not second_result
    assert inventory.selected_item is None


def test_removing_selected_item_clears_selection() -> None:
    inventory = Inventory()
    item = create_test_item()
    inventory.add(item)
    inventory.select(item.item_id)

    removed_item = inventory.remove(item.item_id)

    assert removed_item is item
    assert inventory.selected_item is None
    assert not inventory.contains(item.item_id)


def test_inventory_returns_none_for_missing_item() -> None:
    inventory = Inventory()

    removed_item = inventory.remove("missing")

    assert removed_item is None
