from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """An item that can be stored in the player's inventory."""

    item_id: str
    name: str
    description: str
