import pygame

from game.entities.exit_hotspot import ExitHotspot
from game.entities.hotspot import Hotspot
from game.entities.item import Item
from game.entities.item_hotspot import ItemHotspot
from game.entities.npc import NPC
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene, WorldTargetKind
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import Recipe, RecipeBook

pygame.font.init()


def create_test_scene(
    game_state: GameState,
    exits: list[ExitHotspot] | None = None,
    hotspots: list[Hotspot] | None = None,
    item_hotspots: list[ItemHotspot] | None = None,
    npcs: list[NPC] | None = None,
    recipe_book: RecipeBook | None = None,
) -> AdventureScene:
    """Create a minimal AdventureScene for behavioral tests."""
    return AdventureScene(
        name="Test Scene",
        description="A scene used by automated tests.",
        background_color=(0, 0, 0),
        exits=exits or [],
        hotspots=hotspots or [],
        item_hotspots=item_hotspots or [],
        npcs=npcs or [],
        game_state=game_state,
        recipe_book=recipe_book or RecipeBook(),
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


def get_inventory_row_position(
    scene: AdventureScene,
    row_index: int,
) -> tuple[int, int]:
    """Return the center position of an inventory item row."""
    rows = scene.inventory_bar.item_rows(scene.game_state.inventory.items)

    return rows[row_index][1].center


def create_primary_click(position: tuple[int, int]) -> pygame.event.Event:
    """Create a primary mouse click event at a position."""
    return pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=position,
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
        dialogue_lines=(
            "First line.",
            "Second line.",
        ),
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
        interaction_id="interaction.test",
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
    assert not game_state.has_completed_interaction("interaction.test")
    assert game_state.inventory.contains(wrong_item.item_id)
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
        interaction_id="interaction.test",
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
    assert game_state.has_completed_interaction("interaction.test")
    assert game_state.inventory.contains(correct_item.item_id)
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "Success."


def test_successful_item_use_records_completion_for_future_attempts() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test",
        consume_item=False,
    )
    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        label="Test Hotspot",
        inspect_text="Inspect text.",
        item_use=interaction,
    )
    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)
    scene = create_test_scene(game_state, hotspots=[hotspot])

    first_result = scene.handle_event(create_primary_click(hotspot.rect.center))
    game_state.inventory.select(correct_item.item_id)
    second_result = scene.handle_event(create_primary_click(hotspot.rect.center))

    assert first_result.consumed
    assert second_result.consumed
    assert game_state.has_completed_interaction("interaction.test")
    assert game_state.inventory.contains(correct_item.item_id)
    assert scene.interaction_text == "Already complete."


def test_consumed_item_is_removed_after_success() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")

    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test",
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

    assert game_state.has_completed_interaction("interaction.test")
    assert not game_state.inventory.contains(correct_item.item_id)
    assert game_state.inventory.selected_item is None


def test_inventory_items_combine_into_recipe_result() -> None:
    first_item = create_item(
        "first",
        "First Item",
    )
    second_item = create_item(
        "second",
        "Second Item",
    )
    result_item = create_item(
        "result",
        "Result Item",
    )

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

    game_state.inventory.add(first_item)
    game_state.inventory.add(second_item)
    game_state.inventory.select(first_item.item_id)

    scene = create_test_scene(
        game_state,
        recipe_book=recipe_book,
    )

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=get_inventory_row_position(scene, 1),
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert not game_state.inventory.contains(first_item.item_id)
    assert not game_state.inventory.contains(second_item.item_id)
    assert game_state.inventory.contains(result_item.item_id)
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "Combination succeeded."


def test_invalid_combination_keeps_both_items() -> None:
    first_item = create_item(
        "first",
        "First Item",
    )
    second_item = create_item(
        "second",
        "Second Item",
    )

    game_state = GameState()

    game_state.inventory.add(first_item)
    game_state.inventory.add(second_item)
    game_state.inventory.select(first_item.item_id)

    scene = create_test_scene(game_state)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=get_inventory_row_position(scene, 1),
    )

    result = scene.handle_event(event)

    assert result.consumed
    assert game_state.inventory.contains(first_item.item_id)
    assert game_state.inventory.contains(second_item.item_id)
    assert game_state.inventory.selected_item is first_item
    assert scene.interaction_text == ("First Item and Second Item do not combine.")


