from pathlib import Path

import pygame

from game.asset_ids import (
    ANCIENT_PEDESTAL_IMAGE,
    DIALOGUE_SOUND,
    EMPTY_CUP_IMAGE,
    FOREST_PATH_BACKGROUND,
    MOON_HERB_IMAGE,
    MUSHROOM_GUARD_IMAGE,
    NOTICE_BOARD_IMAGE,
    OLD_WELL_IMAGE,
    PATH_EXIT_IMAGE,
    PICKUP_SOUND,
    RETIRED_WITCH_IMAGE,
    SCENE_TRANSITION_SOUND,
    SUSPICIOUS_STUMP_IMAGE,
    TITLE_BACKGROUND,
    TOWER_GATE_IMAGE,
    TOWER_INTERIOR_BACKGROUND,
    UNLOCK_SOUND,
    VILLAGE_SQUARE_BACKGROUND,
)
from game.ui.resources import UIResources

pygame.font.init()


def test_ui_resources_caches_fonts_by_size() -> None:
    resources = UIResources()

    assert resources.font(30) is resources.font(30)
    assert resources.body_font is resources.font(30)


def test_ui_resources_exposes_asset_paths_by_stable_id() -> None:
    resources = UIResources(asset_root=Path("assets"))

    assert resources.image_path("scene.village") == Path("assets/images/scene.village.png")
    assert resources.audio_path("music.theme") == Path("assets/audio/music.theme.ogg")


def test_ui_resources_loads_and_caches_scaled_images(tmp_path: Path) -> None:
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    source = pygame.Surface((10, 10))
    pygame.image.save(source, image_dir / "test.image.png")
    resources = UIResources(asset_root=tmp_path)

    first = resources.image("test.image", (20, 30))
    second = resources.image("test.image", (20, 30))

    assert first is second
    assert first is not None
    assert first.get_size() == (20, 30)


def test_ui_resources_missing_optional_assets_are_non_fatal(tmp_path: Path) -> None:
    resources = UIResources(asset_root=tmp_path)

    assert resources.image("missing.image") is None
    assert resources.sound("missing.sound") is None
    resources.play_sound("missing.sound")


def test_demo_placeholder_asset_files_exist() -> None:
    resources = UIResources()
    image_ids = (
        TITLE_BACKGROUND,
        VILLAGE_SQUARE_BACKGROUND,
        FOREST_PATH_BACKGROUND,
        TOWER_INTERIOR_BACKGROUND,
        NOTICE_BOARD_IMAGE,
        OLD_WELL_IMAGE,
        EMPTY_CUP_IMAGE,
        RETIRED_WITCH_IMAGE,
        PATH_EXIT_IMAGE,
        MUSHROOM_GUARD_IMAGE,
        MOON_HERB_IMAGE,
        SUSPICIOUS_STUMP_IMAGE,
        TOWER_GATE_IMAGE,
        ANCIENT_PEDESTAL_IMAGE,
    )
    sound_ids = (
        PICKUP_SOUND,
        DIALOGUE_SOUND,
        UNLOCK_SOUND,
        SCENE_TRANSITION_SOUND,
    )

    assert all(resources.image_path(asset_id).is_file() for asset_id in image_ids)
    assert all(resources.audio_path(asset_id).is_file() for asset_id in sound_ids)


def test_default_assets_work_from_another_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    resources = UIResources()
    assert resources.image_path(TITLE_BACKGROUND).is_file()
    assert resources.audio_path(PICKUP_SOUND).is_file()


def test_frozen_assets_use_bundle_directory(tmp_path, monkeypatch) -> None:
    import sys

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    assert UIResources().asset_root == tmp_path / "assets"
