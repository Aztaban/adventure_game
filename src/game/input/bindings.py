from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

import pygame


class InputAction(Enum):
    """Semantic actions understood by the current game and menus."""

    PRIMARY = "primary"
    CANCEL = "cancel"
    DIALOGUE_ADVANCE = "dialogue_advance"
    MENU_UP = "menu_up"
    MENU_DOWN = "menu_down"
    MENU_CONFIRM = "menu_confirm"
    NEW_GAME = "new_game"
    FULLSCREEN_TOGGLE = "fullscreen_toggle"


class InputTriggerKind(Enum):
    """Supported physical input trigger types."""

    KEY = "key"
    MOUSE_BUTTON = "mouse_button"


@dataclass(frozen=True)
class InputTrigger:
    """One physical input and its player-facing label."""

    kind: InputTriggerKind
    code: int
    label: str

    def matches(self, event: pygame.event.Event) -> bool:
        """Return whether a Pygame event activates this trigger."""
        if self.kind is InputTriggerKind.KEY:
            return event.type == pygame.KEYDOWN and event.key == self.code

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == self.code
            and getattr(event, "pos", None) is not None
        )


@dataclass(frozen=True)
class ActionBinding:
    """Player-facing metadata and physical triggers for one action."""

    display_name: str
    triggers: tuple[InputTrigger, ...]

    @property
    def input_labels(self) -> tuple[str, ...]:
        """Return the labels that can be shown on a Controls screen."""
        return tuple(trigger.label for trigger in self.triggers)

    @property
    def input_summary(self) -> str:
        """Return one compact player-facing binding summary."""
        return " / ".join(self.input_labels)


def _key(code: int, label: str) -> InputTrigger:
    """Create a keyboard trigger for the binding catalog."""
    return InputTrigger(InputTriggerKind.KEY, code, label)


def _mouse_button(code: int, label: str) -> InputTrigger:
    """Create a mouse-button trigger for the binding catalog."""
    return InputTrigger(InputTriggerKind.MOUSE_BUTTON, code, label)


INPUT_BINDINGS = MappingProxyType(
    {
        InputAction.PRIMARY: ActionBinding(
            display_name="Interact / select",
            triggers=(_mouse_button(1, "Left Click"),),
        ),
        InputAction.CANCEL: ActionBinding(
            display_name="Cancel / back",
            triggers=(_key(pygame.K_ESCAPE, "Esc"),),
        ),
        InputAction.DIALOGUE_ADVANCE: ActionBinding(
            display_name="Advance dialogue",
            triggers=(
                _key(pygame.K_SPACE, "Space"),
                _key(pygame.K_RETURN, "Enter"),
                _key(pygame.K_KP_ENTER, "Numpad Enter"),
            ),
        ),
        InputAction.MENU_UP: ActionBinding(
            display_name="Menu up",
            triggers=(
                _key(pygame.K_UP, "Up Arrow"),
                _key(pygame.K_w, "W"),
            ),
        ),
        InputAction.MENU_DOWN: ActionBinding(
            display_name="Menu down",
            triggers=(
                _key(pygame.K_DOWN, "Down Arrow"),
                _key(pygame.K_s, "S"),
            ),
        ),
        InputAction.MENU_CONFIRM: ActionBinding(
            display_name="Confirm menu",
            triggers=(
                _key(pygame.K_RETURN, "Enter"),
                _key(pygame.K_KP_ENTER, "Numpad Enter"),
                _key(pygame.K_SPACE, "Space"),
            ),
        ),
        InputAction.NEW_GAME: ActionBinding(
            display_name="Start a fresh game",
            triggers=(_key(pygame.K_n, "N"),),
        ),
        InputAction.FULLSCREEN_TOGGLE: ActionBinding(
            display_name="Toggle fullscreen",
            triggers=(_key(pygame.K_F11, "F11"),),
        ),
    }
)


def actions_for_event(event: pygame.event.Event) -> frozenset[InputAction]:
    """Translate one Pygame event into all matching semantic actions."""
    return frozenset(
        action
        for action, binding in INPUT_BINDINGS.items()
        if any(trigger.matches(event) for trigger in binding.triggers)
    )


def binding_for(action: InputAction) -> ActionBinding:
    """Return the authoritative binding metadata for an action."""
    return INPUT_BINDINGS[action]


def input_summary_for(*actions: InputAction) -> str:
    """Return unique player-facing input labels for one or more actions."""
    labels: list[str] = []

    for action in actions:
        for label in binding_for(action).input_labels:
            if label not in labels:
                labels.append(label)

    return " / ".join(labels)
