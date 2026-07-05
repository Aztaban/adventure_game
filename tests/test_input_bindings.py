import pygame

from game.input.bindings import (
    is_cancel,
    is_dialogue_advance,
    is_primary_action,
)


def test_primary_action_accepts_left_mouse_button() -> None:
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(100, 100),
    )

    assert is_primary_action(event)


def test_primary_action_rejects_right_mouse_button() -> None:
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=3,
        pos=(100, 100),
    )

    assert not is_primary_action(event)


def test_dialogue_advance_accepts_space() -> None:
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

    assert is_dialogue_advance(event)


def test_cancel_accepts_escape() -> None:
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    assert is_cancel(event)
