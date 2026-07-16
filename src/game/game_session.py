from __future__ import annotations

from dataclasses import dataclass

from game.content.demo_world import create_demo_content
from game.game_content import GameContent
from game.game_state import GameState
from game.scene_manager import SceneManager
from game.ui.resources import UIResources


@dataclass(frozen=True)
class GameSession:
    """One fresh playable run of the game."""

    game_state: GameState
    scene_manager: SceneManager


def create_game_session(
    content: GameContent,
    ui_resources: UIResources,
) -> GameSession:
    """Create a fresh session using reusable static content."""
    game_state = GameState()
    scene_manager = SceneManager(
        scenes=content.build_scenes(game_state, ui_resources),
        starting_scene_id=content.starting_scene_id,
    )

    return GameSession(
        game_state=game_state,
        scene_manager=scene_manager,
    )


def create_demo_game_session(
    content: GameContent | None = None,
    ui_resources: UIResources | None = None,
) -> GameSession:
    """Create a fresh demo session with new runtime state and scenes."""
    active_resources = ui_resources or UIResources()

    return create_game_session(
        content or create_demo_content(active_resources),
        active_resources,
    )
