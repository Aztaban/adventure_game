from __future__ import annotations

import pygame

LETTERBOX_COLOR = (0, 0, 0)


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
