from __future__ import annotations

import pygame

LETTERBOX_COLOR = (0, 0, 0)
POINTER_EVENT_TYPES = frozenset(
    {
        pygame.MOUSEMOTION,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP,
    }
)


class DisplayModeChangeError(RuntimeError):
    """Raised when Pygame cannot create an approved display mode."""


def primary_desktop_size() -> tuple[int, int]:
    """Return the configured size of the primary desktop."""
    try:
        desktop_sizes = pygame.display.get_desktop_sizes()
    except pygame.error as error:
        raise DisplayModeChangeError(f"Could not read the desktop display size: {error}") from error

    if not desktop_sizes:
        raise DisplayModeChangeError("Pygame did not report an available desktop display.")

    width, height = desktop_sizes[0]

    if width <= 0 or height <= 0:
        raise DisplayModeChangeError(f"Pygame reported an invalid desktop display size: {width} x {height}.")

    return int(width), int(height)


def create_display_surface(
    size: tuple[int, int],
    *,
    fullscreen: bool,
) -> pygame.Surface:
    """Create one fullscreen-desktop or approved windowed display surface."""
    flags = pygame.FULLSCREEN if fullscreen else 0
    mode_name = "fullscreen desktop" if fullscreen else f"{size[0]} x {size[1]} windowed"

    try:
        return pygame.display.set_mode(size, flags)
    except pygame.error as error:
        raise DisplayModeChangeError(f"Could not switch to {mode_name} mode: {error}") from error


def calculate_destination_rect(
    logical_size: tuple[int, int],
    output_size: tuple[int, int],
) -> pygame.Rect:
    """Return the largest centered logical frame that preserves its aspect ratio."""
    logical_width, logical_height = logical_size
    output_width, output_height = output_size

    if logical_width <= 0 or logical_height <= 0:
        raise ValueError("Logical display dimensions must be positive.")

    if output_width <= 0 or output_height <= 0:
        raise ValueError("Physical display dimensions must be positive.")

    if output_width * logical_height <= output_height * logical_width:
        scaled_width = output_width
        scaled_height = max(1, output_width * logical_height // logical_width)
    else:
        scaled_height = output_height
        scaled_width = max(1, output_height * logical_width // logical_height)

    offset_x = (output_width - scaled_width) // 2
    offset_y = (output_height - scaled_height) // 2
    return pygame.Rect(offset_x, offset_y, scaled_width, scaled_height)


def physical_to_logical_position(
    physical_position: tuple[int, int],
    logical_size: tuple[int, int],
    destination_rect: pygame.Rect,
) -> tuple[int, int] | None:
    """Map one physical pointer position into logical coordinates.

    Positions in letterbox or pillarbox space return ``None`` so callers can
    treat them as non-interactive.
    """
    logical_width, logical_height = logical_size

    if logical_width <= 0 or logical_height <= 0:
        raise ValueError("Logical display dimensions must be positive.")

    if destination_rect.width <= 0 or destination_rect.height <= 0:
        raise ValueError("Presentation rectangle dimensions must be positive.")

    if not destination_rect.collidepoint(physical_position):
        return None

    local_x = physical_position[0] - destination_rect.left
    local_y = physical_position[1] - destination_rect.top

    logical_x = min(
        logical_width - 1,
        (local_x * logical_width + destination_rect.width // 2) // destination_rect.width,
    )
    logical_y = min(
        logical_height - 1,
        (local_y * logical_height + destination_rect.height // 2) // destination_rect.height,
    )
    return logical_x, logical_y


def convert_pointer_event(
    event: pygame.event.Event,
    logical_size: tuple[int, int],
    destination_rect: pygame.Rect,
) -> pygame.event.Event:
    """Return a pointer event whose position uses logical coordinates."""
    if event.type not in POINTER_EVENT_TYPES or not hasattr(event, "pos"):
        return event

    attributes = event.dict.copy()
    attributes["pos"] = physical_to_logical_position(
        event.pos,
        logical_size,
        destination_rect,
    )
    return pygame.event.Event(event.type, attributes)


def present_logical_surface(
    logical_surface: pygame.Surface,
    output_surface: pygame.Surface,
    destination_rect: pygame.Rect,
) -> None:
    """Present one logical frame using already-calculated viewport geometry."""
    output_surface.fill(LETTERBOX_COLOR)

    if destination_rect.size == logical_surface.get_size():
        presented_surface = logical_surface
    else:
        presented_surface = pygame.transform.smoothscale(
            logical_surface,
            destination_rect.size,
        )

    output_surface.blit(presented_surface, destination_rect)


class DisplayViewport:
    """Own logical rendering, physical presentation and pointer conversion."""

    def __init__(
        self,
        logical_size: tuple[int, int],
        output_surface: pygame.Surface,
    ) -> None:
        self.logical_surface = pygame.Surface(logical_size)
        self.logical_surface.fill(LETTERBOX_COLOR)
        self._output_surface = output_surface
        self._destination_rect = calculate_destination_rect(logical_size, output_surface.get_size())

    @classmethod
    def create(
        cls,
        logical_size: tuple[int, int],
        output_size: tuple[int, int],
        *,
        fullscreen: bool,
    ) -> DisplayViewport:
        """Create the physical display and its authoritative logical viewport."""
        return cls(logical_size, create_display_surface(output_size, fullscreen=fullscreen))

    @property
    def logical_size(self) -> tuple[int, int]:
        """Return fixed logical drawing size."""
        return self.logical_surface.get_size()

    @property
    def output_surface(self) -> pygame.Surface:
        """Return the active physical display surface."""
        return self._output_surface

    @property
    def output_size(self) -> tuple[int, int]:
        """Return the active physical output size."""
        return self._output_surface.get_size()

    @property
    def destination_rect(self) -> pygame.Rect:
        """Return a copy of the authoritative physical presentation rectangle."""
        return self._destination_rect.copy()

    def recreate_output(
        self,
        size: tuple[int, int],
        *,
        fullscreen: bool,
    ) -> None:
        """Replace the physical display after succesful creation only."""
        new_output_surface = create_display_surface(size, fullscreen=fullscreen)
        new_destination_rect = calculate_destination_rect(
            self.logical_size,
            new_output_surface.get_size(),
        )
        self._output_surface = new_output_surface
        self._destination_rect = new_destination_rect

    def convert_pointer_event(self, event: pygame.event.Event) -> pygame.event.Event:
        """Translate a physical pointer event through this viewport."""
        return convert_pointer_event(
            event,
            self.logical_size,
            self._destination_rect,
        )

    def present(self) -> None:
        """Scale and flip the current logical frame through this viewport."""
        present_logical_surface(
            self.logical_surface,
            self._output_surface,
            self._destination_rect,
        )
        pygame.display.flip()