def test_pickup_adds_item_and_records_collected_state() -> None:
    game_state = GameState()
    item = create_item("pickup", "Pickup Item")
    pickup = ItemHotspot(
        pickup_id="pickup.test",
        rect=pygame.Rect(100, 100, 120, 80),
        item=item,
        pickup_text="Item collected.",
    )
    scene = create_test_scene(
        game_state,
        item_hotspots=[pickup],
    )

    result = scene.handle_event(create_primary_click(pickup.rect.center))

    assert result.consumed
    assert game_state.inventory.contains(item.item_id)
    assert pickup in scene.item_hotspots
    assert game_state.has_collected_pickup(pickup.pickup_id)
    assert scene.interaction_text == "Item collected."


def test_collected_pickup_cannot_be_collected_repeatedly() -> None:
    game_state = GameState()
    item = create_item("pickup", "Pickup Item")
    pickup = ItemHotspot(
        pickup_id="pickup.test",
        rect=pygame.Rect(100, 100, 120, 80),
        item=item,
        pickup_text="Item collected.",
    )
    scene = create_test_scene(
        game_state,
        item_hotspots=[pickup],
    )
    click = create_primary_click(pickup.rect.center)

    first_result = scene.handle_event(click)
    second_result = scene.handle_event(click)

    assert first_result.consumed
    assert not second_result.consumed
    assert len(game_state.inventory) == 1
    assert scene.item_hotspots == [pickup]
    assert game_state.has_collected_pickup(pickup.pickup_id)


def test_duplicate_pickup_keeps_existing_item_and_records_pickup() -> None:
    game_state = GameState()
    existing_item = create_item("duplicate", "Existing Item")
    duplicate_item = create_item("duplicate", "Duplicate Item")
    pickup = ItemHotspot(
        pickup_id="pickup.test",
        rect=pygame.Rect(100, 100, 120, 80),
        item=duplicate_item,
        pickup_text="Item collected.",
    )
    game_state.inventory.add(existing_item)
    scene = create_test_scene(
        game_state,
        item_hotspots=[pickup],
    )

    result = scene.handle_event(create_primary_click(pickup.rect.center))

    assert result.consumed
    assert game_state.inventory.items == (existing_item,)
    assert pickup in scene.item_hotspots
    assert game_state.has_collected_pickup(pickup.pickup_id)
    assert scene.interaction_text == "You already have Duplicate Item."


def test_wrong_item_does_not_complete_npc_interaction() -> None:
    game_state = GameState()
    wrong_item = create_item("wrong_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test",
        consume_item=True,
    )
    npc = NPC(
        rect=pygame.Rect(100, 100, 120, 120),
        name="Test NPC",
        dialogue_lines=("Hello.",),
        item_use=interaction,
    )
    game_state.inventory.add(wrong_item)
    game_state.inventory.select(wrong_item.item_id)
    scene = create_test_scene(game_state, npcs=[npc])

    result = scene.handle_event(create_primary_click(npc.rect.center))

    assert result.consumed
    assert not game_state.has_completed_interaction("interaction.test")
    assert game_state.inventory.contains(wrong_item.item_id)
    assert game_state.inventory.selected_item is wrong_item
    assert not scene.dialogue.is_active
    assert scene.interaction_text == "Failure."


def test_correct_item_completes_npc_interaction_without_consuming_item() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test",
        consume_item=False,
    )
    npc = NPC(
        rect=pygame.Rect(100, 100, 120, 120),
        name="Test NPC",
        dialogue_lines=("Hello.",),
        item_use=interaction,
    )
    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)
    scene = create_test_scene(game_state, npcs=[npc])

    result = scene.handle_event(create_primary_click(npc.rect.center))

    assert result.consumed
    assert game_state.has_completed_interaction("interaction.test")
    assert game_state.inventory.contains(correct_item.item_id)
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "Success."


