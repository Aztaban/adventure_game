from __future__ import annotations

from dataclasses import dataclass, field

from game.systems.inventory import Inventory


@dataclass
class GameState:
    """Mutable persistent state shared by every scene in the game."""

    inventory: Inventory = field(default_factory=Inventory)
    _flags: set[str] = field(default_factory=set, repr=False)
    _collected_pickup_ids: set[str] = field(
        default_factory=set,
        repr=False,
    )
    _completed_interaction_ids: set[str] = field(
        default_factory=set,
        repr=False,
    )

    def has_flag(self, flag: str) -> bool:
        """Return whether a progression flag is active."""
        return flag in self._flags

    def set_flag(self, flag: str) -> None:
        """Activate a progression flag."""
        self._flags.add(flag)

    def clear_flag(self, flag: str) -> None:
        """Remove a progression flag when it exists."""
        self._flags.discard(flag)

    def has_collected_pickup(self, pickup_id: str) -> bool:
        """Return whether a world pickup has already been collected."""
        return pickup_id in self._collected_pickup_ids

    def collect_pickup(self, pickup_id: str) -> None:
        """Record a world pickup as collected."""
        self._collected_pickup_ids.add(pickup_id)

    def has_completed_interaction(self, interaction_id: str) -> bool:
        """Return whether a non-semantic interaction is complete."""
        return interaction_id in self._completed_interaction_ids

    def complete_interaction(self, interaction_id: str) -> None:
        """Record a non-semantic interaction as complete."""
        self._completed_interaction_ids.add(interaction_id)
