from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pygame


@dataclass
class UIResources:
    """Small owner for shared UI rendering resources."""

    _font_cache: dict[int, pygame.font.Font] = field(default_factory=dict)
    image_asset_ids: frozenset[str] = field(default_factory=frozenset)
    audio_asset_ids: frozenset[str] = field(default_factory=frozenset)

    def font(self, size: int) -> pygame.font.Font:
        """Return a cached default font at the requested size."""
        font = self._font_cache.get(size)

        if font is None:
            font = pygame.font.Font(None, size)
            self._font_cache[size] = font

        return font

    @property
    def title_font(self) -> pygame.font.Font:
        """Return the scene-title font."""
        return self.font(52)

    @property
    def body_font(self) -> pygame.font.Font:
        """Return the normal body font."""
        return self.font(30)

    @property
    def small_font(self) -> pygame.font.Font:
        """Return the small UI font."""
        return self.font(26)

    @property
    def dialogue_font(self) -> pygame.font.Font:
        """Return the dialogue text font."""
        return self.font(32)

    @property
    def hint_font(self) -> pygame.font.Font:
        """Return the hint/helper text font."""
        return self.font(23)

    @property
    def inventory_title_font(self) -> pygame.font.Font:
        """Return the inventory-title font."""
        return self.font(32)

    @property
    def inventory_item_font(self) -> pygame.font.Font:
        """Return the inventory item-row font."""
        return self.font(26)

    @property
    def inventory_status_font(self) -> pygame.font.Font:
        """Return the inventory status font."""
        return self.font(22)

    @property
    def debug_font(self) -> pygame.font.Font:
        """Return the debug overlay font."""
        return self.font(26)

    def image_path(self, asset_id: str) -> Path:
        """Return the future image path for a stable image asset ID."""
        return Path("assets/images") / f"{asset_id}.png"

    def audio_path(self, asset_id: str) -> Path:
        """Return the future audio path for a stable audio asset ID."""
        return Path("assets/audio") / f"{asset_id}.ogg"
