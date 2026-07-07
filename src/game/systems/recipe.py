from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from game.entities.item import Item

RecipeKey = tuple[str, str]


def create_recipe_key(first_item_id: str, second_item_id: str) -> RecipeKey:
    """Create an order-independent key fro the item IDs."""
    return tuple(sorted((first_item_id, second_item_id)))


@dataclass(frozen=True)
class Recipe:
    """Describe two ingredients and the resulting item."""

    first_item_id: str
    second_item_id: str
    result_item: Item
    success_text: str

    def __post_init__(self) -> None:
        if self.first_item_id == self.second_item_id:
            raise ValueError("A recipe currently requires two different items.")

        if self.result_item.item_id in {self.first_item_id, self.second_item_id}:
            raise ValueError("Recipe result must differ from its ingredients.")

    @property
    def key(self) -> RecipeKey:
        """Return the order-independent recipe key."""
        return create_recipe_key(self.first_item_id, self.second_item_id)


class RecipeBook:
    """Store and find available item-combination recipes."""

    def __init__(self, recipes: Iterable[Recipe] = ()) -> None:
        self._recipes: dict[RecipeKey, Recipe] = {}

        for recipe in recipes:
            self.add(recipe)

    def add(self, recipe: Recipe) -> None:
        """Add a recipe and reject duplicate ingredient pairs."""
        if recipe.key in self._recipes:
            raise ValueError("A recipe for these ingredients already exists.")

        self._recipes[recipe.key] = recipe

    def find(self, first_item_id: str, second_item_id: str) -> Recipe | None:
        """Find a recipe regardless of ingredient order."""
        key = create_recipe_key(first_item_id, second_item_id)

        return self._recipes.get(key)
