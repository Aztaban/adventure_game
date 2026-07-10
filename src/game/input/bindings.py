from __future__ import annotations

import pygame

PRIMARY_ACTION_BUTTON = 1

DIALOGUE_ADVANCE_KEYS = frozenset(
    {
        pygame.K_SPACE,
        pygame.K_RETURN,
        pygame.K_KP_ENTER,
    }
)

CANCEL_KEY = pygame.K_ESCAPE
NEW_GAME_KEY = pygame.K_n


def is_primary_action(event: pygame.event.Event) -> bool:
    """Return whether an event is the primary mouse action."""
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == PRIMARY_ACTION_BUTTON


def is_dialogue_advance(event: pygame.event.Event) -> bool:
    """Return whether an event should advance active dialogue."""
    return event.type == pygame.KEYDOWN and event.key in DIALOGUE_ADVANCE_KEYS


def is_cancel(event: pygame.event.Event) -> bool:
    """Return whether an event is the cancel action."""
    return event.type == pygame.KEYDOWN and event.key == CANCEL_KEY

def is_new_game(event: pygame.event.Event) -> bool:
    """Return whether an event requests a fresh new game session."""
    return event.type == pygame.KEYDOWN and event.key == NEW_GAME_KEY
