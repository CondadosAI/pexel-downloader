import pytest

from pexel_downloader.client import PexelDownloader


@pytest.fixture
def downloader():
    return PexelDownloader(api_key="test-api-key")


@pytest.fixture
def mock_image_search_response():
    return {
        "photos": [
            {
                "id": 123,
                "photographer": "Test Author",
                "photographer_url": "https://pexels.com/@test",
                "src": {
                    "original": "https://example.com/photo_original.jpg",
                    "large2x": "https://example.com/photo_large2x.jpg",
                    "large": "https://example.com/photo_large.jpg",
                    "medium": "https://example.com/photo_medium.jpg",
                    "small": "https://example.com/photo_small.jpg",
                    "portrait": "https://example.com/photo_portrait.jpg",
                    "landscape": "https://example.com/photo_landscape.jpg",
                    "tiny": "https://example.com/photo_tiny.jpg",
                },
            }
        ],
        "total_results": 1,
    }


@pytest.fixture
def mock_video_search_response():
    return {
        "videos": [
            {
                "id": 456,
                "user": {"name": "Test Author", "url": "https://pexels.com/@test"},
                "video_files": [
                    {"quality": "large", "link": "https://example.com/video_large.mp4"},
                    {"quality": "medium", "link": "https://example.com/video_medium.mp4"},
                    {"quality": "small", "link": "https://example.com/video_small.mp4"},
                ],
            }
        ],
        "total_results": 1,
    }
