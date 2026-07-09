from game.content.item_ids import (
    EMPTY_CUP,
    GLOWING_TEA,
    MOON_HERB,
    RUSTY_KEY,
    WATER_CUP,
)
from game.entities.item import Item


def create_empty_cup() -> Item:
    """Create the Empty Cup item."""
    return Item(
        item_id=EMPTY_CUP,
        name="Empty Cup",
        description="A chipped cup that looks ready for a suspicious beverage.",
    )


def create_water_cup() -> Item:
    """Create the Cup of Water item."""
    return Item(
        item_id=WATER_CUP,
        name="Cup of Water",
        description="A chipped cup now filled with cold well water.",
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
        description="A luminous herbal drink that is probably safe enough.",
    )


def create_rusty_key() -> Item:
    """Create the Rusty Key item."""
    return Item(
        item_id=RUSTY_KEY,
        name="Rusty Key",
        description="An old tower key with more rust than confidence.",
    )


def create_demo_items() -> tuple[Item, ...]:
    """Create the complete item catalog used by the demo."""
    return (
        create_empty_cup(),
        create_water_cup(),
        create_moon_herb(),
        create_glowing_tea(),
        create_rusty_key(),
    )
