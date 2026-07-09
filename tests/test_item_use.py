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


def test_item_use_definition_has_no_mutable_completion_state() -> None:
    interaction = create_interaction()

    assert not hasattr(interaction, "is_completed")


def test_interaction_id_completion_is_read_from_world_state() -> None:
    interaction = create_interaction()

    assert not interaction.has_been_completed(
        lambda _: False,
        lambda _: False,
    )
    assert interaction.has_been_completed(
        lambda _: False,
        lambda interaction_id: interaction_id == "interaction.test",
    )


def test_completion_flag_completion_is_read_from_world_state() -> None:
    interaction = ItemUseInteraction(
        required_item_id="correct_item",
        success_text="That worked.",
        failure_text="That did not work.",
        completed_text="Already complete.",
        flags_to_set=("quest_finished",),
        completion_flag="quest_finished",
    )

    assert not interaction.has_been_completed(
        lambda _: False,
        lambda _: False,
    )
    assert interaction.has_been_completed(
        lambda flag: flag == "quest_finished",
        lambda _: False,
    )


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
