import pygame

from game.entities.npc import NPC
from game.systems.item_use import ItemUseInteraction


def create_item_use(
    interaction_id: str = "interaction.test",
) -> ItemUseInteraction:
    """Create a stateless test interaction definition."""
    return ItemUseInteraction(
        required_item_id="correct_item",
        success_text="That worked.",
        failure_text="That did not work.",
        completed_text="This is already complete.",
        interaction_id=interaction_id,
    )


def create_npc(
    *,
    item_use: ItemUseInteraction | None = None,
    completed_dialogue_lines: tuple[str, ...] = (),
    dialogue_flag: str | None = None,
    flagged_dialogue_lines: tuple[str, ...] = (),
) -> NPC:
    """Create a test NPC with optional conditional dialogue."""
    return NPC(
        rect=pygame.Rect(100, 100, 200, 100),
        name="Test NPC",
        dialogue_lines=("Default dialogue.",),
        item_use=item_use,
        completed_dialogue_lines=completed_dialogue_lines,
        dialogue_flag=dialogue_flag,
        flagged_dialogue_lines=flagged_dialogue_lines,
    )


def dialogue_for(
    npc: NPC,
    *,
    active_flag: str | None = None,
    completed_interaction_id: str | None = None,
) -> tuple[str, ...]:
    """Return NPC dialogue using test world-state callbacks."""
    return npc.dialogue_for(
        lambda flag: flag == active_flag,
        lambda interaction_id: interaction_id == completed_interaction_id,
    )


def test_npc_contains_point_inside_rectangle() -> None:
    npc = create_npc()

    assert npc.contains_point((150, 150))


def test_npc_rejects_point_outside_rectangle() -> None:
    npc = create_npc()

    assert not npc.contains_point((50, 50))


def test_default_npc_returns_default_dialogue() -> None:
    npc = create_npc()

    assert dialogue_for(npc) == ("Default dialogue.",)


def test_completed_interaction_returns_completed_dialogue() -> None:
    npc = create_npc(
        item_use=create_item_use(),
        completed_dialogue_lines=("Completed dialogue.",),
    )

    assert dialogue_for(npc, completed_interaction_id="interaction.test") == (
        "Completed dialogue.",
    )


def test_active_matching_flag_returns_flagged_dialogue() -> None:
    npc = create_npc(
        dialogue_flag="world_changed",
        flagged_dialogue_lines=("Flagged dialogue.",),
    )

    assert dialogue_for(npc, active_flag="world_changed") == (
        "Flagged dialogue.",
    )


def test_inactive_flag_falls_back_to_completed_dialogue() -> None:
    npc = create_npc(
        item_use=create_item_use(),
        completed_dialogue_lines=("Completed dialogue.",),
        dialogue_flag="world_changed",
        flagged_dialogue_lines=("Flagged dialogue.",),
    )

    assert dialogue_for(npc, completed_interaction_id="interaction.test") == (
        "Completed dialogue.",
    )


def test_dialogue_priority_is_flag_then_completed_then_default() -> None:
    npc = create_npc(
        item_use=create_item_use(),
        completed_dialogue_lines=("Completed dialogue.",),
        dialogue_flag="world_changed",
        flagged_dialogue_lines=("Flagged dialogue.",),
    )

    assert dialogue_for(npc) == ("Default dialogue.",)
    assert dialogue_for(npc, completed_interaction_id="interaction.test") == (
        "Completed dialogue.",
    )
    assert dialogue_for(
        npc,
        active_flag="world_changed",
        completed_interaction_id="interaction.test",
    ) == ("Flagged dialogue.",)
