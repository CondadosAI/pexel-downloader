import json
from unittest.mock import patch

from pexel_downloader.config import (
    get_api_key,
    get_content_type,
    get_download_dir,
    get_size,
    save_config,
)


class TestConfigApiKey:
    def test_get_api_key_no_config(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            assert get_api_key() is None

    def test_save_and_get_api_key(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(api_key="test-key-123")
            assert get_api_key() == "test-key-123"

    def test_save_creates_directory(self, tmp_path):
        fake_path = tmp_path / "subdir" / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(api_key="test-key")
            assert fake_path.parent.exists()
            assert fake_path.exists()

    def test_save_returns_path(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            result = save_config(api_key="test-key")
            assert result == fake_path

    def test_save_preserves_other_fields(self, tmp_path):
        fake_path = tmp_path / "config.json"
        fake_path.write_text(json.dumps({"download_dir": "/my/dir"}))
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(api_key="new-key")
            config = json.loads(fake_path.read_text())
            assert config["api_key"] == "new-key"
            assert config["download_dir"] == "/my/dir"


class TestConfigDownloadDir:
    def test_get_download_dir_default(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            assert get_download_dir() == "downloads"

    def test_save_and_get_download_dir(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(download_dir="/my/downloads")
            assert get_download_dir() == "/my/downloads"


class TestConfigContentType:
    def test_get_content_type_default(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            assert get_content_type() == "image"

    def test_save_and_get_content_type(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(content_type="video")
            assert get_content_type() == "video"


class TestConfigSize:
    def test_get_size_default(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            assert get_size() == "medium"

    def test_save_and_get_size(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(size="large")
            assert get_size() == "large"


class TestSaveAllFields:
    def test_save_all_at_once(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(api_key="key", download_dir="/dir", content_type="video", size="small")
            assert get_api_key() == "key"
            assert get_download_dir() == "/dir"
            assert get_content_type() == "video"
            assert get_size() == "small"

    def test_save_only_updates_provided_fields(self, tmp_path):
        fake_path = tmp_path / "config.json"
        with patch("pexel_downloader.config._config_path", return_value=fake_path):
            save_config(api_key="my-key", content_type="video")
            save_config(download_dir="/new/dir", size="large")
            assert get_api_key() == "my-key"
            assert get_content_type() == "video"
            assert get_download_dir() == "/new/dir"
            assert get_size() == "large"
