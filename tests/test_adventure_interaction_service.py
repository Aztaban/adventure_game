import pygame

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item import Item
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.systems.adventure_interaction_service import AdventureInteractionService
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import Recipe, RecipeBook


def create_item(
    item_id: str,
    name: str,
) -> Item:
    """Create a test item definition."""
    return Item(
        item_id=item_id,
        name=name,
        description="A test item.",
    )


def create_service(
    game_state: GameState,
    recipe_book: RecipeBook | None = None,
) -> AdventureInteractionService:
    """Create an interaction service for tests."""
    return AdventureInteractionService(
        game_state=game_state,
        recipe_book=recipe_book or RecipeBook(),
    )


def test_service_selects_deselects_and_combines_inventory_items() -> None:
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
    game_state = GameState()
    service = create_service(game_state, recipe_book)
    game_state.inventory.add(first_item)
    game_state.inventory.add(second_item)

    select_outcome = service.select_or_combine_inventory_item(first_item)
    deselect_outcome = service.select_or_combine_inventory_item(first_item)
    service.select_or_combine_inventory_item(first_item)
    combine_outcome = service.select_or_combine_inventory_item(second_item)

    assert select_outcome.consumed
    assert select_outcome.message == "Selected First Item. Click another item to combine them."
    assert deselect_outcome.consumed
    assert deselect_outcome.message == "Deselected First Item."
    assert combine_outcome.consumed
    assert combine_outcome.message == "Combination succeeded."
    assert not game_state.inventory.contains(first_item.item_id)
    assert not game_state.inventory.contains(second_item.item_id)
    assert game_state.inventory.contains(result_item.item_id)


def test_service_collects_pickup_once() -> None:
    item = create_item("cup", "Cup")
    item_hotspot = ItemHotspot(
        pickup_id="pickup.test.cup",
        rect=pygame.Rect(0, 0, 10, 10),
        item=item,
        pickup_text="You pick up the cup.",
    )
    game_state = GameState()
    service = create_service(game_state)

    first_outcome = service.collect_item(item_hotspot)
    second_outcome = service.collect_item(item_hotspot)

    assert first_outcome.consumed
    assert first_outcome.message == "You pick up the cup."
    assert game_state.inventory.contains(item.item_id)
    assert game_state.has_collected_pickup(item_hotspot.pickup_id)
    assert not second_outcome.consumed
    assert second_outcome.message is None
    assert len(game_state.inventory) == 1


def test_service_inspects_hotspot_without_rendering() -> None:
    hotspot = Hotspot(
        rect=pygame.Rect(0, 0, 10, 10),
        label="Old Sign",
        inspect_text="The sign is old.",
    )
    service = create_service(GameState())

    outcome = service.interact_with_hotspot(hotspot)

    assert outcome.consumed
    assert outcome.message == "The sign is old."


def test_service_returns_npc_dialogue_outcome_without_opening_dialogue_ui() -> None:
    npc = NPC(
        rect=pygame.Rect(0, 0, 10, 10),
        name="Guide",
        dialogue_lines=("Hello.", "Good luck."),
    )
    service = create_service(GameState())

    outcome = service.interact_with_npc(npc)

    assert outcome.consumed
    assert outcome.speaker_name == "Guide"
    assert outcome.dialogue_lines == ("Hello.", "Good luck.")
    assert outcome.message is None


def test_service_uses_correct_item_on_hotspot_and_updates_state() -> None:
    correct_item = create_item("key", "Key")
    interaction = ItemUseInteraction(
        required_item_id=correct_item.item_id,
        success_text="The lock opens.",
        failure_text="That does not fit.",
        completed_text="The lock is already open.",
        interaction_id="interaction.test.lock",
    )
    hotspot = Hotspot(
        rect=pygame.Rect(0, 0, 10, 10),
        label="Lock",
        inspect_text="A locked box.",
        item_use=interaction,
    )
    game_state = GameState()
    service = create_service(game_state)
    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)

    outcome = service.interact_with_hotspot(hotspot)

    assert outcome.consumed
    assert outcome.message == "The lock opens."
    assert game_state.has_completed_interaction("interaction.test.lock")
    assert game_state.inventory.contains(correct_item.item_id)
    assert game_state.inventory.selected_item is None


def test_service_wrong_item_on_npc_does_not_mutate_state() -> None:
    wrong_item = create_item("wrong", "Wrong Item")
    interaction = ItemUseInteraction(
        required_item_id="correct",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test.npc",
    )
    npc = NPC(
        rect=pygame.Rect(0, 0, 10, 10),
        name="Guide",
        dialogue_lines=("Hello.",),
        item_use=interaction,
    )
    game_state = GameState()
    service = create_service(game_state)
    game_state.inventory.add(wrong_item)
    game_state.inventory.select(wrong_item.item_id)

    outcome = service.interact_with_npc(npc)

    assert outcome.consumed
    assert outcome.message == "Failure."
    assert not game_state.has_completed_interaction("interaction.test.npc")
    assert game_state.inventory.contains(wrong_item.item_id)
    assert game_state.inventory.selected_item is wrong_item


def test_service_target_without_item_use_returns_generic_message() -> None:
    selected_item = create_item("rock", "Rock")
    hotspot = Hotspot(
        rect=pygame.Rect(0, 0, 10, 10),
        label="Door",
        inspect_text="A plain door.",
    )
    game_state = GameState()
    service = create_service(game_state)
    game_state.inventory.add(selected_item)
    game_state.inventory.select(selected_item.item_id)

    outcome = service.interact_with_hotspot(hotspot)

    assert outcome.consumed
    assert outcome.message == "Rock does not seem useful here."
    assert game_state.inventory.selected_item is selected_item


def test_service_locked_exit_returns_message_without_transition() -> None:
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(0, 0, 10, 10),
        target_scene_id="next_scene",
        label="Exit",
        required_flag="door_open",
        locked_text="The door is locked.",
        completion_flag="left_scene",
    )
    game_state = GameState()
    service = create_service(game_state)

    outcome = service.interact_with_exit(exit_hotspot)

    assert outcome.consumed
    assert outcome.message == "The door is locked."
    assert outcome.target_scene_id is None
    assert not game_state.has_flag("left_scene")


def test_service_unlocked_exit_returns_transition_and_sets_completion_flag() -> None:
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(0, 0, 10, 10),
        target_scene_id="next_scene",
        label="Exit",
        required_flag="door_open",
        completion_flag="left_scene",
    )
    game_state = GameState()
    service = create_service(game_state)
    game_state.set_flag("door_open")

    outcome = service.interact_with_exit(exit_hotspot)

    assert outcome.consumed
    assert outcome.message is None
    assert outcome.target_scene_id == "next_scene"
    assert game_state.has_flag("left_scene")
