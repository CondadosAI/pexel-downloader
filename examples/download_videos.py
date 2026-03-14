import os

from pexel_downloader import PexelDownloader

api_key = os.environ.get("PEXEL_API_KEY")
downloader = PexelDownloader(api_key=api_key)
downloader.download_videos(query="nature", num_videos=5, save_directory="./videos", size="medium")
