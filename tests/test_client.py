import csv
from unittest.mock import MagicMock, patch

import pytest

from pexel_downloader.client import PexelDownloader
from pexel_downloader.constants import BASE_URL


class TestPexelDownloaderInit:
    def test_init_sets_api_key(self, downloader):
        assert downloader.api_key == "test-api-key"

    def test_init_sets_base_url(self, downloader):
        assert downloader.base_url == BASE_URL


class TestSearchImages:
    @patch("pexel_downloader.client.requests.get")
    def test_search_images_calls_correct_url(self, mock_get, downloader):
        mock_response = MagicMock()
        mock_response.json.return_value = {"photos": [], "total_results": 0}
        mock_get.return_value = mock_response

        downloader.search_images("nature", per_page=10, page=1)

        mock_get.assert_called_once_with(
            f"{BASE_URL}search",
            headers={"Authorization": "test-api-key"},
            params={"query": "nature", "per_page": 10, "page": 1},
        )

    @patch("pexel_downloader.client.requests.get")
    def test_search_images_returns_json(self, mock_get, downloader):
        expected = {"photos": [{"id": 1}], "total_results": 1}
        mock_response = MagicMock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        result = downloader.search_images("nature")
        assert result == expected


class TestSearchVideos:
    @patch("pexel_downloader.client.requests.get")
    def test_search_videos_calls_correct_url(self, mock_get, downloader):
        mock_response = MagicMock()
        mock_response.json.return_value = {"videos": [], "total_results": 0}
        mock_get.return_value = mock_response

        downloader.search_videos("ocean", per_page=10, page=2)

        mock_get.assert_called_once_with(
            f"{BASE_URL}videos/search",
            headers={"Authorization": "test-api-key"},
            params={"query": "ocean", "per_page": 10, "page": 2},
        )

    @patch("pexel_downloader.client.requests.get")
    def test_search_videos_returns_json(self, mock_get, downloader):
        expected = {"videos": [{"id": 1}], "total_results": 1}
        mock_response = MagicMock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        result = downloader.search_videos("ocean")
        assert result == expected


class TestDownloadImages:
    def test_invalid_size_raises_value_error(self, downloader, tmp_path):
        with pytest.raises(ValueError, match="size must be one of"):
            downloader.download_images("nature", 1, tmp_path, size="invalid")

    @patch("pexel_downloader.client.requests.get")
    def test_download_images_creates_directory(self, mock_get, downloader, tmp_path, mock_image_search_response):
        mock_search = MagicMock()
        mock_search.json.return_value = mock_image_search_response
        mock_get.return_value = mock_search

        # Mock _download_image to avoid real HTTP calls from joblib subprocesses
        with patch.object(downloader, "_download_image"):
            save_dir = tmp_path / "new_dir"
            downloader.download_images("nature", 1, save_dir, size="medium")

        assert save_dir.exists()

    @patch("pexel_downloader.client.requests.get")
    def test_download_images_creates_csv(self, mock_get, downloader, tmp_path, mock_image_search_response):
        mock_search = MagicMock()
        mock_search.json.return_value = mock_image_search_response
        mock_get.return_value = mock_search

        with patch.object(downloader, "_download_image"):
            downloader.download_images("nature", 1, tmp_path, size="medium")

        csv_file = tmp_path / "downloaded_content.csv"
        assert csv_file.exists()

        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert rows[0] == ["Content ID", "Author", "Profile URL", "File Path", "Content Type"]
            assert rows[1][0] == "123"
            assert rows[1][1] == "Test Author"
            assert rows[1][4] == "image"

    @patch("pexel_downloader.client.requests.get")
    def test_download_images_pagination(self, mock_get, downloader, tmp_path):
        page1 = MagicMock()
        page1.json.return_value = {
            "photos": [
                {
                    "id": i,
                    "photographer": "Author",
                    "photographer_url": "https://pexels.com/@author",
                    "src": {"medium": f"https://example.com/photo_{i}.jpg"},
                }
                for i in range(2)
            ],
            "total_results": 3,
        }
        page2 = MagicMock()
        page2.json.return_value = {
            "photos": [
                {
                    "id": 2,
                    "photographer": "Author",
                    "photographer_url": "https://pexels.com/@author",
                    "src": {"medium": "https://example.com/photo_2.jpg"},
                }
            ],
            "total_results": 3,
        }
        mock_get.side_effect = [page1, page2]

        with patch.object(downloader, "_download_image"):
            downloader.download_images("nature", 3, tmp_path, size="medium")

        # Should have called search twice (pagination)
        assert mock_get.call_count == 2


class TestDownloadVideos:
    def test_invalid_size_raises_value_error(self, downloader, tmp_path):
        with pytest.raises(ValueError, match="size must be one of"):
            downloader.download_videos("nature", 1, tmp_path, size="invalid")

    @patch("pexel_downloader.client.requests.get")
    def test_download_videos_creates_csv(self, mock_get, downloader, tmp_path, mock_video_search_response):
        mock_search = MagicMock()
        mock_search.json.return_value = mock_video_search_response
        mock_get.return_value = mock_search

        with patch.object(downloader, "_download_video"):
            downloader.download_videos("ocean", 1, tmp_path, size="medium")

        csv_file = tmp_path / "downloaded_content.csv"
        assert csv_file.exists()

        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert rows[0] == ["Content ID", "Author", "Profile URL", "File Path", "Content Type"]
            assert rows[1][0] == "456"
            assert rows[1][4] == "video"


class TestLogToCsv:
    def test_creates_csv_with_headers(self, downloader, tmp_path):
        csv_file = str(tmp_path / "test.csv")
        downloader._log_to_csv(1, "Author", "https://example.com", "/path/file.jpg", "image", csv_file)

        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert rows[0] == ["Content ID", "Author", "Profile URL", "File Path", "Content Type"]
            assert rows[1] == ["1", "Author", "https://example.com", "/path/file.jpg", "image"]

    def test_appends_to_existing_csv(self, downloader, tmp_path):
        csv_file = str(tmp_path / "test.csv")
        downloader._log_to_csv(1, "Author1", "https://example.com/1", "/path/1.jpg", "image", csv_file)
        downloader._log_to_csv(2, "Author2", "https://example.com/2", "/path/2.jpg", "video", csv_file)

        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 3  # header + 2 data rows
            assert rows[1][0] == "1"
            assert rows[2][0] == "2"
