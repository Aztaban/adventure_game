import tomllib
from dataclasses import fields
from pathlib import Path

import pytest

import game.save_paths as save_paths_module
from game.save_paths import (
    APPLICATION_NAME,
    MANUAL_SAVE_FILENAME,
    SavePaths,
    resolve_save_paths,
)


def test_default_save_paths_use_approved_platformdirs_identity(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    expected_user_data_dir = tmp_path / "platform-user-data"
    received_arguments: dict[str, object] = {}

    def fake_user_data_path(**kwargs: object) -> Path:
        received_arguments.update(kwargs)
        return expected_user_data_dir

    monkeypatch.setattr(
        save_paths_module.platformdirs,
        "user_data_path",
        fake_user_data_path,
    )

    paths = resolve_save_paths()

    assert received_arguments == {
        "appname": "Mysterious Forest",
        "appauthor": False,
        "ensure_exists": False,
    }
    assert APPLICATION_NAME == "Mysterious Forest"
    assert MANUAL_SAVE_FILENAME == "save.json"
    assert paths.user_data_dir == expected_user_data_dir
    assert paths.manual_save_path == expected_user_data_dir / "save.json"
    assert not expected_user_data_dir.exists()
    assert not paths.manual_save_path.exists()


def test_injected_user_data_directory_bypasses_platform_lookup(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    injected_user_data_dir = tmp_path / "injected-user-data"

    def fail_platform_lookup(**kwargs: object) -> Path:
        del kwargs
        pytest.fail("platformdirs should not be called for an injected path")

    monkeypatch.setattr(
        save_paths_module.platformdirs,
        "user_data_path",
        fail_platform_lookup,
    )

    paths = resolve_save_paths(user_data_dir=injected_user_data_dir)

    assert paths.user_data_dir == injected_user_data_dir
    assert paths.manual_save_path == injected_user_data_dir / MANUAL_SAVE_FILENAME
    assert not injected_user_data_dir.exists()
    assert not paths.manual_save_path.exists()


def test_save_paths_expose_no_settings_or_config_location() -> None:
    assert [field.name for field in fields(SavePaths)] == [
        "user_data_dir",
        "manual_save_path",
    ]


def test_platformdirs_is_a_runtime_dependency() -> None:
    project_root = Path(__file__).resolve().parents[1]

    with (project_root / "pyproject.toml").open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    runtime_dependencies = pyproject["project"]["dependencies"]
    development_dependencies = pyproject["project"]["optional-dependencies"]["dev"]

    assert "platformdirs" in runtime_dependencies
    assert "platformdirs" not in development_dependencies

    with (project_root / "poetry.lock").open("rb") as lock_file:
        lock_data = tomllib.load(lock_file)

    platformdirs_package = next(
        package
        for package in lock_data["package"]
        if package["name"] == "platformdirs"
    )

    assert platformdirs_package["optional"] is False
    assert platformdirs_package["groups"] == ["main"]
