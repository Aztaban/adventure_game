from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pygame


@dataclass
class UIResources:
    """Own shared cached fonts and optional image/audio assets."""

    asset_root: Path = Path("assets")
    _font_cache: dict[int, pygame.font.Font] = field(default_factory=dict)
    _image_cache: dict[tuple[str, tuple[int, int] | None], pygame.Surface | None] = field(default_factory=dict)
    _sound_cache: dict[str, pygame.mixer.Sound | None] = field(default_factory=dict)

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
        return self.font(31)

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

    @property
    def menu_title_font(self) -> pygame.font.Font:
        """Return the title/ending heading font."""
        return self.font(78)

    @property
    def menu_subtitle_font(self) -> pygame.font.Font:
        """Return the title/ending supporting text font."""
        return self.font(32)

    @property
    def menu_button_font(self) -> pygame.font.Font:
        """Return the title/ending button font."""
        return self.font(38)

    def image_path(self, asset_id: str) -> Path:
        """Return the future image path for a stable image asset ID."""
        return self.asset_root / "images" / f"{asset_id}.png"

    def audio_path(self, asset_id: str) -> Path:
        """Return the future audio path for a stable audio asset ID."""
        return self.asset_root / "audio" / f"{asset_id}.ogg"

    def image(
        self,
        asset_id: str | None,
        size: tuple[int, int] | None = None,
    ) -> pygame.Surface | None:
        """Load and cache an optional image, scaled to the requested size."""
        if asset_id is None:
            return None

        cache_key = (asset_id, size)

        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        path = self.image_path(asset_id)

        try:
            image = pygame.image.load(path)

            if size is not None and image.get_size() != size:
                image = pygame.transform.smoothscale(image, size)
        except (FileNotFoundError, OSError, pygame.error):
            image = None

        self._image_cache[cache_key] = image
        return image

    def sound(self, asset_id: str) -> pygame.mixer.Sound | None:
        """Load and cache an optional sound when the mixer is available."""
        if asset_id in self._sound_cache:
            return self._sound_cache[asset_id]

        if pygame.mixer.get_init() is None:
            self._sound_cache[asset_id] = None
            return None

        try:
            sound = pygame.mixer.Sound(self.audio_path(asset_id))
        except (FileNotFoundError, OSError, pygame.error):
            sound = None

        self._sound_cache[asset_id] = sound
        return sound

    def play_sound(
        self,
        asset_id: str | None,
        *,
        volume: float = 0.55,
    ) -> None:
        """Play an optional cached sound without making missing assets fatal."""
        if asset_id is None:
            return

        sound = self.sound(asset_id)

        if sound is None:
            return

        sound.set_volume(max(0.0, min(1.0, volume)))
        sound.play()
