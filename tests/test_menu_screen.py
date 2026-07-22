import pygame

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


def test_menu_quit_button_works_with_keyboard() -> None:
    menu = create_menu()

    menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        FIXED_SURFACE_SIZE,
    )
    action = menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN),
        FIXED_SURFACE_SIZE,
    )

    assert action is MenuAction.QUIT


def test_menu_escape_quits() -> None:
    menu = create_menu()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    assert menu.handle_event(event, FIXED_SURFACE_SIZE) is MenuAction.QUIT
