import os

from pexel_downloader import PexelDownloader

api_key = os.environ.get("PEXEL_API_KEY")
downloader = PexelDownloader(api_key=api_key)
downloader.download_images(query="beaches", num_images=100, save_directory="./images")
