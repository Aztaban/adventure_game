import pygame
import pytest

from game.input.bindings import (
    INPUT_BINDINGS,
    InputAction,
    actions_for_event,
    binding_for,
    input_summary_for,
)


@pytest.mark.parametrize(
    ("event", "expected_actions"),
    [
        (
            pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                button=1,
                pos=(100, 100),
            ),
            {InputAction.PRIMARY},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE),
            {InputAction.CANCEL},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE),
            {InputAction.DIALOGUE_ADVANCE, InputAction.MENU_CONFIRM},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN),
            {InputAction.DIALOGUE_ADVANCE, InputAction.MENU_CONFIRM},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_KP_ENTER),
            {InputAction.DIALOGUE_ADVANCE, InputAction.MENU_CONFIRM},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP),
            {InputAction.MENU_UP},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w),
            {InputAction.MENU_UP},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
            {InputAction.MENU_DOWN},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s),
            {InputAction.MENU_DOWN},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_n),
            {InputAction.NEW_GAME},
        ),
        (
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11),
            {InputAction.FULLSCREEN_TOGGLE},
        ),
    ],
)
def test_current_physical_inputs_translate_to_semantic_actions(
    event: pygame.event.Event,
    expected_actions: set[InputAction],
) -> None:
    assert actions_for_event(event) == frozenset(expected_actions)


def test_unbound_input_translates_to_no_actions() -> None:
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=3,
        pos=(100, 100),
    )

    assert actions_for_event(event) == frozenset()


def test_binding_catalog_covers_the_complete_action_vocabulary() -> None:
    assert set(INPUT_BINDINGS) == set(InputAction)


@pytest.mark.parametrize(
    ("action", "display_name", "input_summary"),
    [
        (InputAction.PRIMARY, "Interact / select", "Left Click"),
        (InputAction.CANCEL, "Cancel / back", "Esc"),
        (
            InputAction.DIALOGUE_ADVANCE,
            "Advance dialogue",
            "Space / Enter / Numpad Enter",
        ),
        (InputAction.MENU_UP, "Menu up", "Up Arrow / W"),
        (InputAction.MENU_DOWN, "Menu down", "Down Arrow / S"),
        (
            InputAction.MENU_CONFIRM,
            "Confirm menu",
            "Enter / Numpad Enter / Space",
        ),
        (InputAction.NEW_GAME, "Start a fresh game", "N"),
        (InputAction.FULLSCREEN_TOGGLE, "Toggle fullscreen", "F11"),
    ],
)
def test_player_facing_control_text_comes_from_the_binding_catalog(
    action: InputAction,
    display_name: str,
    input_summary: str,
) -> None:
    binding = binding_for(action)

    assert binding.display_name == display_name
    assert binding.input_summary == input_summary


def test_primary_action_ignores_non_interactive_pointer_position() -> None:
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=None,
    )

    assert actions_for_event(event) == frozenset()


def test_input_summary_for_combines_catalog_labels_without_duplicates() -> None:
    assert input_summary_for(
        InputAction.PRIMARY,
        InputAction.DIALOGUE_ADVANCE,
        InputAction.MENU_CONFIRM,
    ) == "Left Click / Space / Enter / Numpad Enter"
