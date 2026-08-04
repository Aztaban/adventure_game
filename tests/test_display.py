import pygame
import pytest

import game.display as display_module
from game.display import (
    LETTERBOX_COLOR,
    DisplayModeChangeError,
    DisplayViewport,
    calculate_destination_rect,
    convert_pointer_event,
    create_display_surface,
    physical_to_logical_position,
    present_logical_surface,
    primary_desktop_size,
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

    destination_rect = pygame.Rect(0, 0, *LOGICAL_SIZE)

    present_logical_surface(logical_surface, output_surface, destination_rect)

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

    destination_rect = pygame.Rect(0, 219, 1000, 562)

    present_logical_surface(logical_surface, output_surface, destination_rect)

    assert output_surface.fill_calls == [LETTERBOX_COLOR]
    assert scale_calls == [(logical_surface, destination_rect.size)]
    assert output_surface.blit_calls == [(scaled_surface, destination_rect)]


@pytest.mark.parametrize(
    ("output_size", "physical_position", "expected_position"),
    [
        ((1280, 720), (640, 360), (640, 360)),
        ((1600, 900), (800, 450), (640, 360)),
        ((1600, 900), (0, 0), (0, 0)),
        ((1600, 900), (1599, 899), (1279, 719)),
        ((3440, 1440), (440, 0), (0, 0)),
        ((3440, 1440), (2999, 1439), (1279, 719)),
        ((1024, 768), (512, 384), (640, 360)),
    ],
)
def test_physical_positions_map_into_logical_frame(
    output_size: tuple[int, int],
    physical_position: tuple[int, int],
    expected_position: tuple[int, int],
) -> None:
    destination_rect = calculate_destination_rect(LOGICAL_SIZE, output_size)

    assert (
        physical_to_logical_position(
            physical_position,
            LOGICAL_SIZE,
            destination_rect,
        )
        == expected_position
    )


@pytest.mark.parametrize(
    "physical_position",
    [
        (512, 95),
        (512, 672),
        (-1, 384),
        (1024, 384),
    ],
)
def test_physical_positions_outside_letterboxed_frame_are_rejected(
    physical_position: tuple[int, int],
) -> None:
    destination_rect = calculate_destination_rect(LOGICAL_SIZE, (1024, 768))

    assert (
        physical_to_logical_position(
            physical_position,
            LOGICAL_SIZE,
            destination_rect,
        )
        is None
    )


@pytest.mark.parametrize(
    "event_type",
    [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP],
)
def test_pointer_events_share_the_same_coordinate_conversion(event_type: int) -> None:
    attributes: dict[str, object] = {"pos": (800, 450)}

    if event_type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        attributes["button"] = 1

    event = pygame.event.Event(event_type, attributes)
    converted_event = convert_pointer_event(
        event,
        LOGICAL_SIZE,
        calculate_destination_rect(LOGICAL_SIZE, (1600, 900)),
    )

    assert converted_event.pos == (640, 360)
    assert event.pos == (800, 450)


@pytest.mark.parametrize(
    "event_type",
    [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN],
)
def test_pointer_events_in_letterbox_space_receive_no_logical_position(
    event_type: int,
) -> None:
    attributes: dict[str, object] = {"pos": (500, 100)}

    if event_type == pygame.MOUSEBUTTONDOWN:
        attributes["button"] = 1

    event = pygame.event.Event(event_type, attributes)
    converted_event = convert_pointer_event(
        event,
        LOGICAL_SIZE,
        calculate_destination_rect(LOGICAL_SIZE, (1000, 1000)),
    )

    assert converted_event.pos is None


def test_primary_desktop_size_uses_first_configured_desktop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        pygame.display,
        "get_desktop_sizes",
        lambda: [(2560, 1440), (1920, 1080)],
    )

    assert primary_desktop_size() == (2560, 1440)


def test_primary_desktop_size_rejects_missing_desktop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(pygame.display, "get_desktop_sizes", lambda: [])

    with pytest.raises(DisplayModeChangeError, match="available desktop"):
        primary_desktop_size()


