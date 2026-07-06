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
