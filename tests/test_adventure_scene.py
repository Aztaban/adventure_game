import pygame

from game.entities.hotspot import Hotspot
from game.entities.item import Item
from game.entities.npc import NPC
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.settings import WINDOW_WIDTH
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import Recipe, RecipeBook
from game.ui.inventory_bar import InventoryBar

pygame.font.init()


def create_test_scene(
    game_state: GameState,
    hotspots: list[Hotspot] | None = None,
    npcs: list[NPC] | None = None,
) -> AdventureScene:
    """Create a minimal AdventureScene for behavioral tests."""
    return AdventureScene(
        name="Test Scene",
        description="A scene used by automated tests.",
        background_color=(0, 0, 0),
        exits=[],
        hotspots=hotspots or [],
        item_hotspots=[],
        npcs=npcs or [],
        game_state=game_state,
    )


def create_item(
    item_id: str,
    name: str = "Test Item",
) -> Item:
    """Create a test inventory item."""
    return Item(
        item_id=item_id,
        name=name,
        description="An item used by automated tests.",
    )


def test_escape_clears_selected_inventory_item() -> None:
    game_state = GameState()
    item = create_item("selected_item")

    game_state.inventory.add(item)
    game_state.inventory.select(item.item_id)

    scene = create_test_scene(game_state)
    event = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_ESCAPE,
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "Item selection cleared."


def test_escape_is_not_consumed_when_nothing_is_active() -> None:
    game_state = GameState()
    scene = create_test_scene(game_state)
    event = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_ESCAPE,
    )

    result = scene.handle_event(event)

    assert not result.consumed


def test_escape_closes_active_dialogue() -> None:
    game_state = GameState()
    npc = NPC(
        rect=pygame.Rect(100, 100, 120, 120),
        name="Test NPC",
        dialogue_lines=("First line.", "Second line."),
    )
    scene = create_test_scene(
        game_state,
        npcs=[npc],
    )

    click_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(110, 110),
    )
    escape_event = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_ESCAPE,
    )

    scene.handle_event(click_event)
    result = scene.handle_event(escape_event)

    assert result.consumed
    assert not scene.dialogue.is_active


def test_wrong_item_does_not_complete_hotspot_interaction() -> None:
    game_state = GameState()
    wrong_item = create_item("wrong_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
    )
    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        label="Test Hotspot",
        inspect_text="Inspect text.",
        item_use=interaction,
    )

    game_state.inventory.add(wrong_item)
    game_state.inventory.select(wrong_item.item_id)

    scene = create_test_scene(
        game_state,
        hotspots=[hotspot],
    )
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(110, 110),
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert not interaction.is_completed
    assert game_state.inventory.selected_item is wrong_item
    assert scene.interaction_text == "Failure."


def test_correct_item_completes_hotspot_interaction() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
    )
    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        label="Test Hotspot",
        inspect_text="Inspect text.",
        item_use=interaction,
    )

    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)

    scene = create_test_scene(
        game_state,
        hotspots=[hotspot],
    )
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(110, 110),
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert interaction.is_completed
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "Success."


def test_consumed_item_is_removed_after_success() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        consume_item=True,
    )
    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        label="Test Hotspot",
        inspect_text="Inspect text.",
        item_use=interaction,
    )

    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)

    scene = create_test_scene(
        game_state,
        hotspots=[hotspot],
    )
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(110, 110),
    )

    scene.handle_event(event)

    assert interaction.is_completed
    assert not game_state.inventory.contains(correct_item.item_id)
    assert game_state.inventory.selected_item is None


def get_second_inventory_row_position() -> tuple[int, int]:
    """Return a position inside the second inventory row."""
    panel_left = WINDOW_WIDTH - InventoryBar.PANEL_WIDTH - InventoryBar.PANEL_MARGIN

    return (
        panel_left + InventoryBar.INNER_PADDING + 5,
        InventoryBar.PANEL_MARGIN + InventoryBar.ITEM_START_OFFSET + InventoryBar.ROW_HEIGHT + 5,
    )


def test_inventory_items_combine_into_recipe_result() -> None:
    first_item = create_item("first", "First Item")
    second_item = create_item("second", "Second Item")
    result_item = create_item("result", "Result Item")

    recipe_book = RecipeBook(
        [
            Recipe(
                first_item_id=first_item.item_id,
                second_item_id=second_item.item_id,
                result_item=result_item,
                success_text="Combination succeeded.",
            )
        ]
    )
    game_state = GameState(recipe_book=recipe_book)

    game_state.inventory.add(first_item)
    game_state.inventory.add(second_item)
    game_state.inventory.select(first_item.item_id)

    scene = create_test_scene(game_state)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=get_second_inventory_row_position(),
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert not game_state.inventory.contains(first_item.item_id)
    assert not game_state.inventory.contains(second_item.item_id)
    assert game_state.inventory.contains(result_item.item_id)
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "Combination succeeded."


def test_invalid_combination_keeps_both_items() -> None:
    first_item = create_item("first", "First Item")
    second_item = create_item("second", "Second Item")
    game_state = GameState()

    game_state.inventory.add(first_item)
    game_state.inventory.add(second_item)
    game_state.inventory.select(first_item.item_id)

    scene = create_test_scene(game_state)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=get_second_inventory_row_position(),
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert game_state.inventory.contains(first_item.item_id)
    assert game_state.inventory.contains(second_item.item_id)
    assert game_state.inventory.selected_item is first_item
    assert scene.interaction_text == ("First Item and Second Item do not combine.")
