import pygame

from game.ui.menu_screen import MenuAction, MenuScreen


def create_menu() -> MenuScreen:
    """Create a deterministic menu for input tests."""
    return MenuScreen(
        title="Test Menu",
        subtitle="Choose an action.",
        primary_label="Start",
    )


def test_menu_primary_button_works_with_mouse() -> None:
    menu = create_menu()
    primary = menu.layout((1280, 720))[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=primary.rect.center,
    )

    assert menu.handle_event(event, (1280, 720)) is MenuAction.PRIMARY


def test_menu_quit_button_works_with_keyboard() -> None:
    menu = create_menu()

    menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        (1280, 720),
    )
    action = menu.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN),
        (1280, 720),
    )

    assert action is MenuAction.QUIT


def test_menu_escape_quits() -> None:
    menu = create_menu()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    assert menu.handle_event(event, (1280, 720)) is MenuAction.QUIT
