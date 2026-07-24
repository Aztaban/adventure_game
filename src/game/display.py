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
) -> pygame.Rect:
    """Scale one logical frame into the physical output with black unused space."""
    destination_rect = calculate_destination_rect(
        logical_surface.get_size(),
        output_surface.get_size(),
    )

    output_surface.fill(LETTERBOX_COLOR)

    if destination_rect.size == logical_surface.get_size():
        presented_surface = logical_surface
    else:
        presented_surface = pygame.transform.smoothscale(
            logical_surface,
            destination_rect.size,
        )

    output_surface.blit(presented_surface, destination_rect)
    return destination_rect
