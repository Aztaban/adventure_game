from game.content.item_ids import (
    EMPTY_CUP,
    GLOWING_TEA,
    MOON_HERB,
)
from game.entities.item import Item


def create_empty_cup() -> Item:
    """Create the Empty Cup item."""
    return Item(
        item_id=EMPTY_CUP,
        name="Empty Cup",
        description="A chipped cup that looks ready for a suspicious beverage.",
    )


def create_moon_herb() -> Item:
    """Create the Moon Herb item."""
    return Item(
        item_id=MOON_HERB,
        name="Moon Herb",
        description="A glowing herb with an unreasonable amount of confidence.",
    )


def create_glowing_tea() -> Item:
    """Create the Glowing Tea item."""
    return Item(
        item_id=GLOWING_TEA,
        name="Glowing Tea",
        description=("A luminous herbal drink that is probably safe enough."),
    )


def create_demo_items() -> tuple[Item, ...]:
    """Create the complete item catalog used by the demo."""
    return (
        create_empty_cup(),
        create_moon_herb(),
        create_glowing_tea(),
    )
