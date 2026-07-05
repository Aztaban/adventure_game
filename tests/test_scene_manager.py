import pygame
import pytest

from game.scene_event_result import SceneEventResult
from game.scene_manager import SceneManager
from game.scenes.base_scene import BaseScene


class DummyScene(BaseScene):
    """Minimal scene used only by SceneManager tests."""

    def __init__(
        self,
        event_result: SceneEventResult | None = None,
    ) -> None:
        self.event_result = event_result or SceneEventResult()

    def handle_event(self, event: pygame.event.Event) -> SceneEventResult:
        del event
        return self.event_result

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


def test_scene_manager_reports_consumed_event() -> None:
    manager = SceneManager(
        scenes={
            "first": DummyScene(
                SceneEventResult(consumed=True),
            )
        },
        starting_scene_id="first",
    )

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

    assert manager.handle_event(event)


def test_scene_manager_changes_scene_from_event_result() -> None:
    manager = SceneManager(
        scenes={
            "first": DummyScene(
                SceneEventResult(
                    consumed=True,
                    target_scene_id="second",
                )
            ),
            "second": DummyScene(),
        },
        starting_scene_id="first",
    )

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(0, 0),
    )

    assert manager.handle_event(event)
    assert manager.current_scene_id == "second"
