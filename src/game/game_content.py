from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from game.entities.item import Item
from game.game_state import GameState
from game.scenes.adventure_scene import AdventureScene
from game.scenes.base_scene import BaseScene
from game.systems.item_use import ItemUseInteraction
from game.systems.recipe import Recipe, RecipeBook
from game.ui.resources import UIResources

SceneBuilder = Callable[
    [GameState, RecipeBook, Mapping[str, Item], UIResources],
    BaseScene,
]


@dataclass(frozen=True)
class ContentIdRegistries:
    """Known stable IDs collected from reusable game content."""

    flag_ids: frozenset[str] = field(default_factory=frozenset)
    pickup_ids: frozenset[str] = field(default_factory=frozenset)
    interaction_ids: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class GameContent:
    """Reusable static content and rules shared by game sessions."""

    items_by_id: Mapping[str, Item]
    recipe_book: RecipeBook
    scenes_by_id: Mapping[str, SceneBuilder]
    starting_scene_id: str
    flag_ids: frozenset[str] = field(default_factory=frozenset)
    pickup_ids: frozenset[str] = field(default_factory=frozenset)
    interaction_ids: frozenset[str] = field(default_factory=frozenset)

    @property
    def items(self) -> tuple[Item, ...]:
        """Return item definitions in stable catalog order."""
        return tuple(self.items_by_id.values())

    @property
    def recipes(self) -> tuple[Recipe, ...]:
        """Return recipe definitions in stable catalog order."""
        return self.recipe_book.recipes

    def build_scenes(
        self,
        game_state: GameState,
        ui_resources: UIResources,
    ) -> dict[str, BaseScene]:
        """Build fresh session scenes from reusable content definitions."""
        return {
            scene_id: scene_builder(
                game_state,
                self.recipe_book,
                self.items_by_id,
                ui_resources,
            )
            for scene_id, scene_builder in self.scenes_by_id.items()
        }


def create_item_registry(items: tuple[Item, ...]) -> Mapping[str, Item]:
    """Create a read-only item registry keyed by stable item ID."""
    return MappingProxyType({item.item_id: item for item in items})


def create_scene_registry(
    scenes_by_id: Mapping[str, SceneBuilder],
) -> Mapping[str, SceneBuilder]:
    """Create a read-only scene-builder registry keyed by stable scene ID."""
    return MappingProxyType(dict(scenes_by_id))


def collect_content_id_registries(
    scenes_by_id: Mapping[str, BaseScene],
) -> ContentIdRegistries:
    """Collect stable IDs that runtime snapshots may reference."""
    flag_ids: set[str] = set()
    pickup_ids: set[str] = set()
    interaction_ids: set[str] = set()

    for scene in scenes_by_id.values():
        if not isinstance(scene, AdventureScene):
            continue

        for exit_hotspot in scene.exits:
            _add_optional(flag_ids, exit_hotspot.required_flag)
            _add_optional(flag_ids, exit_hotspot.completion_flag)
            _collect_item_use_ids(
                exit_hotspot.item_use,
                flag_ids=flag_ids,
                interaction_ids=interaction_ids,
            )

        for pickup in scene.item_hotspots:
            pickup_ids.add(pickup.pickup_id)

        for hotspot in scene.hotspots:
            _add_optional(flag_ids, hotspot.inspect_flag)
            _collect_item_use_ids(
                hotspot.item_use,
                flag_ids=flag_ids,
                interaction_ids=interaction_ids,
            )

        for npc in scene.npcs:
            _add_optional(flag_ids, npc.dialogue_flag)
            _collect_item_use_ids(
                npc.item_use,
                flag_ids=flag_ids,
                interaction_ids=interaction_ids,
            )

    return ContentIdRegistries(
        flag_ids=frozenset(flag_ids),
        pickup_ids=frozenset(pickup_ids),
        interaction_ids=frozenset(interaction_ids),
    )


def _collect_item_use_ids(
    item_use: ItemUseInteraction | None,
    *,
    flag_ids: set[str],
    interaction_ids: set[str],
) -> None:
    """Collect flag and interaction IDs from an item-use rule."""
    if item_use is None:
        return

    flag_ids.update(item_use.flags_to_set)
    _add_optional(flag_ids, item_use.completion_flag)
    _add_optional(interaction_ids, item_use.interaction_id)


def _add_optional(values: set[str], value: str | None) -> None:
    """Add an optional string to a set when present."""
    if value is not None:
        values.add(value)
