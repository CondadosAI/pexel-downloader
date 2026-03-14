from enum import Enum

BASE_URL = "https://api.pexels.com/v1/"


class ImageSize(str, Enum):
    original = "original"
    large2x = "large2x"
    large = "large"
    medium = "medium"
    small = "small"
    portrait = "portrait"
    landscape = "landscape"
    tiny = "tiny"


class VideoSize(str, Enum):
    large = "large"
    medium = "medium"
    small = "small"


class ContentType(str, Enum):
    image = "image"
    video = "video"
