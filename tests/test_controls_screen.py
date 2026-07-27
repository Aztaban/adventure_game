import pygame
import pytest

from game.input.bindings import InputAction, binding_for
from game.settings import LOGICAL_SIZE
from game.ui.controls_screen import ControlsResult, ControlsScreen
from game.ui.resources import UIResources

pygame.font.init()


def test_controls_rows_use_the_complete_authoritative_binding_catalog() -> None:
    screen = ControlsScreen()
    rows = screen.binding_rows()

    assert [row.action for row in rows] == list(ControlsScreen.ACTION_ORDER)
    assert {row.action for row in rows} == set(InputAction)

    for row in rows:
        binding = binding_for(row.action)
        assert row.action_label == binding.display_name
        assert row.input_summary == binding.input_summary


def test_controls_back_button_has_fixed_logical_geometry() -> None:
    screen = ControlsScreen()

    assert screen.back_button_rect(LOGICAL_SIZE) == pygame.Rect(500, 592, 280, 58)


@pytest.mark.parametrize(
    "key",
    [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE],
)
def test_controls_keyboard_back_inputs_return_semantic_result(key: int) -> None:
    screen = ControlsScreen()
    event = pygame.event.Event(pygame.KEYDOWN, key=key)

    assert screen.handle_event(event, LOGICAL_SIZE) is ControlsResult.BACK


@pytest.mark.parametrize("key", [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s])
def test_controls_navigation_keeps_back_selected(key: int) -> None:
    screen = ControlsScreen()
    screen.back_selected = False
    event = pygame.event.Event(pygame.KEYDOWN, key=key)

    assert screen.handle_event(event, LOGICAL_SIZE) is None
    assert screen.back_selected


def test_controls_back_button_works_with_mouse() -> None:
    screen = ControlsScreen()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=screen.back_button_rect(LOGICAL_SIZE).center,
    )

    assert screen.handle_event(event, LOGICAL_SIZE) is ControlsResult.BACK


def test_controls_ignores_mouse_click_outside_back_button() -> None:
    screen = ControlsScreen()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(100, 100),
    )

    assert screen.handle_event(event, LOGICAL_SIZE) is None


def test_controls_ignores_non_interactive_pointer_position() -> None:
    screen = ControlsScreen()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=None,
    )

    assert screen.handle_event(event, LOGICAL_SIZE) is None


def test_controls_draws_at_logical_resolution() -> None:
    screen = ControlsScreen()
    surface = pygame.Surface(LOGICAL_SIZE)

    screen.draw(surface, UIResources())
