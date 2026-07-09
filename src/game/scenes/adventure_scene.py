from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

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


class WorldTargetKind(Enum):
    """Kinds of clickable world targets in scene priority order."""

    NPC = "npc"
    EXIT = "exit"
    ITEM_PICKUP = "item_pickup"
    HOTSPOT = "hotspot"


@dataclass(frozen=True)
class WorldTarget:
    """Tagged world target resolved from a scene position."""

    kind: WorldTargetKind
    entity: NPC | ExitHotspot | ItemHotspot | Hotspot


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

        hovered_target = self._resolve_world_target(pygame.mouse.get_pos())

        self._draw_scene_entities(
            surface=surface,
            hovered_target=hovered_target,
        )
        self._draw_hover_text(
            surface=surface,
            hovered_target=hovered_target,
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
        return self._apply_interaction_outcome(
            self.interaction_service.clear_selected_item()
        )

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
                self.interaction_service.select_or_combine_inventory_item(
                    inventory_item,
                )
            )

        target = self._resolve_world_target(position)

        if target is None:
            return SceneEventResult()

        return self._interact_with_world_target(target)

    def _interact_with_world_target(
        self,
        target: WorldTarget,
    ) -> SceneEventResult:
        """Run the interaction matching a resolved world target."""
        if target.kind is WorldTargetKind.NPC:
            assert isinstance(target.entity, NPC)

            return self._apply_interaction_outcome(
                self.interaction_service.interact_with_npc(target.entity)
            )

        if target.kind is WorldTargetKind.EXIT:
            assert isinstance(target.entity, ExitHotspot)

            return self._apply_interaction_outcome(
                self.interaction_service.interact_with_exit(target.entity)
            )

        if target.kind is WorldTargetKind.ITEM_PICKUP:
            assert isinstance(target.entity, ItemHotspot)

            return self._apply_interaction_outcome(
                self.interaction_service.collect_item(target.entity)
            )

        assert isinstance(target.entity, Hotspot)

        return self._apply_interaction_outcome(
            self.interaction_service.interact_with_hotspot(target.entity)
        )

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
            target_scene_id=outcome.target_scene_id,
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
        hovered_target: WorldTarget | None,
    ) -> None:
        """Draw scene hotspots, items, NPCs, and exits."""
        for hotspot in self.hotspots:
            hotspot.draw(
                surface,
                self.body_font,
                is_hovered=self._is_hovered_target(
                    hovered_target,
                    WorldTargetKind.HOTSPOT,
                    hotspot,
                ),
            )

        for item_hotspot in self.item_hotspots:
            if self.game_state.has_collected_pickup(item_hotspot.pickup_id):
                continue

            item_hotspot.draw(
                surface,
                self.body_font,
                is_hovered=self._is_hovered_target(
                    hovered_target,
                    WorldTargetKind.ITEM_PICKUP,
                    item_hotspot,
                ),
            )

        for npc in self.npcs:
            npc.draw(
                surface,
                self.body_font,
                is_hovered=self._is_hovered_target(
                    hovered_target,
                    WorldTargetKind.NPC,
                    npc,
                ),
            )

        for exit_hotspot in self.exits:
            required_flag = exit_hotspot.required_flag

            is_locked = required_flag is not None and not self.game_state.has_flag(required_flag)

            exit_hotspot.draw(
                surface,
                self.body_font,
                is_locked=is_locked,
                is_hovered=self._is_hovered_target(
                    hovered_target,
                    WorldTargetKind.EXIT,
                    exit_hotspot,
                ),
            )

    def _draw_hover_text(
        self,
        surface: pygame.Surface,
        hovered_target: WorldTarget | None,
    ) -> None:
        """Draw information for the currently hovered entity."""
        if self.dialogue.is_active:
            return

        hover_text = self._hover_text_for_target(hovered_target)

        if hover_text is None:
            return

        hover_surface = self.body_font.render(
            hover_text,
            True,
            TEXT_HIGHLIGHT,
        )

        surface.blit(hover_surface, (40, 150))

    def _hover_text_for_target(
        self,
        target: WorldTarget | None,
    ) -> str | None:
        """Return hover text for a resolved world target."""
        if target is None:
            return None

        selected_item = self.game_state.inventory.selected_item

        if target.kind is WorldTargetKind.NPC:
            assert isinstance(target.entity, NPC)

            if selected_item is not None:
                return f"Use {selected_item.name} on {target.entity.name}"

            return f"Talk to: {target.entity.name}"

        if target.kind is WorldTargetKind.EXIT:
            assert isinstance(target.entity, ExitHotspot)

            return f"Go to: {self._display_label_for_exit(target.entity)}"

        if target.kind is WorldTargetKind.ITEM_PICKUP:
            assert isinstance(target.entity, ItemHotspot)

            return f"Pick up: {target.entity.item.name}"

        assert isinstance(target.entity, Hotspot)

        if selected_item is not None:
            return f"Use {selected_item.name} on {target.entity.label}"

        return f"Inspect: {target.entity.label}"

    def _display_label_for_exit(
        self,
        exit_hotspot: ExitHotspot,
    ) -> str:
        """Return the exit label matching current locked state."""
        required_flag = exit_hotspot.required_flag
        is_locked = required_flag is not None and not self.game_state.has_flag(required_flag)

        if is_locked and exit_hotspot.locked_label is not None:
            return exit_hotspot.locked_label

        return exit_hotspot.label

    def _resolve_world_target(
        self,
        position: tuple[int, int],
    ) -> WorldTarget | None:
        """Return the highest-priority world target at a position."""
        for npc in self.npcs:
            if npc.contains_point(position):
                return WorldTarget(WorldTargetKind.NPC, npc)

        for exit_hotspot in self.exits:
            if exit_hotspot.contains_point(position):
                return WorldTarget(WorldTargetKind.EXIT, exit_hotspot)

        for item_hotspot in self.item_hotspots:
            if self.game_state.has_collected_pickup(item_hotspot.pickup_id):
                continue

            if item_hotspot.contains_point(position):
                return WorldTarget(WorldTargetKind.ITEM_PICKUP, item_hotspot)

        for hotspot in self.hotspots:
            if hotspot.contains_point(position):
                return WorldTarget(WorldTargetKind.HOTSPOT, hotspot)

        return None

    def _is_hovered_target(
        self,
        hovered_target: WorldTarget | None,
        target_kind: WorldTargetKind,
        entity: NPC | ExitHotspot | ItemHotspot | Hotspot,
    ) -> bool:
        """Return whether an entity matches the resolved hovered target."""
        return (
            hovered_target is not None
            and hovered_target.kind is target_kind
            and hovered_target.entity is entity
        )
