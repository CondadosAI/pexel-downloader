from __future__ import annotations

import json
from pathlib import Path

import typer

APP_NAME = "pexel-downloader"
CONFIG_FILENAME = "config.json"

DEFAULT_DOWNLOAD_DIR = "downloads"
DEFAULT_CONTENT_TYPE = "image"
DEFAULT_SIZE = "medium"


def _config_path() -> Path:
    return Path(typer.get_app_dir(APP_NAME)) / CONFIG_FILENAME


def _read_config() -> dict:
    path = _config_path()
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _write_config(config: dict) -> None:
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n")


def get_api_key() -> str | None:
    """Get API key from config file."""
    return _read_config().get("api_key")


def get_download_dir() -> str:
    """Get default download directory from config file."""
    return _read_config().get("download_dir", DEFAULT_DOWNLOAD_DIR)


def get_content_type() -> str:
    """Get default content type from config file."""
    return _read_config().get("content_type", DEFAULT_CONTENT_TYPE)


def get_size() -> str:
    """Get default size from config file."""
    return _read_config().get("size", DEFAULT_SIZE)


def save_config(
    *,
    api_key: str | None = None,
    download_dir: str | None = None,
    content_type: str | None = None,
    size: str | None = None,
) -> Path:
    """Save config values. Only updates provided fields. Returns the config file path."""
    config = _read_config()
    if api_key is not None:
        config["api_key"] = api_key
    if download_dir is not None:
        config["download_dir"] = download_dir
    if content_type is not None:
        config["content_type"] = content_type
    if size is not None:
        config["size"] = size
    _write_config(config)
    return _config_path()
