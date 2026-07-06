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
    )


def test_item_use_rejects_wrong_item() -> None:
    interaction = create_interaction()

    result = interaction.attempt("wrong_item")

    assert not result.success
    assert result.message == "That did not work."
    assert not result.consume_item
    assert not interaction.is_completed


def test_item_use_accepts_correct_item() -> None:
    interaction = create_interaction()

    result = interaction.attempt("correct_item")

    assert result.success
    assert result.message == "That worked."
    assert interaction.is_completed


def test_item_use_reports_item_consumption() -> None:
    interaction = create_interaction(consume_item=True)

    result = interaction.attempt("correct_item")

    assert result.success
    assert result.consume_item


def test_completed_interaction_cannot_run_again() -> None:
    interaction = create_interaction()
    interaction.attempt("correct_item")

    result = interaction.attempt("correct_item")

    assert not result.success
    assert result.message == "This is already complete."
