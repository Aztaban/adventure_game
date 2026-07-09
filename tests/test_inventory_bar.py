import pygame

from game.entities.item import Item
from game.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from game.ui.inventory_bar import InventoryBar

pygame.font.init()

PLANNED_MAXIMUM_VISIBLE_ITEMS = 8


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


def create_items(count: int) -> tuple[Item, ...]:
    """Create a predictable inventory item sequence."""
    return tuple(
        create_item(
            f"item_{index}",
            f"Item {index}",
        )
        for index in range(count)
    )


def test_inventory_bar_draws_empty_inventory() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    inventory_bar.draw(
        surface=surface,
        items=(),
        selected_item=None,
    )


def test_inventory_bar_layout_for_empty_inventory_has_panel_and_no_rows() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)

    layout = inventory_bar.layout_for_items(())

    assert layout.item_rows == ()
    assert layout.panel_rect.width == inventory_bar.PANEL_WIDTH
    assert layout.panel_rect.height >= inventory_bar.MINIMUM_HEIGHT


def test_inventory_bar_creates_one_row_per_item() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    items = create_items(2)

    layout = inventory_bar.layout_for_items(items)

    assert len(layout.item_rows) == 2
    assert layout.item_rows[0][0] is items[0]
    assert layout.item_rows[1][0] is items[1]


def test_inventory_rows_do_not_overlap() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    items = create_items(2)

    rows = inventory_bar.layout_for_items(items).item_rows

    first_rect = rows[0][1]
    second_rect = rows[1][1]

    assert not first_rect.colliderect(second_rect)
    assert second_rect.top == first_rect.bottom


def test_inventory_rows_respect_panel_padding() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    items = create_items(1)

    layout = inventory_bar.layout_for_items(items)
    row_rect = layout.item_rows[0][1]

    assert row_rect.left == layout.panel_rect.left + inventory_bar.INNER_PADDING
    assert row_rect.right == layout.panel_rect.right - inventory_bar.INNER_PADDING
    assert row_rect.top > layout.panel_rect.top + inventory_bar.INNER_PADDING
    assert row_rect.bottom <= layout.panel_rect.bottom - inventory_bar.INNER_PADDING


def test_inventory_bar_finds_clicked_item_from_shared_layout() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    items = create_items(2)
    layout = inventory_bar.layout_for_items(items)

    clicked_item = inventory_bar.item_at_position(
        position=layout.item_rows[1][1].center,
        items=items,
    )

    assert clicked_item is items[1]


def test_inventory_bar_returns_none_outside_item_rows() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    items = create_items(1)

    clicked_item = inventory_bar.item_at_position(
        position=(0, 0),
        items=items,
    )

    assert clicked_item is None


def test_planned_maximum_inventory_size_fits_inside_window() -> None:
    inventory_bar = InventoryBar(WINDOW_WIDTH)
    items = create_items(PLANNED_MAXIMUM_VISIBLE_ITEMS)

    layout = inventory_bar.layout_for_items(items)

    assert len(layout.item_rows) == PLANNED_MAXIMUM_VISIBLE_ITEMS
    assert layout.panel_rect.bottom <= WINDOW_HEIGHT
