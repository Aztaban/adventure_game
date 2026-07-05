import pytest

from game.systems.dialogue import Dialogue


def test_dialogue_starts_on_first_line() -> None:
    dialogue = Dialogue()

    dialogue.start(("First line.", "Second line."))

    assert dialogue.is_active
    assert dialogue.current_line == "First line."


def test_dialogue_advances_to_next_line() -> None:
    dialogue = Dialogue()
    dialogue.start(("First line.", "Second line."))

    dialogue.advance()

    assert dialogue.is_active
    assert dialogue.current_line == "Second line."


def test_dialogue_closes_after_final_line() -> None:
    dialogue = Dialogue()
    dialogue.start(("Only line.",))

    dialogue.advance()

    assert not dialogue.is_active
    assert dialogue.current_line is None


def test_dialogue_can_be_closed_manually() -> None:
    dialogue = Dialogue()
    dialogue.start(("First line.", "Second line."))

    dialogue.close()

    assert not dialogue.is_active
    assert dialogue.current_line is None


def test_dialogue_rejects_empty_lines() -> None:
    dialogue = Dialogue()

    with pytest.raises(ValueError, match="at least one line"):
        dialogue.start(())
