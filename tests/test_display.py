import pygame
import pytest

from game.display import (
    LETTERBOX_COLOR,
    calculate_destination_rect,
    present_logical_surface,
)
from game.settings import LOGICAL_SIZE


class RecordingOutputSurface:
    """Small output-surface double for presentation tests."""

    def __init__(self, size: tuple[int, int]) -> None:
        self._size = size
        self.fill_calls: list[tuple[int, int, int]] = []
        self.blit_calls: list[tuple[object, pygame.Rect]] = []

    def get_size(self) -> tuple[int, int]:
        return self._size

    def fill(self, color: tuple[int, int, int]) -> None:
        self.fill_calls.append(color)

    def blit(self, surface: object, destination: pygame.Rect) -> None:
        self.blit_calls.append((surface, destination))


@pytest.mark.parametrize(
    ("output_size", "expected_rect"),
    [
        ((1280, 720), pygame.Rect(0, 0, 1280, 720)),
        ((1600, 900), pygame.Rect(0, 0, 1600, 900)),
        ((1920, 1080), pygame.Rect(0, 0, 1920, 1080)),
        ((1024, 768), pygame.Rect(0, 96, 1024, 576)),
        ((3440, 1440), pygame.Rect(440, 0, 2560, 1440)),
        ((1000, 1000), pygame.Rect(0, 219, 1000, 562)),
    ],
)
def test_destination_rect_preserves_aspect_ratio_and_centers_output(
    output_size: tuple[int, int],
    expected_rect: pygame.Rect,
) -> None:
    assert calculate_destination_rect(LOGICAL_SIZE, output_size) == expected_rect


@pytest.mark.parametrize(
    ("logical_size", "output_size", "message"),
    [
        ((0, 720), (1280, 720), "Logical"),
        ((1280, -1), (1280, 720), "Logical"),
        ((1280, 720), (0, 720), "Physical"),
        ((1280, 720), (1280, -1), "Physical"),
    ],
)
def test_destination_rect_rejects_non_positive_dimensions(
    logical_size: tuple[int, int],
    output_size: tuple[int, int],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        calculate_destination_rect(logical_size, output_size)


def test_native_presentation_clears_output_and_blits_logical_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    logical_surface = pygame.Surface(LOGICAL_SIZE)
    output_surface = RecordingOutputSurface(LOGICAL_SIZE)

    def fail_if_scaled(*args: object) -> None:
        del args
        raise AssertionError("Native presentation should not scale the logical frame.")

    monkeypatch.setattr(pygame.transform, "smoothscale", fail_if_scaled)

    destination_rect = present_logical_surface(logical_surface, output_surface)

    assert destination_rect == pygame.Rect(0, 0, *LOGICAL_SIZE)
    assert output_surface.fill_calls == [LETTERBOX_COLOR]
    assert output_surface.blit_calls == [(logical_surface, destination_rect)]


def test_scaled_presentation_clears_letterbox_space_and_uses_one_scaled_frame(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    logical_surface = pygame.Surface(LOGICAL_SIZE)
    output_surface = RecordingOutputSurface((1000, 1000))
    scaled_surface = object()
    scale_calls: list[tuple[object, tuple[int, int]]] = []

    def record_scale(
        source: pygame.Surface,
        size: tuple[int, int],
    ) -> object:
        scale_calls.append((source, size))
        return scaled_surface

    monkeypatch.setattr(pygame.transform, "smoothscale", record_scale)

    destination_rect = present_logical_surface(logical_surface, output_surface)

    assert destination_rect == pygame.Rect(0, 219, 1000, 562)
    assert output_surface.fill_calls == [LETTERBOX_COLOR]
    assert scale_calls == [(logical_surface, destination_rect.size)]
    assert output_surface.blit_calls == [(scaled_surface, destination_rect)]
