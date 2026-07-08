import pytest

from game.systems.item_use import ItemUseInteraction


def create_interaction(
    consume_item: bool = False,
) -> ItemUseInteraction:
    return ItemUseInteraction(
        required_item_id="correct_item",
        success_text="That worked.",
        failure_text="That did not work.",
        completed_text="This is already complete.",
        consume_item=consume_item,
        interaction_id="interaction.test",
    )


def test_item_use_rejects_wrong_item() -> None:
    interaction = create_interaction()

    result = interaction.attempt("wrong_item")

    assert not result.success
    assert result.message == "That did not work."
    assert not result.consume_item


def test_item_use_accepts_correct_item() -> None:
    interaction = create_interaction()

    result = interaction.attempt("correct_item")

    assert result.success
    assert result.message == "That worked."


def test_item_use_reports_item_consumption() -> None:
    interaction = create_interaction(consume_item=True)

    result = interaction.attempt("correct_item")

    assert result.success
    assert result.consume_item


def test_completed_interaction_cannot_run_again() -> None:
    interaction = create_interaction()

    result = interaction.attempt(
        "correct_item",
        is_completed=True,
    )

    assert not result.success
    assert result.message == "This is already complete."


def test_successful_item_use_returns_progression_flags() -> None:
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="That worked.",
        failure_text="That did not work.",
        completed_text="Already complete.",
        flags_to_set=(
            "first_flag",
            "second_flag",
        ),
        interaction_id="interaction.test",
    )

    result = interaction.attempt("correct_item")

    assert result.success
    assert result.flags_to_set == (
        "first_flag",
        "second_flag",
    )


def test_interaction_requires_one_completion_identifier() -> None:
    with pytest.raises(
        ValueError,
        match="requires exactly one completion identifier",
    ):
        ItemUseInteraction(
            required_item_id="correct_item",
            success_text="That worked.",
            failure_text="That did not work.",
            completed_text="Already complete.",
        )


def test_completion_flag_must_be_set_by_success() -> None:
    with pytest.raises(
        ValueError,
        match="completion_flag must also be present in flags_to_set",
    ):
        ItemUseInteraction(
            required_item_id="correct_item",
            success_text="That worked.",
            failure_text="That did not work.",
            completed_text="Already complete.",
            completion_flag="quest_finished",
        )
