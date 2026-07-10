from game.game_state import GameState


def test_game_state_starts_with_empty_inventory() -> None:
    game_state = GameState()

    assert len(game_state.inventory) == 0


def test_game_state_sets_and_clears_flags() -> None:
    game_state = GameState()

    game_state.set_flag("test_flag")

    assert game_state.has_flag("test_flag")

    game_state.clear_flag("test_flag")

    assert not game_state.has_flag("test_flag")


def test_game_state_starts_without_persistent_world_records() -> None:
    game_state = GameState()

    assert game_state.flags == ()
    assert game_state.collected_pickup_ids == ()
    assert game_state.completed_interaction_ids == ()
    assert not game_state.ending_reached
    assert not game_state.has_collected_pickup("pickup.test")
    assert not game_state.has_completed_interaction("interaction.test")


def test_collecting_pickup_is_idempotent() -> None:
    game_state = GameState()

    game_state.collect_pickup("pickup.test")
    game_state.collect_pickup("pickup.test")

    assert game_state.has_collected_pickup("pickup.test")


def test_completing_interaction_is_idempotent() -> None:
    game_state = GameState()

    game_state.complete_interaction("interaction.test")
    game_state.complete_interaction("interaction.test")

    assert game_state.has_completed_interaction("interaction.test")


def test_game_state_marks_ending_reached() -> None:
    game_state = GameState()

    game_state.mark_ending_reached()

    assert game_state.ending_reached