@pytest.mark.parametrize(
    ("fullscreen", "expected_flags"),
    [(True, pygame.FULLSCREEN), (False, 0)],
)
def test_display_surface_creation_uses_expected_pygame_flags(
    fullscreen: bool,
    expected_flags: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_surface = pygame.Surface((1600, 900))
    calls: list[tuple[tuple[int, int], int]] = []

    def record_set_mode(
        size: tuple[int, int],
        flags: int,
    ) -> pygame.Surface:
        calls.append((size, flags))
        return expected_surface

    monkeypatch.setattr(pygame.display, "set_mode", record_set_mode)

    result = create_display_surface((1600, 900), fullscreen=fullscreen)

    assert result is expected_surface
    assert calls == [((1600, 900), expected_flags)]


def test_display_surface_creation_wraps_pygame_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_set_mode(size: tuple[int, int], flags: int) -> pygame.Surface:
        del size, flags
        raise pygame.error("video mode unavailable")

    monkeypatch.setattr(pygame.display, "set_mode", fail_set_mode)

    with pytest.raises(DisplayModeChangeError, match="1600 x 900 windowed"):
        create_display_surface((1600, 900), fullscreen=False)


def test_viewport_uses_one_destination_rect_for_presentation_and_pointer_conversion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_surface = RecordingOutputSurface((1000, 1000))
    viewport = DisplayViewport(LOGICAL_SIZE, output_surface)
    expected_rect = pygame.Rect(0, 219, 1000, 562)

    def fail_recalculation(*args: object) -> pygame.Rect:
        del args
        raise AssertionError("Viewport geometry must not be recalculated during use.")

    monkeypatch.setattr(display_module, "calculate_destination_rect", fail_recalculation)
    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    converted_event = viewport.convert_pointer_event(
        pygame.event.Event(
            pygame.MOUSEMOTION,
            pos=(500, 500),
            rel=(0, 0),
            buttons=(0, 0, 0),
        )
    )
    viewport.present()

    assert viewport.destination_rect == expected_rect
    assert converted_event.pos == (640, 360)
    assert output_surface.blit_calls[-1][1] == expected_rect


def test_viewport_recalculates_geometry_only_after_successful_recreation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_output = pygame.Surface(LOGICAL_SIZE)
    viewport = DisplayViewport(LOGICAL_SIZE, original_output)
    original_rect = viewport.destination_rect
    calculation_calls: list[tuple[tuple[int, int], tuple[int, int]]] = []

    def fail_creation(
        size: tuple[int, int],
        *,
        fullscreen: bool,
    ) -> pygame.Surface:
        del size, fullscreen
        raise DisplayModeChangeError("mode unavailable")

    def record_calculation(
        logical_size: tuple[int, int],
        output_size: tuple[int, int],
    ) -> pygame.Rect:
        calculation_calls.append((logical_size, output_size))
        return pygame.Rect(0, 96, 1024, 576)

    monkeypatch.setattr(display_module, "create_display_surface", fail_creation)
    monkeypatch.setattr(display_module, "calculate_destination_rect", record_calculation)

    with pytest.raises(DisplayModeChangeError, match="mode unavailable"):
        viewport.recreate_output((1024, 768), fullscreen=False)

    assert viewport.output_surface is original_output
    assert viewport.destination_rect == original_rect
    assert calculation_calls == []

    new_output = pygame.Surface((1024, 768))
    monkeypatch.setattr(
        display_module,
        "create_display_surface",
        lambda size, *, fullscreen: new_output,
    )

    viewport.recreate_output((1024, 768), fullscreen=False)

    assert viewport.output_surface is new_output
    assert viewport.destination_rect == pygame.Rect(0, 96, 1024, 576)
    assert calculation_calls == [(LOGICAL_SIZE, (1024, 768))]


def test_viewport_destination_rect_is_not_mutable_by_callers() -> None:
    viewport = DisplayViewport(LOGICAL_SIZE, pygame.Surface((1000, 1000)))

    external_rect = viewport.destination_rect
    external_rect.x = 123

    assert viewport.destination_rect == pygame.Rect(0, 219, 1000, 562)
