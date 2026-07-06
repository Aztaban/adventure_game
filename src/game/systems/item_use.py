from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ItemUseResult:
    """Result of attempting to use an item on a target."""

    success: bool
    message: str
    consume_item: bool = False


@dataclass
class ItemUseInteraction:
    """Define which item a target requires and what happens when used."""

    required_item_id: str
    success_text: str
    failure_text: str
    completed_text: str
    consume_item: bool = False

    is_completed: bool = field(default=False, init=False)

    def attempt(self, item_id: str) -> ItemUseResult:
        """Attempt to use an item on this interaction target."""
        if self.is_completed:
            return ItemUseResult(
                success=False,
                message=self.completed_text,
            )

        if item_id != self.required_item_id:
            return ItemUseResult(
                success=False,
                message=self.failure_text,
            )

        self.is_completed = True

        return ItemUseResult(success=True, message=self.success_text, consume_item=self.consume_item)