def test_completed_hotspot_interaction_returns_completed_inspection_text() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test",
    )
    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        label="Test Hotspot",
        inspect_text="Default inspection.",
        item_use=interaction,
        completed_inspect_text="Completed inspection.",
    )
    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)
    scene = create_test_scene(game_state, hotspots=[hotspot])

    scene.handle_event(create_primary_click(hotspot.rect.center))
    result = scene.handle_event(create_primary_click(hotspot.rect.center))

    assert result.consumed
    assert game_state.has_completed_interaction("interaction.test")
    assert scene.interaction_text == "Completed inspection."


def test_completed_npc_interaction_returns_completed_dialogue() -> None:
    game_state = GameState()
    correct_item = create_item("correct_item")
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="Success.",
        failure_text="Failure.",
        completed_text="Already complete.",
        interaction_id="interaction.test",
    )
    npc = NPC(
        rect=pygame.Rect(100, 100, 120, 120),
        name="Test NPC",
        dialogue_lines=("Default dialogue.",),
        item_use=interaction,
        completed_dialogue_lines=("Completed dialogue.",),
    )
    game_state.inventory.add(correct_item)
    game_state.inventory.select(correct_item.item_id)
    scene = create_test_scene(game_state, npcs=[npc])

    scene.handle_event(create_primary_click(npc.rect.center))
    result = scene.handle_event(create_primary_click(npc.rect.center))

    assert result.consumed
    assert game_state.has_completed_interaction("interaction.test")
    assert scene.dialogue.current_line == "Completed dialogue."
    assert scene.active_speaker_name == npc.name


def test_item_on_target_without_item_use_rule_keeps_selection() -> None:
    game_state = GameState()
    selected_item = create_item("selected_item", "Selected Item")
    hotspot = Hotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        label="Test Hotspot",
        inspect_text="Inspection text.",
    )
    game_state.inventory.add(selected_item)
    game_state.inventory.select(selected_item.item_id)
    scene = create_test_scene(game_state, hotspots=[hotspot])

    result = scene.handle_event(create_primary_click(hotspot.rect.center))

    assert result.consumed
    assert game_state.inventory.contains(selected_item.item_id)
    assert game_state.inventory.selected_item is selected_item
    assert scene.interaction_text == "Selected Item does not seem useful here."


def test_locked_exit_does_not_transition_or_set_completion_flag() -> None:
    game_state = GameState()
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        target_scene_id="next_scene",
        label="Locked Exit",
        required_flag="exit_unlocked",
        locked_text="The exit is locked.",
        completion_flag="exit_completed",
    )
    scene = create_test_scene(game_state, exits=[exit_hotspot])

    result = scene.handle_event(create_primary_click(exit_hotspot.rect.center))

    assert result.consumed
    assert result.target_scene_id is None
    assert not game_state.has_flag("exit_completed")
    assert scene.interaction_text == "The exit is locked."


def test_unlocked_exit_transitions_and_sets_completion_flag() -> None:
    game_state = GameState()
    game_state.set_flag("exit_unlocked")
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        target_scene_id="next_scene",
        label="Unlocked Exit",
        required_flag="exit_unlocked",
        completion_flag="exit_completed",
    )
    scene = create_test_scene(game_state, exits=[exit_hotspot])

    result = scene.handle_event(create_primary_click(exit_hotspot.rect.center))

    assert result.consumed
    assert result.target_scene_id == "next_scene"
    assert game_state.has_flag("exit_completed")


def test_active_dialogue_consumes_advance_input() -> None:
    game_state = GameState()
    npc = NPC(
        rect=pygame.Rect(100, 100, 120, 120),
        name="Test NPC",
        dialogue_lines=(
            "First line.",
            "Second line.",
        ),
    )
    scene = create_test_scene(game_state, npcs=[npc])
    scene.handle_event(create_primary_click(npc.rect.center))
    advance_event = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_SPACE,
    )

    result = scene.handle_event(advance_event)

    assert result.consumed
    assert scene.dialogue.current_line == "Second line."


