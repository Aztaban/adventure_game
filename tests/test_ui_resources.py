import pygame

from game.ui.resources import UIResources

pygame.font.init()


def test_ui_resources_caches_fonts_by_size() -> None:
    resources = UIResources()

    assert resources.font(30) is resources.font(30)
    assert resources.body_font is resources.font(30)


def test_ui_resources_exposes_future_asset_paths_by_stable_id() -> None:
    resources = UIResources()

    assert str(resources.image_path("scene.village")) == ("assets/images/scene.village.png")
    assert str(resources.audio_path("music.theme")) == "assets/audio/music.theme.ogg"
