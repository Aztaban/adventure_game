from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, TypedDict

from game.game_content import GameContent
from game.game_session import GameSession
from game.game_state import GameState
from game.scene_manager import SceneManager
from game.ui.resources import UIResources

SAVE_DATA_VERSION = 1


class GameSnapshot(TypedDict):
    """Serialization-ready runtime state snapshot."""

    save_version: int
    current_scene_id: str
    inventory_item_ids: list[str]
    selected_item_id: str | None
    flags: list[str]
    collected_pickup_ids: list[str]
    completed_interaction_ids: list[str]
    ending_reached: bool


class SnapshotValidationError(ValueError):
    """Raised when a runtime-state snapshot references invalid content IDs."""


def create_state_snapshot(
    session: GameSession,
) -> GameSnapshot:
    """Export session runtime state as plain Python data."""
    game_state = session.game_state

    return {
        "save_version": SAVE_DATA_VERSION,
        "current_scene_id": session.scene_manager.current_scene_id,
        "inventory_item_ids": list(game_state.inventory.item_ids),
        "selected_item_id": game_state.inventory.selected_item_id,
        "flags": list(game_state.flags),
        "collected_pickup_ids": list(game_state.collected_pickup_ids),
        "completed_interaction_ids": list(game_state.completed_interaction_ids),
        "ending_reached": game_state.ending_reached,
    }


def restore_session_from_snapshot(
    *,
    content: GameContent,
    snapshot: Mapping[str, Any],
    ui_resources: UIResources,
) -> GameSession:
    """Create a fresh session from a validated runtime-state snapshot."""
    validated_snapshot = _validate_snapshot(
        content=content,
        snapshot=snapshot,
    )
    game_state = _restore_game_state(
        content=content,
        snapshot=validated_snapshot,
    )
    scene_manager = SceneManager(
        scenes=content.build_scenes(game_state, ui_resources),
        starting_scene_id=content.starting_scene_id,
    )
    scene_manager.change_scene(validated_snapshot["current_scene_id"])

    return GameSession(
        game_state=game_state,
        scene_manager=scene_manager,
    )


def _restore_game_state(
    *,
    content: GameContent,
    snapshot: GameSnapshot,
) -> GameState:
    """Restore persistent runtime state into a fresh GameState."""
    game_state = GameState()

    for item_id in snapshot["inventory_item_ids"]:
        game_state.inventory.add(content.items_by_id[item_id])

    selected_item_id = snapshot["selected_item_id"]

    if selected_item_id is not None:
        game_state.inventory.select(selected_item_id)

    for flag in snapshot["flags"]:
        game_state.set_flag(flag)

    for pickup_id in snapshot["collected_pickup_ids"]:
        game_state.collect_pickup(pickup_id)

    for interaction_id in snapshot["completed_interaction_ids"]:
        game_state.complete_interaction(interaction_id)

    if snapshot["ending_reached"]:
        game_state.mark_ending_reached()

    return game_state


