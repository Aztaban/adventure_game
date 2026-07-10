from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType

from game.entities.item import Item
from game.game_state import GameState
from game.scenes.base_scene import BaseScene
from game.systems.recipe import Recipe, RecipeBook

SceneBuilder = Callable[[GameState, RecipeBook], BaseScene]


@dataclass(frozen=True)
class GameContent:
    """Reusable static content and rules shared by game sessions."""

    items_by_id: Mapping[str, Item]
    recipe_book: RecipeBook
    scenes_by_id: Mapping[str, SceneBuilder]
    starting_scene_id: str

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
    ) -> dict[str, BaseScene]:
        """Build fresh session scenes from reusable content definitions."""
        return {
            scene_id: scene_builder(game_state, self.recipe_book)
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