def test_dialogue_click_does_not_trigger_object_beneath_cursor() -> None:
    game_state = GameState()
    npc = NPC(
        rect=pygame.Rect(100, 100, 120, 120),
        name="Test NPC",
        dialogue_lines=(
            "First line.",
            "Second line.",
        ),
    )
    item = create_item("pickup", "Pickup Item")
    pickup = ItemHotspot(
        pickup_id="pickup.test",
        rect=pygame.Rect(300, 300, 120, 80),
        item=item,
        pickup_text="Item collected.",
    )
    scene = create_test_scene(
        game_state,
        item_hotspots=[pickup],
        npcs=[npc],
    )
    scene.handle_event(create_primary_click(npc.rect.center))

    result = scene.handle_event(create_primary_click(pickup.rect.center))

    assert result.consumed
    assert scene.dialogue.current_line == "Second line."
    assert not game_state.inventory.contains(item.item_id)
    assert pickup in scene.item_hotspots


def test_inventory_click_takes_precedence_over_world_target() -> None:
    game_state = GameState()
    item = create_item("inventory_item", "Inventory Item")
    game_state.inventory.add(item)
    scene = create_test_scene(game_state)
    inventory_row = scene.inventory_bar.item_rows(game_state.inventory.items)[0][1]
    overlapping_hotspot = Hotspot(
        rect=inventory_row.copy(),
        label="Overlapping Hotspot",
        inspect_text="World interaction triggered.",
    )
    scene.hotspots.append(overlapping_hotspot)

    result = scene.handle_event(create_primary_click(inventory_row.center))

    assert result.consumed
    assert game_state.inventory.selected_item is item
    assert scene.interaction_text == ("Selected Inventory Item. Click another item to combine them.")


def test_existing_recipe_result_keeps_ingredients_and_clears_selection() -> None:
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
    game_state.inventory.add(first_item)
    game_state.inventory.add(second_item)
    game_state.inventory.add(result_item)
    game_state.inventory.select(first_item.item_id)
    scene = create_test_scene(
        game_state,
        recipe_book=recipe_book,
    )

    result = scene.handle_event(create_primary_click(get_inventory_row_position(scene, 1)))

    assert result.consumed
    assert game_state.inventory.items == (
        first_item,
        second_item,
        result_item,
    )
    assert game_state.inventory.selected_item is None
    assert scene.interaction_text == "You already have Result Item."


def test_world_target_resolver_resolves_every_target_kind() -> None:
    game_state = GameState()
    npc = NPC(
        rect=pygame.Rect(100, 100, 80, 80),
        name="Target NPC",
        dialogue_lines=("Hello.",),
    )
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(200, 100, 80, 80),
        target_scene_id="next_scene",
        label="Target Exit",
    )
    item_hotspot = ItemHotspot(
        pickup_id="pickup.target",
        rect=pygame.Rect(300, 100, 80, 80),
        item=create_item("target_item", "Target Item"),
        pickup_text="Collected.",
    )
    hotspot = Hotspot(
        rect=pygame.Rect(400, 100, 80, 80),
        label="Target Hotspot",
        inspect_text="Inspect text.",
    )
    scene = create_test_scene(
        game_state,
        exits=[exit_hotspot],
        hotspots=[hotspot],
        item_hotspots=[item_hotspot],
        npcs=[npc],
    )

    assert scene._resolve_world_target(npc.rect.center).kind is WorldTargetKind.NPC
    assert scene._resolve_world_target(exit_hotspot.rect.center).kind is WorldTargetKind.EXIT
    assert scene._resolve_world_target(item_hotspot.rect.center).kind is WorldTargetKind.ITEM_PICKUP
    assert scene._resolve_world_target(hotspot.rect.center).kind is WorldTargetKind.HOTSPOT


def test_world_target_resolver_returns_none_for_empty_space() -> None:
    scene = create_test_scene(GameState())

    assert scene._resolve_world_target((10, 10)) is None


