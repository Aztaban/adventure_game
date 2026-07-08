import pygame

from game.entities.item import Item
from game.entities.item_hotspot import ItemHotspot


def create_item_hotspot() -> ItemHotspot:
    item = Item(
        item_id="test_item",
        name="Test Item",
        description="An item used by automated tests.",
    )

    return ItemHotspot(
        pickup_id="pickup.test",
        rect=pygame.Rect(100, 100, 200, 100),
        item=item,
        pickup_text="You picked up the test item.",
    )


def test_item_hotspot_contains_point_inside_rectangle() -> None:
    item_hotspot = create_item_hotspot()

    assert item_hotspot.contains_point((150, 150))


def test_item_hotspot_rejects_point_outside_rectangle() -> None:
    item_hotspot = create_item_hotspot()

    assert not item_hotspot.contains_point((50, 50))
