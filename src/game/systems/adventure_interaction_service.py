from __future__ import annotations

from dataclasses import dataclass

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item import Item
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.systems.item_combination import combine_inventory_items
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import RecipeBook


@dataclass(frozen=True)
class AdventureInteractionOutcome:
    """Presentation and transition result of a gameplay interaction."""

    consumed: bool = False
    message: str | None = None
    speaker_name: str | None = None
    dialogue_lines: tuple[str, ...] = ()
    target_scene_id: str | None = None


class AdventureInteractionService:
    """Handle adventure gameplay transactions without Pygame presentation code."""

    def __init__(
        self,
        game_state: GameState,
        recipe_book: RecipeBook,
    ) -> None:
        self.game_state = game_state
        self.recipe_book = recipe_book

    def clear_selected_item(self) -> AdventureInteractionOutcome:
        """Clear the current inventory selection when one exists."""
        inventory = self.game_state.inventory

        if inventory.selected_item is None:
            return AdventureInteractionOutcome()

        inventory.clear_selection()

        return AdventureInteractionOutcome(
            consumed=True,
            message="Item selection cleared.",
        )

    def select_or_combine_inventory_item(
        self,
        clicked_item: Item,
    ) -> AdventureInteractionOutcome:
        """Select, deselect, or combine an inventory item."""
        inventory = self.game_state.inventory
        selected_item = inventory.selected_item

        if selected_item is None:
            inventory.select(clicked_item.item_id)

            return AdventureInteractionOutcome(
                consumed=True,
                message=f"Selected {clicked_item.name}. Click another item to combine them.",
            )

        if selected_item.item_id == clicked_item.item_id:
            inventory.clear_selection()

            return AdventureInteractionOutcome(
                consumed=True,
                message=f"Deselected {clicked_item.name}.",
            )

        result = combine_inventory_items(
            inventory=inventory,
            recipe_book=self.recipe_book,
            first_item_id=selected_item.item_id,
            second_item_id=clicked_item.item_id,
        )

        return AdventureInteractionOutcome(
            consumed=True,
            message=result.message,
        )

    def collect_item(
        self,
        item_hotspot: ItemHotspot,
    ) -> AdventureInteractionOutcome:
        """Collect a pickup and record it as collected in persistent world state."""
        if self.game_state.has_collected_pickup(item_hotspot.pickup_id):
            return AdventureInteractionOutcome()

        inventory = self.game_state.inventory
        was_added = inventory.add(item_hotspot.item)

        self.game_state.collect_pickup(item_hotspot.pickup_id)

        if was_added:
            message = item_hotspot.pickup_text
        else:
            message = f"You already have {item_hotspot.item.name}."

        return AdventureInteractionOutcome(
            consumed=True,
            message=message,
        )

    def interact_with_npc(
        self,
        npc: NPC,
    ) -> AdventureInteractionOutcome:
        """Talk to an NPC or use the selected inventory item on them."""
        if self.game_state.inventory.selected_item is not None:
            return self.use_selected_item(npc.item_use)

        return AdventureInteractionOutcome(
            consumed=True,
            speaker_name=npc.name,
            dialogue_lines=npc.dialogue_for(
                self.game_state.has_flag,
                self.game_state.has_completed_interaction,
            ),
        )

    def interact_with_hotspot(
        self,
        hotspot: Hotspot,
    ) -> AdventureInteractionOutcome:
        """Inspect a hotspot or use the selected inventory item on it."""
        if self.game_state.inventory.selected_item is not None:
            return self.use_selected_item(hotspot.item_use)

        return AdventureInteractionOutcome(
            consumed=True,
            message=hotspot.inspect_text_for(
                self.game_state.has_flag,
                self.game_state.has_completed_interaction,
            ),
        )

    def interact_with_exit(
        self,
        exit_hotspot: ExitHotspot,
    ) -> AdventureInteractionOutcome:
        """Use an exit, unlock it with an item, or return its locked message."""
        if (
            self.game_state.inventory.selected_item is not None
            and exit_hotspot.item_use is not None
        ):
            return self.use_selected_item(exit_hotspot.item_use)

        required_flag = exit_hotspot.required_flag

        if required_flag is not None and not self.game_state.has_flag(required_flag):
            return AdventureInteractionOutcome(
                consumed=True,
                message=exit_hotspot.locked_text,
            )

        if exit_hotspot.completion_flag is not None:
            self.game_state.set_flag(exit_hotspot.completion_flag)

        return AdventureInteractionOutcome(
            consumed=True,
            target_scene_id=exit_hotspot.target_scene_id,
        )

    def use_selected_item(
        self,
        interaction: ItemUseInteraction | None,
    ) -> AdventureInteractionOutcome:
        """Use the selected inventory item on a target interaction."""
        inventory = self.game_state.inventory
        selected_item = inventory.selected_item

        if selected_item is None:
            return AdventureInteractionOutcome()

        if interaction is None:
            return AdventureInteractionOutcome(
                consumed=True,
                message=f"{selected_item.name} does not seem useful here.",
            )

        is_completed = interaction.has_been_completed(
            self.game_state.has_flag,
            self.game_state.has_completed_interaction,
        )
        result = interaction.attempt(
            selected_item.item_id,
            is_completed=is_completed,
        )

        if not result.success:
            return AdventureInteractionOutcome(
                consumed=True,
                message=result.message,
            )

        if (
            result.result_item is not None
            and inventory.contains(result.result_item.item_id)
        ):
            inventory.clear_selection()

            return AdventureInteractionOutcome(
                consumed=True,
                message=f"You already have {result.result_item.name}.",
            )

        for flag in result.flags_to_set:
            self.game_state.set_flag(flag)

        if interaction.interaction_id is not None:
            self.game_state.complete_interaction(interaction.interaction_id)

        if result.consume_item:
            inventory.remove(selected_item.item_id)
        else:
            inventory.clear_selection()

        if result.result_item is not None:
            inventory.add(result.result_item)

        return AdventureInteractionOutcome(
            consumed=True,
            message=result.message,
        )