def test_world_target_resolver_uses_documented_priority_for_overlaps() -> None:
    game_state = GameState()
    rect = pygame.Rect(100, 100, 120, 120)
    npc = NPC(
        rect=rect.copy(),
        name="Priority NPC",
        dialogue_lines=("Hello.",),
    )
    exit_hotspot = ExitHotspot(
        rect=rect.copy(),
        target_scene_id="next_scene",
        label="Priority Exit",
    )
    item_hotspot = ItemHotspot(
        pickup_id="pickup.priority",
        rect=rect.copy(),
        item=create_item("priority_item", "Priority Item"),
        pickup_text="Collected.",
    )
    hotspot = Hotspot(
        rect=rect.copy(),
        label="Priority Hotspot",
        inspect_text="Inspect text.",
    )
    scene = create_test_scene(
        game_state,
        exits=[exit_hotspot],
        hotspots=[hotspot],
        item_hotspots=[item_hotspot],
        npcs=[npc],
    )

    target = scene._resolve_world_target(rect.center)
    assert target is not None
    assert target.kind is WorldTargetKind.NPC
    assert target.entity is npc

    scene.npcs.clear()
    target = scene._resolve_world_target(rect.center)
    assert target is not None
    assert target.kind is WorldTargetKind.EXIT
    assert target.entity is exit_hotspot

    scene.exits.clear()
    target = scene._resolve_world_target(rect.center)
    assert target is not None
    assert target.kind is WorldTargetKind.ITEM_PICKUP
    assert target.entity is item_hotspot

    scene.item_hotspots.clear()
    target = scene._resolve_world_target(rect.center)
    assert target is not None
    assert target.kind is WorldTargetKind.HOTSPOT
    assert target.entity is hotspot


def test_world_target_resolver_ignores_collected_pickups() -> None:
    game_state = GameState()
    item_hotspot = ItemHotspot(
        pickup_id="pickup.collected",
        rect=pygame.Rect(100, 100, 120, 120),
        item=create_item("collected_item", "Collected Item"),
        pickup_text="Collected.",
    )
    game_state.collect_pickup(item_hotspot.pickup_id)
    scene = create_test_scene(
        game_state,
        item_hotspots=[item_hotspot],
    )

    assert scene._resolve_world_target(item_hotspot.rect.center) is None


def test_click_and_hover_use_same_world_target_priority() -> None:
    game_state = GameState()
    rect = pygame.Rect(100, 100, 120, 120)
    exit_hotspot = ExitHotspot(
        rect=rect.copy(),
        target_scene_id="next_scene",
        label="Priority Exit",
    )
    hotspot = Hotspot(
        rect=rect.copy(),
        label="Lower Priority Hotspot",
        inspect_text="Inspect text.",
    )
    scene = create_test_scene(
        game_state,
        exits=[exit_hotspot],
        hotspots=[hotspot],
    )

    target = scene._resolve_world_target(rect.center)
    result = scene.handle_event(create_primary_click(rect.center))

    assert target is not None
    assert target.kind is WorldTargetKind.EXIT
    assert scene._hover_text_for_target(target) == "Go to: Priority Exit"
    assert result.consumed
    assert result.target_scene_id == "next_scene"
    assert scene.interaction_text is None


def test_exit_hover_text_uses_locked_label_when_exit_is_locked() -> None:
    game_state = GameState()
    exit_hotspot = ExitHotspot(
        rect=pygame.Rect(100, 100, 120, 120),
        target_scene_id="next_scene",
        label="Tower Gate",
        required_flag="tower_open",
        locked_label="Tower Gate (Locked)",
    )
    scene = create_test_scene(
        game_state,
        exits=[exit_hotspot],
    )

    target = scene._resolve_world_target(exit_hotspot.rect.center)

    assert target is not None
    assert target.kind is WorldTargetKind.EXIT
    assert scene._hover_text_for_target(target) == "Go to: Tower Gate (Locked)"
