from __future__ import annotations

import csv
from pathlib import Path

import requests
from joblib import Parallel, delayed
from tqdm import tqdm

from .constants import BASE_URL, ImageSize, VideoSize


class PexelDownloader:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = BASE_URL

    def _log_to_csv(
        self,
        content_id: int,
        author_name: str,
        profile_url: str,
        file_path: str,
        content_type: str,
        csv_file: str = "downloaded_content.csv",
    ) -> None:
        csv_path = Path(csv_file)
        if not csv_path.exists():
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Content ID", "Author", "Profile URL", "File Path", "Content Type"])
        with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([content_id, author_name, profile_url, file_path, content_type])

    def search_images(self, query: str, per_page: int = 80, page: int = 1) -> dict:
        url = f"{self.base_url}search"
        headers = {"Authorization": self.api_key}
        params = {"query": query, "per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def search_videos(self, query: str, per_page: int = 80, page: int = 1) -> dict:
        url = f"{self.base_url}videos/search"
        headers = {"Authorization": self.api_key}
        params = {"query": query, "per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def _download_image(self, img_url: str, img_name: str) -> None:
        img_data = requests.get(img_url).content
        with open(img_name, "wb") as handler:
            handler.write(img_data)

    def _download_video(self, video_url: str, video_name: str) -> None:
        video_data = requests.get(video_url, stream=True)
        with open(video_name, "wb") as handler:
            for chunk in video_data.iter_content(chunk_size=1024):
                if chunk:
                    handler.write(chunk)

    def download_images(
        self,
        query: str,
        num_images: int,
        save_directory: str | Path,
        size: str = "original",
        page: int = 1,
    ) -> None:
        save_directory = Path(save_directory)
        save_directory.mkdir(parents=True, exist_ok=True)
        if size not in ImageSize.__members__:
            raise ValueError(f"size must be one of {[s.value for s in ImageSize]}")

        images: list[dict] = []
        while len(images) < num_images:
            result = self.search_images(query=query, per_page=80, page=page)
            images.extend(result["photos"])
            page += 1
            if not result["photos"]:
                break
        images = images[:num_images]

        def process_image(img: dict) -> None:
            img_url = img["src"][size]
            author = img["photographer"]
            profile_url = img["photographer_url"]
            img_name_suffix = author.lower().replace(" ", "_").split("/")[0].split("\\")[0]
            img_name = str(save_directory / f"{img['id']}_{img_name_suffix}.jpg")
            self._download_image(img_url, img_name)
            self._log_to_csv(
                content_id=img["id"],
                author_name=author,
                profile_url=profile_url,
                file_path=img_name,
                content_type="image",
                csv_file=str(save_directory / "downloaded_content.csv"),
            )

        Parallel(n_jobs=-1)(delayed(process_image)(img) for img in tqdm(images, desc="Downloading ..."))

    def download_videos(
        self,
        query: str,
        num_videos: int,
        save_directory: str | Path,
        size: str = "medium",
        page: int = 1,
    ) -> None:
        save_directory = Path(save_directory)
        save_directory.mkdir(parents=True, exist_ok=True)
        if size not in VideoSize.__members__:
            raise ValueError(f"size must be one of {[s.value for s in VideoSize]}")

        videos: list[dict] = []
        while len(videos) < num_videos:
            result = self.search_videos(query=query, per_page=80, page=page)
            videos.extend(result["videos"])
            page += 1
            if not result["videos"]:
                break
        videos = videos[:num_videos]

        def process_video(video: dict) -> None:
            video_files = video["video_files"]
            video_url = next(
                (file["link"] for file in video_files if file["quality"] == size),
                video_files[0]["link"],
            )
            author = video["user"]["name"]
            profile_url = video["user"]["url"]
            video_name_suffix = author.lower().replace(" ", "_").split("/")[0].split("\\")[0]
            video_name = str(save_directory / f"{video['id']}_{video_name_suffix}.mp4")
            self._download_video(video_url, video_name)
            self._log_to_csv(
                content_id=video["id"],
                author_name=author,
                profile_url=profile_url,
                file_path=video_name,
                content_type="video",
                csv_file=str(save_directory / "downloaded_content.csv"),
            )

        Parallel(n_jobs=-1)(delayed(process_video)(video) for video in tqdm(videos, desc="Downloading videos..."))
