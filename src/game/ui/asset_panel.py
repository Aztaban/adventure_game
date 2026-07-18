from __future__ import annotations

import pygame

from game.theme import PANEL_BACKGROUND, TEXT_PRIMARY


def draw_labeled_asset(
    surface: pygame.Surface,
    rect: pygame.Rect,
    font: pygame.font.Font,
    label: str,
    image: pygame.Surface | None,
    *,
    background_color: tuple[int, int, int],
    border_color: tuple[int, int, int],
    border_radius: int = 8,
    overlay_color: tuple[int, int, int, int] | None = None,
) -> None:
    """Draw an image-backed target with a readable fallback and label."""
    pygame.draw.rect(
        surface,
        background_color,
        rect,
        border_radius=border_radius,
    )

    if image is not None:
        surface.blit(image, rect)

    if overlay_color is not None:
        overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        overlay.fill(overlay_color)
        surface.blit(overlay, rect)

    label_height = min(rect.height, font.get_height() + 12)
    label_rect = pygame.Rect(
        rect.x,
        rect.bottom - label_height,
        rect.width,
        label_height,
    )

    label_background = pygame.Surface(label_rect.size, pygame.SRCALPHA)
    label_background.fill((*PANEL_BACKGROUND, 215))
    surface.blit(label_background, label_rect)

    pygame.draw.rect(
        surface,
        border_color,
        rect,
        width=2,
        border_radius=border_radius,
    )

    label_surface = font.render(label, True, TEXT_PRIMARY)
    label_rect_for_text = label_surface.get_rect(center=label_rect.center)
    surface.blit(label_surface, label_rect_for_text)
