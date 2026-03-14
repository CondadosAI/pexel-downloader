import os
import re
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from pexel_downloader.cli import app

runner = CliRunner()


def _strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


class TestCLIHelp:
    def test_help_exits_successfully(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

    def test_help_shows_commands(self):
        result = runner.invoke(app, ["--help"])
        output = _strip_ansi(result.output)
        assert "download" in output
        assert "config" in output

    def test_download_help_shows_arguments(self):
        result = runner.invoke(app, ["download", "--help"])
        output = _strip_ansi(result.output)
        assert result.exit_code == 0
        assert "QUERY" in output
        assert "NUM" in output

    def test_download_help_shows_options(self):
        result = runner.invoke(app, ["download", "--help"])
        output = _strip_ansi(result.output)
        assert "--size" in output
        assert "--save-directory" in output
        assert "--start-page" in output


class TestCLIDownloadImages:
    @patch.dict(os.environ, {"PEXEL_API_KEY": "fake-key"})
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_download_images(self, mock_cls, tmp_path):
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance

        result = runner.invoke(app, ["download", "nature", "5", "image", "-o", str(tmp_path)])

        assert result.exit_code == 0
        mock_cls.assert_called_once_with(api_key="fake-key")
        mock_instance.download_images.assert_called_once_with(
            query="nature",
            num_images=5,
            save_directory=str(tmp_path),
            size="medium",
            page=1,
        )
        assert "[INFO]" in result.output
        assert str(tmp_path.resolve()) in result.output

    @patch.dict(os.environ, {"PEXEL_API_KEY": "fake-key"})
    @patch("pexel_downloader.cli.get_download_dir", return_value="my_downloads")
    @patch("pexel_downloader.cli.get_content_type", return_value="image")
    @patch("pexel_downloader.cli.get_size", return_value="medium")
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_uses_config_defaults_when_no_flags(self, mock_cls, mock_size, mock_ct, mock_dir):
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance

        result = runner.invoke(app, ["download", "nature", "1"])

        assert result.exit_code == 0
        mock_instance.download_images.assert_called_once()
        call_kwargs = mock_instance.download_images.call_args.kwargs
        assert call_kwargs["save_directory"] == "my_downloads"
        assert call_kwargs["size"] == "medium"

    @patch.dict(os.environ, {"PEXEL_API_KEY": "fake-key"})
    @patch("pexel_downloader.cli.get_download_dir", return_value="downloads")
    @patch("pexel_downloader.cli.get_content_type", return_value="video")
    @patch("pexel_downloader.cli.get_size", return_value="large")
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_uses_config_content_type_and_size(self, mock_cls, mock_size, mock_ct, mock_dir):
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance

        result = runner.invoke(app, ["download", "nature", "3"])

        assert result.exit_code == 0
        mock_instance.download_videos.assert_called_once()
        call_kwargs = mock_instance.download_videos.call_args.kwargs
        assert call_kwargs["size"] == "large"


class TestCLIDownloadVideos:
    @patch.dict(os.environ, {"PEXEL_API_KEY": "fake-key"})
    @patch("pexel_downloader.cli.get_download_dir", return_value="downloads")
    @patch("pexel_downloader.cli.get_size", return_value="medium")
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_download_videos(self, mock_cls, mock_size, mock_dir, tmp_path):
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance

        result = runner.invoke(app, ["download", "ocean", "3", "video", "--size", "large", "-p", "2"])

        assert result.exit_code == 0
        mock_cls.assert_called_once_with(api_key="fake-key")
        mock_instance.download_videos.assert_called_once_with(
            query="ocean",
            num_videos=3,
            save_directory="downloads",
            size="large",
            page=2,
        )


class TestCLIContentType:
    @patch.dict(os.environ, {"PEXEL_API_KEY": "fake-key"})
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_case_insensitive_content_type(self, mock_cls):
        mock_cls.return_value = MagicMock()

        result = runner.invoke(app, ["download", "nature", "1", "Image"])
        assert result.exit_code == 0


class TestCLIMissingApiKey:
    @patch.dict(os.environ, {}, clear=True)
    @patch("pexel_downloader.cli.get_api_key", return_value=None)
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_prompts_for_api_key_and_saves(self, mock_cls, mock_get_key):
        mock_cls.return_value = MagicMock()

        result = runner.invoke(app, ["download", "nature", "1", "image"], input="my-secret-key\ny\n")

        assert result.exit_code == 0
        mock_cls.assert_called_once_with(api_key="my-secret-key")

    @patch.dict(os.environ, {}, clear=True)
    @patch("pexel_downloader.cli.get_api_key", return_value="saved-key")
    @patch("pexel_downloader.cli.PexelDownloader")
    def test_uses_config_file_key(self, mock_cls, mock_get_key):
        mock_cls.return_value = MagicMock()

        result = runner.invoke(app, ["download", "nature", "1", "image"])

        assert result.exit_code == 0
        mock_cls.assert_called_once_with(api_key="saved-key")


class TestConfigCommand:
    def test_config_api_key_flag(self):
        with patch("pexel_downloader.cli.save_config", return_value="/fake/config.json") as mock_save:
            result = runner.invoke(app, ["config", "--api-key", "my-key"])

        assert result.exit_code == 0
        mock_save.assert_called_once_with(
            api_key="my-key", download_dir=None, content_type=None, size=None
        )

    def test_config_download_dir_flag(self):
        with patch("pexel_downloader.cli.save_config", return_value="/fake/config.json") as mock_save:
            result = runner.invoke(app, ["config", "--download-dir", "/my/downloads"])

        assert result.exit_code == 0
        mock_save.assert_called_once_with(
            api_key=None, download_dir="/my/downloads", content_type=None, size=None
        )

    def test_config_content_type_flag(self):
        with patch("pexel_downloader.cli.save_config", return_value="/fake/config.json") as mock_save:
            result = runner.invoke(app, ["config", "--content-type", "video"])

        assert result.exit_code == 0
        mock_save.assert_called_once_with(
            api_key=None, download_dir=None, content_type="video", size=None
        )

    def test_config_size_flag(self):
        with patch("pexel_downloader.cli.save_config", return_value="/fake/config.json") as mock_save:
            result = runner.invoke(app, ["config", "--size", "large"])

        assert result.exit_code == 0
        mock_save.assert_called_once_with(
            api_key=None, download_dir=None, content_type=None, size="large"
        )

    def test_config_interactive_prompts_all(self):
        with patch("pexel_downloader.cli.save_config", return_value="/fake/config.json") as mock_save, \
             patch("pexel_downloader.cli.get_api_key", return_value=None), \
             patch("pexel_downloader.cli.get_download_dir", return_value="downloads"), \
             patch("pexel_downloader.cli.get_content_type", return_value="image"), \
             patch("pexel_downloader.cli.get_size", return_value="medium"):
            # Input: api_key, download_dir, content_type, size
            result = runner.invoke(app, ["config"], input="my-key\n~/pics\nimage\nlarge\n")

        assert result.exit_code == 0
        mock_save.assert_called_once()
        call_kwargs = mock_save.call_args.kwargs
        assert call_kwargs["api_key"] == "my-key"
        assert call_kwargs["download_dir"] == "~/pics"
        assert call_kwargs["content_type"] == "image"
        assert call_kwargs["size"] == "large"
