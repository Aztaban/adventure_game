from __future__ import annotations

import pygame

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.npc import NPC
from game.input.bindings import (
    is_cancel,
    is_dialogue_advance,
    is_primary_action,
)
from game.scene_event_result import SceneEventResult
from game.scenes.base_scene import BaseScene
from game.systems.dialogue import Dialogue
from game.theme import (
    BORDER_DEFAULT,
    PANEL_BACKGROUND,
    TEXT_HIGHLIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from game.ui.dialogue_box import DialogueBox


class AdventureScene(BaseScene):
    """Adventure scene with exits, hotspots, NPCs, and dialogue."""

    def __init__(
        self,
        name: str,
        description: str,
        background_color: tuple[int, int, int],
        exits: list[ExitHotspot],
        hotspots: list[Hotspot],
        npcs: list[NPC],
    ) -> None:
        self.name = name
        self.description = description
        self.background_color = background_color
        self.exits = exits
        self.hotspots = hotspots
        self.npcs = npcs

        self.interaction_text: str | None = None
        self.active_speaker_name = ""

        self.dialogue = Dialogue()
        self.dialogue_box = DialogueBox()

        self.title_font = pygame.font.Font(None, 52)
        self.body_font = pygame.font.Font(None, 30)

    def handle_event(self, event: pygame.event.Event) -> SceneEventResult:
        """Handle dialogue, NPC, exit, and hotspot interactions."""
        if self.dialogue.is_active:
            return self._handle_dialogue_event(event)

        if not is_primary_action(event):
            return SceneEventResult()

        npc = self._find_npc(event.pos)

        if npc is not None:
            self.active_speaker_name = npc.name
            self.dialogue.start(npc.dialogue_lines)
            self.interaction_text = None
            return SceneEventResult(consumed=True)

        for exit_hotspot in self.exits:
            if exit_hotspot.contains_point(event.pos):
                return SceneEventResult(
                    consumed=True,
                    target_scene_id=exit_hotspot.target_scene_id,
                )

        hotspot = self._find_hotspot(event.pos)

        if hotspot is not None:
            self.interaction_text = hotspot.inspect_text
            return SceneEventResult(consumed=True)

        return SceneEventResult()

    def update(self, delta_time: float) -> None:
        """Update the scene."""
        del delta_time

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the complete scene."""
        surface.fill(self.background_color)

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

        mouse_position = pygame.mouse.get_pos()
        hovered_hotspot = self._find_hotspot(mouse_position)
        hovered_npc = self._find_npc(mouse_position)

        for hotspot in self.hotspots:
            hotspot.draw(
                surface,
                self.body_font,
                is_hovered=hotspot is hovered_hotspot,
            )

        for npc in self.npcs:
            npc.draw(
                surface,
                self.body_font,
                is_hovered=npc is hovered_npc,
            )

        for exit_hotspot in self.exits:
            exit_hotspot.draw(surface, self.body_font)

        self._draw_hover_text(
            surface,
            hovered_npc,
            hovered_hotspot,
        )
        self._draw_interaction_text(surface)

        current_line = self.dialogue.current_line

        if current_line is not None:
            self.dialogue_box.draw(
                surface,
                speaker_name=self.active_speaker_name,
                text=current_line,
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

    def _draw_hover_text(
        self,
        surface: pygame.Surface,
        hovered_npc: NPC | None,
        hovered_hotspot: Hotspot | None,
    ) -> None:
        """Draw information for the currently hovered entity."""
        hover_text: str | None = None

        if hovered_npc is not None:
            hover_text = f"Talk to: {hovered_npc.name}"
        elif hovered_hotspot is not None:
            hover_text = f"Inspect: {hovered_hotspot.label}"

        if hover_text is None:
            return

        hover_surface = self.body_font.render(
            hover_text,
            True,
            TEXT_HIGHLIGHT,
        )
        surface.blit(hover_surface, (40, 150))

    def _draw_interaction_text(self, surface: pygame.Surface) -> None:
        """Draw the most recent hotspot inspection result."""
        if self.interaction_text is None or self.dialogue.is_active:
            return

        interaction_surface = self.body_font.render(
            self.interaction_text,
            True,
            TEXT_PRIMARY,
        )
        interaction_rect = interaction_surface.get_rect(
            center=(
                surface.get_width() // 2,
                surface.get_height() - 80,
            )
        )
        background_rect = interaction_rect.inflate(40, 24)

        pygame.draw.rect(
            surface,
            PANEL_BACKGROUND,
            background_rect,
            border_radius=8,
        )
        pygame.draw.rect(
            surface,
            BORDER_DEFAULT,
            background_rect,
            width=2,
            border_radius=8,
        )

        surface.blit(interaction_surface, interaction_rect)

    def _find_hotspot(
        self,
        position: tuple[int, int],
    ) -> Hotspot | None:
        """Return the hotspot at a position."""
        for hotspot in self.hotspots:
            if hotspot.contains_point(position):
                return hotspot

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
