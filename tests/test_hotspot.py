import pygame

from game.entities.hotspot import Hotspot


def create_hotspot() -> Hotspot:
    return Hotspot(
        rect=pygame.Rect(100, 100, 200, 100),
        label="Test Object",
        inspect_text="A mysterious test object.",
    )


def test_hotspot_contains_point_inside_rectangle() -> None:
    hotspot = create_hotspot()

    assert hotspot.contains_point((150, 150))


def test_hotspot_rejects_point_outside_rectangle() -> None:
    hotspot = create_hotspot()

    assert not hotspot.contains_point((50, 50))