def _validate_snapshot(
    *,
    content: GameContent,
    snapshot: Mapping[str, Any],
) -> GameSnapshot:
    """Validate snapshot shape and all content references."""
    errors: list[str] = []
    save_version = snapshot.get("save_version")

    if save_version != SAVE_DATA_VERSION:
        errors.append(f"Unsupported save version '{save_version}'. Expected '{SAVE_DATA_VERSION}'.")

    current_scene_id = _require_string(snapshot, "current_scene_id", errors)
    inventory_item_ids = _require_string_list(
        snapshot,
        "inventory_item_ids",
        errors,
    )
    selected_item_id = _require_optional_string(
        snapshot,
        "selected_item_id",
        errors,
    )
    flags = _require_string_list(snapshot, "flags", errors)
    collected_pickup_ids = _require_string_list(
        snapshot,
        "collected_pickup_ids",
        errors,
    )
    completed_interaction_ids = _require_string_list(
        snapshot,
        "completed_interaction_ids",
        errors,
    )
    ending_reached = _require_bool(snapshot, "ending_reached", errors)

    _validate_known_id(
        value=current_scene_id,
        known_values=set(content.scenes_by_id),
        id_type="scene",
        errors=errors,
    )
    _validate_known_ids(
        values=inventory_item_ids,
        known_values=set(content.items_by_id),
        id_type="inventory item",
        errors=errors,
    )
    _validate_known_ids(
        values=flags,
        known_values=content.flag_ids,
        id_type="flag",
        errors=errors,
    )
    _validate_known_ids(
        values=collected_pickup_ids,
        known_values=content.pickup_ids,
        id_type="collected pickup",
        errors=errors,
    )
    _validate_known_ids(
        values=completed_interaction_ids,
        known_values=content.interaction_ids,
        id_type="completed interaction",
        errors=errors,
    )

    if selected_item_id is not None:
        _validate_known_id(
            value=selected_item_id,
            known_values=set(content.items_by_id),
            id_type="selected item",
            errors=errors,
        )

        if selected_item_id not in inventory_item_ids:
            errors.append(f"Selected item ID '{selected_item_id}' is not present in inventory_item_ids.")

    _validate_no_duplicates(
        values=inventory_item_ids,
        id_type="inventory item",
        errors=errors,
    )
    _validate_no_duplicates(
        values=flags,
        id_type="flag",
        errors=errors,
    )
    _validate_no_duplicates(
        values=collected_pickup_ids,
        id_type="collected pickup",
        errors=errors,
    )
    _validate_no_duplicates(
        values=completed_interaction_ids,
        id_type="completed interaction",
        errors=errors,
    )

    if errors:
        formatted_errors = "\n- ".join(errors)
        raise SnapshotValidationError(f"State snapshot validation failed:\n- {formatted_errors}")

    return GameSnapshot(
        save_version=SAVE_DATA_VERSION,
        current_scene_id=current_scene_id,
        inventory_item_ids=list(inventory_item_ids),
        selected_item_id=selected_item_id,
        flags=list(flags),
        collected_pickup_ids=list(collected_pickup_ids),
        completed_interaction_ids=list(completed_interaction_ids),
        ending_reached=ending_reached,
    )


def _require_string(
    snapshot: Mapping[str, Any],
    key: str,
    errors: list[str],
) -> str:
    """Return a required string value or record a validation error."""
    value = snapshot.get(key)

    if isinstance(value, str):
        return value

    errors.append(f"Snapshot field '{key}' must be a string.")
    return ""


def _require_optional_string(
    snapshot: Mapping[str, Any],
    key: str,
    errors: list[str],
) -> str | None:
    """Return a required string-or-null value or record a validation error."""
    value = snapshot.get(key)

    if value is None or isinstance(value, str):
        return value

    errors.append(f"Snapshot field '{key}' must be a string or null.")
    return None


def _require_string_list(
    snapshot: Mapping[str, Any],
    key: str,
    errors: list[str],
) -> tuple[str, ...]:
    """Return a required string sequence or record a validation error."""
    value = snapshot.get(key)

    if not _is_sequence(value):
        errors.append(f"Snapshot field '{key}' must be a list of strings.")
        return ()

    invalid_values = [entry for entry in value if not isinstance(entry, str)]

    if invalid_values:
        errors.append(f"Snapshot field '{key}' must contain only strings.")
        return ()

    return tuple(value)


def _require_bool(
    snapshot: Mapping[str, Any],
    key: str,
    errors: list[str],
) -> bool:
    """Return a required bool value or record a validation error."""
    value = snapshot.get(key)

    if isinstance(value, bool):
        return value

    errors.append(f"Snapshot field '{key}' must be a bool.")
    return False


def _is_sequence(value: Any) -> bool:
    """Return whether a value is a non-string sequence."""
    return isinstance(value, Sequence) and not isinstance(value, str | bytes)


def _validate_known_ids(
    *,
    values: tuple[str, ...],
    known_values: frozenset[str] | set[str],
    id_type: str,
    errors: list[str],
) -> None:
    """Validate a group of content IDs."""
    for value in values:
        _validate_known_id(
            value=value,
            known_values=known_values,
            id_type=id_type,
            errors=errors,
        )


def _validate_known_id(
    *,
    value: str,
    known_values: frozenset[str] | set[str],
    id_type: str,
    errors: list[str],
) -> None:
    """Validate one content ID."""
    if value and value not in known_values:
        errors.append(f"Unknown {id_type} ID '{value}'.")


def _validate_no_duplicates(
    *,
    values: tuple[str, ...],
    id_type: str,
    errors: list[str],
) -> None:
    """Validate that snapshot ID lists do not contain duplicate values."""
    seen: set[str] = set()

    for value in values:
        if value in seen:
            errors.append(f"Duplicate {id_type} ID '{value}'.")
            continue

        seen.add(value)
