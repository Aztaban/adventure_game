import pygame

from game.entities.item import Item
from game.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from game.ui.inventory_bar import InventoryBar

pygame.font.init()


def create_item(
    item_id: str,
    name: str,
) -> Item:
    """Create an item used by InventoryBar tests."""
    return Item(
        item_id=item_id,
        name=name,
        description="An item used by automated tests.",
    )


def test_inventory_bar_draws_empty_inventory() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    inventory_bar.draw(
        surface=surface,
        items=(),
        selected_item=None,
    )


def test_inventory_bar_creates_one_row_per_item() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)

    items = (
        create_item("first", "First Item"),
        create_item("second", "Second Item"),
    )

    rows = inventory_bar.item_rows(items)

    assert len(rows) == 2
    assert rows[0][0] is items[0]
    assert rows[1][0] is items[1]


def test_inventory_rows_do_not_overlap() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)

    items = (
        create_item("first", "First Item"),
        create_item("second", "Second Item"),
    )

    rows = inventory_bar.item_rows(items)

    first_rect = rows[0][1]
    second_rect = rows[1][1]

    assert not first_rect.colliderect(second_rect)
    assert second_rect.top == first_rect.bottom


def test_inventory_bar_finds_clicked_item() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)

    items = (
        create_item("first", "First Item"),
        create_item("second", "Second Item"),
    )

    rows = inventory_bar.item_rows(items)

    clicked_item = inventory_bar.item_at_position(
        position=rows[1][1].center,
        items=items,
    )

    assert clicked_item is items[1]


def test_inventory_bar_returns_none_outside_item_rows() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)

    items = (create_item("first", "First Item"),)

    clicked_item = inventory_bar.item_at_position(
        position=(0, 0),
        items=items,
    )

    assert clicked_item is None
