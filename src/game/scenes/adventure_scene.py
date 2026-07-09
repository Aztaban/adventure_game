from __future__ import annotations

import pygame

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.input.bindings import (
    is_cancel,
    is_dialogue_advance,
    is_primary_action,
)
from game.scene_event_result import SceneEventResult
from game.scenes.base_scene import BaseScene
from game.settings import WINDOW_WIDTH
from game.systems.adventure_interaction_service import (
    AdventureInteractionOutcome,
    AdventureInteractionService,
)
from game.systems.dialogue import Dialogue
from game.systems.recipe import RecipeBook
from game.theme import (
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from game.ui.dialogue_box import DialogueBox
from game.ui.inventory_bar import InventoryBar
from game.ui.message_box import MessageBox


class AdventureScene(BaseScene):
    """Adventure scene with exits, hotspots, NPCs, items, and dialogue."""

    def __init__(
        self,
        name: str,
        description: str,
        background_color: tuple[int, int, int],
        exits: list[ExitHotspot],
        hotspots: list[Hotspot],
        item_hotspots: list[ItemHotspot],
        npcs: list[NPC],
        game_state: GameState,
        recipe_book: RecipeBook,
    ) -> None:
        self.name = name
        self.description = description
        self.background_color = background_color

        self.exits = exits
        self.hotspots = hotspots
        self.item_hotspots = item_hotspots
        self.npcs = npcs

        self.game_state = game_state
        self.interaction_service = AdventureInteractionService(
            game_state=game_state,
            recipe_book=recipe_book,
        )
        self.interaction_text: str | None = None
        self.active_speaker_name = ""

        self.dialogue = Dialogue()
        self.dialogue_box = DialogueBox()
        self.inventory_bar = InventoryBar(WINDOW_WIDTH)
        self.message_box = MessageBox()

        self.title_font = pygame.font.Font(None, 52)
        self.body_font = pygame.font.Font(None, 30)

    def handle_event(
        self,
        event: pygame.event.Event,
    ) -> SceneEventResult:
        """Handle scene input."""
        if self.dialogue.is_active:
            return self._handle_dialogue_event(event)

        if is_cancel(event):
            return self._handle_cancel()

        if not is_primary_action(event):
            return SceneEventResult()

        return self._handle_primary_action(event.pos)

    def update(self, delta_time: float) -> None:
        """Update the scene."""
        del delta_time

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the complete scene."""
        surface.fill(self.background_color)

        self._draw_scene_header(surface)

        mouse_position = pygame.mouse.get_pos()
        hovered_hotspot = self._find_hotspot(mouse_position)
        hovered_item = self._find_item_hotspot(mouse_position)
        hovered_npc = self._find_npc(mouse_position)

        self._draw_scene_entities(
            surface=surface,
            hovered_hotspot=hovered_hotspot,
            hovered_item=hovered_item,
            hovered_npc=hovered_npc,
        )
        self._draw_hover_text(
            surface=surface,
            hovered_npc=hovered_npc,
            hovered_item=hovered_item,
            hovered_hotspot=hovered_hotspot,
        )

        inventory = self.game_state.inventory

        self.inventory_bar.draw(
            surface=surface,
            items=inventory.items,
            selected_item=inventory.selected_item,
        )

        if self.interaction_text is not None and not self.dialogue.is_active:
            self.message_box.draw(
                surface,
                self.interaction_text,
            )

        current_line = self.dialogue.current_line

        if current_line is not None:
            self.dialogue_box.draw(
                surface,
                speaker_name=self.active_speaker_name,
                text=current_line,
            )

    def _handle_cancel(self) -> SceneEventResult:
        """Clear item selection before global cancel handling."""
        return self._apply_interaction_outcome(self.interaction_service.clear_selected_item())

    def _handle_primary_action(
        self,
        position: tuple[int, int],
    ) -> SceneEventResult:
        """Handle a primary click based on its target."""
        inventory = self.game_state.inventory

        inventory_item = self.inventory_bar.item_at_position(
            position,
            inventory.items,
        )

        if inventory_item is not None:
            return self._apply_interaction_outcome(
                self.interaction_service.select_or_combine_inventory_item(inventory_item)
            )

        npc = self._find_npc(position)

        if npc is not None:
            return self._apply_interaction_outcome(self.interaction_service.interact_with_npc(npc))

        exit_hotspot = self._find_exit_hotspot(position)

        if exit_hotspot is not None:
            return self._apply_interaction_outcome(self.interaction_service.interact_with_exit(exit_hotspot))

        item_hotspot = self._find_item_hotspot(position)

        if item_hotspot is not None:
            return self._apply_interaction_outcome(self.interaction_service.collect_item(item_hotspot))

        hotspot = self._find_hotspot(position)

        if hotspot is not None:
            return self._apply_interaction_outcome(self.interaction_service.interact_with_hotspot(hotspot))

        return SceneEventResult()



    def _apply_interaction_outcome(
        self,
        outcome: AdventureInteractionOutcome,
    ) -> SceneEventResult:
        """Apply service output to scene presentation state."""
        if outcome.dialogue_lines:
            self.active_speaker_name = outcome.speaker_name or ""
            self.dialogue.start(outcome.dialogue_lines)
            self.interaction_text = None
        elif outcome.message is not None:
            self.interaction_text = outcome.message

        return SceneEventResult(
            consumed=outcome.consumed,
            target_scene_id=outcome.target_scene_id
        )

    def _handle_dialogue_event(
        self,
        event: pygame.event.Event,
    ) -> SceneEventResult:
        """Advance or close the active dialogue."""
        if is_primary_action(event) or is_dialogue_advance(event):
            self.dialogue.advance()

            return SceneEventResult(consumed=True)

        if is_cancel(event):
            self.dialogue.close()

            return SceneEventResult(consumed=True)

        return SceneEventResult()

    def _draw_scene_header(
        self,
        surface: pygame.Surface,
    ) -> None:
        """Draw the scene title and description."""
        title_surface = self.title_font.render(
            self.name,
            True,
            TEXT_PRIMARY,
        )
        description_surface = self.body_font.render(
            self.description,
            True,
            TEXT_SECONDARY,
        )

        surface.blit(title_surface, (40, 40))
        surface.blit(description_surface, (40, 100))

    def _draw_scene_entities(
        self,
        surface: pygame.Surface,
        hovered_hotspot: Hotspot | None,
        hovered_item: ItemHotspot | None,
        hovered_npc: NPC | None,
    ) -> None:
        """Draw scene hotspots, items, NPCs, and exits."""
        for hotspot in self.hotspots:
            hotspot.draw(
                surface,
                self.body_font,
                is_hovered=hotspot is hovered_hotspot,
            )

        for item_hotspot in self.item_hotspots:
            if self.game_state.has_collected_pickup(item_hotspot.pickup_id):
                continue

            item_hotspot.draw(
                surface,
                self.body_font,
                is_hovered=item_hotspot is hovered_item,
            )

        for npc in self.npcs:
            npc.draw(
                surface,
                self.body_font,
                is_hovered=npc is hovered_npc,
            )

        for exit_hotspot in self.exits:
            required_flag = exit_hotspot.required_flag

            is_locked = required_flag is not None and not self.game_state.has_flag(required_flag)

            exit_hotspot.draw(
                surface,
                self.body_font,
                is_locked=is_locked,
            )

    def _draw_hover_text(
        self,
        surface: pygame.Surface,
        hovered_npc: NPC | None,
        hovered_item: ItemHotspot | None,
        hovered_hotspot: Hotspot | None,
    ) -> None:
        """Draw information for the currently hovered entity."""
        if self.dialogue.is_active:
            return

        hover_text: str | None = None
        selected_item = self.game_state.inventory.selected_item

        if hovered_npc is not None:
            if selected_item is not None:
                hover_text = f"Use {selected_item.name} on {hovered_npc.name}"
            else:
                hover_text = f"Talk to: {hovered_npc.name}"

        elif hovered_item is not None:
            hover_text = f"Pick up: {hovered_item.item.name}"

        elif hovered_hotspot is not None:
            if selected_item is not None:
                hover_text = f"Use {selected_item.name} on {hovered_hotspot.label}"
            else:
                hover_text = f"Inspect: {hovered_hotspot.label}"

        if hover_text is None:
            return

        hover_surface = self.body_font.render(
            hover_text,
            True,
            TEXT_HIGHLIGHT,
        )

        surface.blit(hover_surface, (40, 150))

    def _find_hotspot(
        self,
        position: tuple[int, int],
    ) -> Hotspot | None:
        """Return the hotspot at a position."""
        for hotspot in self.hotspots:
            if hotspot.contains_point(position):
                return hotspot

        return None

    def _find_item_hotspot(
        self,
        position: tuple[int, int],
    ) -> ItemHotspot | None:
        """Return the collectible item at a position."""
        for item_hotspot in self.item_hotspots:
            if self.game_state.has_collected_pickup(item_hotspot.pickup_id):
                continue

            if item_hotspot.contains_point(position):
                return item_hotspot

        return None

    def _find_npc(
        self,
        position: tuple[int, int],
    ) -> NPC | None:
        """Return the NPC at a position."""
        for npc in self.npcs:
            if npc.contains_point(position):
                return npc

        return None

    def _find_exit_hotspot(
        self,
        position: tuple[int, int],
    ) -> ExitHotspot | None:
        """Return the exit hotspot at a position."""
        for exit_hotspot in self.exits:
            if exit_hotspot.contains_point(position):
                return exit_hotspot

        return None
