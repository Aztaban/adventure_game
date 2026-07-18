from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from game.entities.item import Item
from game.scenes.adventure_scene import AdventureScene
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import Recipe

SceneEntry = tuple[str, AdventureScene]


class ContentValidationError(ValueError):
    """Raised when Python-created game content contains invalid references."""


@dataclass(frozen=True)
class StableContentId:
    """Stable content ID paired with the object that owns it."""

    value: str
    owner: str


def validate_content(
    *,
    scene_entries: Iterable[SceneEntry],
    starting_scene_id: str,
    items: Iterable[Item],
    recipes: Iterable[Recipe],
    stable_ids: Iterable[StableContentId] = (),
) -> None:
    """Validate IDs and references in Python-created game content."""
    scenes = tuple(scene_entries)
    item_catalog = tuple(items)
    recipe_catalog = tuple(recipes)
    errors: list[str] = []

    scene_ids = _validate_unique_scene_ids(scenes, errors)
    item_ids = _validate_unique_item_ids(item_catalog, errors)

    if starting_scene_id not in scene_ids:
        errors.append(f"Starting scene ID '{starting_scene_id}' does not exist.")

    _validate_scene_references(
        scenes=scenes,
        scene_ids=scene_ids,
        item_ids=item_ids,
        errors=errors,
    )
    _validate_recipes(recipe_catalog, item_ids, errors)

    all_stable_ids = (
        *_collect_scene_stable_ids(scenes),
        *stable_ids,
    )
    _validate_stable_ids(all_stable_ids, errors)

    if errors:
        formatted_errors = "\n- ".join(errors)
        raise ContentValidationError(f"Content validation failed:\n- {formatted_errors}")


def _validate_unique_scene_ids(
    scenes: tuple[SceneEntry, ...],
    errors: list[str],
) -> set[str]:
    owners_by_id: dict[str, str] = {}

    for scene_id, scene in scenes:
        previous_owner = owners_by_id.get(scene_id)

        if previous_owner is not None:
            errors.append(f"Duplicate scene ID '{scene_id}' used by '{previous_owner}' and '{scene.name}'.")
            continue

        owners_by_id[scene_id] = scene.name

    return set(owners_by_id)


def _validate_unique_item_ids(
    items: tuple[Item, ...],
    errors: list[str],
) -> set[str]:
    owners_by_id: dict[str, str] = {}

    for item in items:
        previous_owner = owners_by_id.get(item.item_id)

        if previous_owner is not None:
            errors.append(f"Duplicate item ID '{item.item_id}' used by '{previous_owner}' and '{item.name}'.")
            continue

        owners_by_id[item.item_id] = item.name

    return set(owners_by_id)


def _validate_scene_references(
    *,
    scenes: tuple[SceneEntry, ...],
    scene_ids: set[str],
    item_ids: set[str],
    errors: list[str],
) -> None:
    for scene_id, scene in scenes:
        for exit_hotspot in scene.exits:
            if exit_hotspot.target_scene_id not in scene_ids:
                errors.append(
                    f"Scene '{scene_id}' exit "
                    f"'{exit_hotspot.label}' targets unknown scene ID "
                    f"'{exit_hotspot.target_scene_id}'."
                )

            _validate_item_use_requirement(
                scene_id=scene_id,
                owner_type="exit",
                owner_name=exit_hotspot.label,
                item_use=exit_hotspot.item_use,
                item_ids=item_ids,
                errors=errors,
            )

        for pickup in scene.item_hotspots:
            if pickup.item.item_id not in item_ids:
                errors.append(
                    f"Scene '{scene_id}' pickup "
                    f"'{pickup.item.name}' references unknown item ID "
                    f"'{pickup.item.item_id}'."
                )

        for hotspot in scene.hotspots:
            _validate_item_use_requirement(
                scene_id=scene_id,
                owner_type="hotspot",
                owner_name=hotspot.label,
                item_use=hotspot.item_use,
                item_ids=item_ids,
                errors=errors,
            )

        for npc in scene.npcs:
            _validate_item_use_requirement(
                scene_id=scene_id,
                owner_type="NPC",
                owner_name=npc.name,
                item_use=npc.item_use,
                item_ids=item_ids,
                errors=errors,
            )


def _validate_item_use_requirement(
    *,
    scene_id: str,
    owner_type: str,
    owner_name: str,
    item_use: ItemUseInteraction | None,
    item_ids: set[str],
    errors: list[str],
) -> None:
    if item_use is None:
        return

    if item_use.required_item_id not in item_ids:
        errors.append(
            f"Scene '{scene_id}' {owner_type} '{owner_name}' requires unknown item ID '{item_use.required_item_id}'."
        )

    if item_use.result_item is None or item_use.result_item.item_id in item_ids:
        return

    errors.append(
        f"Scene '{scene_id}' {owner_type} '{owner_name}' creates unknown item ID '{item_use.result_item.item_id}'."
    )


def _validate_recipes(
    recipes: tuple[Recipe, ...],
    item_ids: set[str],
    errors: list[str],
) -> None:
    for recipe in recipes:
        description = f"{recipe.first_item_id} + {recipe.second_item_id} -> {recipe.result_item.item_id}"

        for ingredient_id in (
            recipe.first_item_id,
            recipe.second_item_id,
        ):
            if ingredient_id not in item_ids:
                errors.append(f"Recipe '{description}' references unknown ingredient item ID '{ingredient_id}'.")

        if recipe.result_item.item_id not in item_ids:
            errors.append(f"Recipe '{description}' references unknown result item ID '{recipe.result_item.item_id}'.")


def _collect_scene_stable_ids(
    scenes: tuple[SceneEntry, ...],
) -> tuple[StableContentId, ...]:
    stable_ids: list[StableContentId] = []

    for scene_id, scene in scenes:
        for pickup in scene.item_hotspots:
            stable_ids.append(
                StableContentId(
                    value=pickup.pickup_id,
                    owner=(f"Scene '{scene_id}' pickup '{pickup.item.name}'"),
                )
            )

        for exit_hotspot in scene.exits:
            _append_interaction_id(
                stable_ids=stable_ids,
                item_use=exit_hotspot.item_use,
                owner=(f"Scene '{scene_id}' exit '{exit_hotspot.label}' interaction"),
            )

        for hotspot in scene.hotspots:
            _append_interaction_id(
                stable_ids=stable_ids,
                item_use=hotspot.item_use,
                owner=(f"Scene '{scene_id}' hotspot '{hotspot.label}' interaction"),
            )

        for npc in scene.npcs:
            _append_interaction_id(
                stable_ids=stable_ids,
                item_use=npc.item_use,
                owner=(f"Scene '{scene_id}' NPC '{npc.name}' interaction"),
            )

    return tuple(stable_ids)


def _append_interaction_id(
    *,
    stable_ids: list[StableContentId],
    item_use: ItemUseInteraction | None,
    owner: str,
) -> None:
    if item_use is None or item_use.interaction_id is None:
        return

    stable_ids.append(
        StableContentId(
            value=item_use.interaction_id,
            owner=owner,
        )
    )


def _validate_stable_ids(
    stable_ids: tuple[StableContentId, ...],
    errors: list[str],
) -> None:
    owners_by_id: dict[str, str] = {}

    for stable_id in stable_ids:
        previous_owner = owners_by_id.get(stable_id.value)

        if previous_owner is not None:
            errors.append(
                f"Duplicate stable ID '{stable_id.value}' used by '{previous_owner}' and '{stable_id.owner}'."
            )
            continue

        owners_by_id[stable_id.value] = stable_id.owner
