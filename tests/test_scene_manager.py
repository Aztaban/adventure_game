import pygame
import pytest

from game.scene_manager import SceneManager
from game.scenes.base_scene import BaseScene


class DummyScene(BaseScene):
    """Minimal scene used only by SceneManager tests."""

    def handle_event(self, event: pygame.event.Event) -> str | None:
        del event
        return None

    def update(self, delta_time: float) -> None:
        del delta_time

    def draw(self, surface: pygame.Surface) -> None:
        del surface


def test_scene_manager_uses_starting_scene() -> None:
    scenes = {
        "first": DummyScene(),
        "second": DummyScene(),
    }

    manager = SceneManager(
        scenes=scenes,
        starting_scene_id="first",
    )

    assert manager.current_scene_id == "first"
    assert manager.current_scene is scenes["first"]


def test_scene_manager_changes_scene() -> None:
    scenes = {
        "first": DummyScene(),
        "second": DummyScene(),
    }

    manager = SceneManager(
        scenes=scenes,
        starting_scene_id="first",
    )

    manager.change_scene("second")

    assert manager.current_scene_id == "second"
    assert manager.current_scene is scenes["second"]


def test_scene_manager_rejects_unknown_scene() -> None:
    manager = SceneManager(
        scenes={"first": DummyScene()},
        starting_scene_id="first",
    )

    with pytest.raises(ValueError, match="Scene does not exist"):
        manager.change_scene("missing")
