from __future__ import annotations

from dataclasses import dataclass, field

from game.systems.inventory import Inventory


@dataclass
class GameState:
    """Mutable state shared by every scene in the game."""

    inventory: Inventory = field(default_factory=Inventory)
    _flags: set[str] = field(default_factory=set, repr=False)

    def has_flag(self, flag: str) -> bool:
        """Return whether a progression flag is active."""
        return flag in self._flags

    def set_flag(self, flag: str) -> None:
        """Activate a progression flag."""
        self._flags.add(flag)

    def clear_flag(self, flag: str) -> None:
        """Remove a progression flag when it exists."""
        self._flags.discard(flag)
