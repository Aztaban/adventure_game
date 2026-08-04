import pygame
import pytest

from game.input.bindings import InputAction, input_summary_for
from game.ui.menu_screen import MenuAction, MenuScreen

FIXED_SURFACE_SIZE = (1280, 720)


def create_menu() -> MenuScreen:
    """Create a deterministic menu for input tests."""
    return MenuScreen(
        title="Test Menu",
        subtitle="Choose an action.",
        primary_label="Start",
    )


def test_menu_layout_matches_fixed_resolution_baseline() -> None:
    primary, quit_button = create_menu().layout(FIXED_SURFACE_SIZE)

    assert primary.rect == pygame.Rect(470, 430, 340, 64)
    assert quit_button.rect == pygame.Rect(470, 512, 340, 64)


def test_menu_primary_button_works_with_mouse() -> None:
    menu = create_menu()
    primary = menu.layout(FIXED_SURFACE_SIZE)[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=primary.rect.center,
    )

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is MenuAction.PRIMARY


def test_menu_quit_button_works_with_mouse() -> None:
    menu = create_menu()
    quit_button = menu.layout(FIXED_SURFACE_SIZE)[1]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=quit_button.rect.center,
    )

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is MenuAction.QUIT


def test_menu_ignores_mouse_click_outside_fixed_resolution_buttons() -> None:
    menu = create_menu()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(469, 430),
    )

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is None


@pytest.mark.parametrize("key", [pygame.K_DOWN, pygame.K_s])
def test_menu_down_bindings_select_quit(key: int) -> None:
    menu = create_menu()

    action = menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=key),
        FIXED_SURFACE_SIZE,
    )

    assert action is None
    assert menu.selected_index == 1


@pytest.mark.parametrize("key", [pygame.K_UP, pygame.K_w])
def test_menu_up_bindings_wrap_to_quit(key: int) -> None:
    menu = create_menu()

    action = menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=key),
        FIXED_SURFACE_SIZE,
    )

    assert action is None
    assert menu.selected_index == 1


@pytest.mark.parametrize(
    "key",
    [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE],
)
def test_menu_confirm_bindings_activate_selected_action(key: int) -> None:
    menu = create_menu()
    menu.selected_index = 1

    action = menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=key),
        FIXED_SURFACE_SIZE,
    )

    assert action is MenuAction.QUIT


def test_menu_escape_quits() -> None:
    menu = create_menu()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is MenuAction.QUIT


def test_menu_ignores_non_interactive_pointer_click() -> None:
    menu = create_menu()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=None,
    )

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is None


def test_title_menu_layout_includes_controls_without_changing_two_button_layout() -> None:
    menu = MenuScreen(
        title="Title",
        subtitle="Choose an action.",
        primary_label="Start Game",
        secondary_label="Controls",
    )

    start, controls, quit_button = menu.layout(FIXED_SURFACE_SIZE)

    assert start.action is MenuAction.PRIMARY
    assert start.rect == pygame.Rect(470, 390, 340, 64)
    assert controls.action is MenuAction.CONTROLS
    assert controls.rect == pygame.Rect(470, 472, 340, 64)
    assert quit_button.action is MenuAction.QUIT
    assert quit_button.rect == pygame.Rect(470, 554, 340, 64)


def test_title_controls_button_works_with_mouse() -> None:
    menu = MenuScreen(
        title="Title",
        subtitle="Choose an action.",
        primary_label="Start Game",
        secondary_label="Controls",
    )
    controls = menu.layout(FIXED_SURFACE_SIZE)[1]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=controls.rect.center,
    )

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is MenuAction.CONTROLS


def test_menu_runtime_hint_is_derived_from_binding_catalog() -> None:
    expected = (
        f"Navigate: {input_summary_for(InputAction.MENU_UP, InputAction.MENU_DOWN)}"
        f" | Select: {input_summary_for(InputAction.PRIMARY, InputAction.MENU_CONFIRM)}"
        f" | Quit: {input_summary_for(InputAction.CANCEL)}"
    )

    assert MenuScreen.input_hint() == expected
