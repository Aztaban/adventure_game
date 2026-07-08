import pygame

from game.entities.hotspot import Hotspot
from game.systems.item_use import ItemUseInteraction


def create_hotspot(
    *,
    item_use: ItemUseInteraction | None = None,
    completed_inspect_text: str | None = None,
    inspect_flag: str | None = None,
    flagged_inspect_text: str | None = None,
) -> Hotspot:
    return Hotspot(
        rect=pygame.Rect(100, 100, 200, 100),
        label="Test Object",
        inspect_text="A mysterious test object.",
        item_use=item_use,
        completed_inspect_text=completed_inspect_text,
        inspect_flag=inspect_flag,
        flagged_inspect_text=flagged_inspect_text,
    )


def create_item_use() -> ItemUseInteraction:
    return ItemUseInteraction(
        required_item_id="correct_item",
        success_text="That worked.",
        failure_text="That did not work.",
        completed_text="This is already complete.",
    )


def test_hotspot_contains_point_inside_rectangle() -> None:
    hotspot = create_hotspot()

    assert hotspot.contains_point((150, 150))


def test_hotspot_rejects_point_outside_rectangle() -> None:
    hotspot = create_hotspot()

    assert not hotspot.contains_point((50, 50))


def test_default_hotspot_returns_inspect_text() -> None:
    hotspot = create_hotspot()

    assert (
        hotspot.inspect_text_for(lambda _: False)
        == "A mysterious test object."
    )


def test_completed_interaction_returns_completed_text() -> None:
    item_use = create_item_use()
    item_use.attempt("correct_item")

    hotspot = create_hotspot(
        item_use=item_use,
        completed_inspect_text="The interaction is complete.",
    )

    assert (
        hotspot.inspect_text_for(lambda _: False)
        == "The interaction is complete."
    )


def test_active_matching_flag_returns_flagged_inspect_text() -> None:
    hotspot = create_hotspot(
        inspect_flag="world_changed",
        flagged_inspect_text="The world has changed this object.",
    )

    assert (
        hotspot.inspect_text_for(
            lambda flag: flag == "world_changed",
        )
        == "The world has changed this object."
    )


def test_inactive_flag_falls_back_to_completed_text() -> None:
    item_use = create_item_use()
    item_use.attempt("correct_item")

    hotspot = create_hotspot(
        item_use=item_use,
        completed_inspect_text="The interaction is complete.",
        inspect_flag="world_changed",
        flagged_inspect_text="The world has changed this object.",
    )

    assert (
        hotspot.inspect_text_for(lambda _: False)
        == "The interaction is complete."
    )


def test_inspection_text_priority_is_flag_then_completed_then_default() -> None:
    item_use = create_item_use()

    hotspot = create_hotspot(
        item_use=item_use,
        completed_inspect_text="The interaction is complete.",
        inspect_flag="world_changed",
        flagged_inspect_text="The world has changed this object.",
    )

    assert (
        hotspot.inspect_text_for(lambda _: False)
        == "A mysterious test object."
    )

    item_use.attempt("correct_item")

    assert (
        hotspot.inspect_text_for(lambda _: False)
        == "The interaction is complete."
    )

    assert (
        hotspot.inspect_text_for(
            lambda flag: flag == "world_changed",
        )
        == "The world has changed this object."
    )
