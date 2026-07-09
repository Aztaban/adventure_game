from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from game.entities.item import Item


@dataclass(frozen=True)
class ItemUseResult:
    """Result of attempting to use an item on a target."""

    success: bool
    message: str
    consume_item: bool = False
    flags_to_set: tuple[str, ...] = ()
    result_item: Item | None = None


@dataclass
class ItemUseInteraction:
    """Define which item a target requires and what happens when used."""

    required_item_id: str
    success_text: str
    failure_text: str
    completed_text: str
    consume_item: bool = False
    flags_to_set: tuple[str, ...] = ()
    result_item: Item | None = None
    interaction_id: str | None = None
    completion_flag: str | None = None

    def __post_init__(self) -> None:
        has_interaction_id = self.interaction_id is not None
        has_completion_flag = self.completion_flag is not None

        if has_interaction_id == has_completion_flag:
            raise ValueError(
                "Item-use interaction requires exactly one completion "
                "identifier: interaction_id or completion_flag."
            )

        if self.completion_flag is not None and self.completion_flag not in self.flags_to_set:
            raise ValueError("completion_flag must also be present in flags_to_set.")

    def has_been_completed(
        self,
        has_flag: Callable[[str], bool],
        has_completed_interaction: Callable[[str], bool],
    ) -> bool:
        """Return whether persistent world state marks this complete."""
        if self.completion_flag is not None:
            return has_flag(self.completion_flag)

        if self.interaction_id is None:
            return False

        return has_completed_interaction(self.interaction_id)

    def attempt(
        self,
        item_id: str,
        *,
        is_completed: bool = False,
    ) -> ItemUseResult:
        """Return the outcome without mutating persistent state."""
        if is_completed:
            return ItemUseResult(
                success=False,
                message=self.completed_text,
            )

        if item_id != self.required_item_id:
            return ItemUseResult(
                success=False,
                message=self.failure_text,
            )

        return ItemUseResult(
            success=True,
            message=self.success_text,
            consume_item=self.consume_item,
            flags_to_set=self.flags_to_set,
            result_item=self.result_item,
        )
