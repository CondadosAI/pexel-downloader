import os
from pathlib import Path
from typing import Annotated

import typer
from requests import HTTPError

from .client import PexelDownloader
from .config import get_api_key, get_content_type, get_download_dir, get_size, save_config
from .constants import ContentType, ImageSize, VideoSize

app = typer.Typer(help="Download images and videos from Pexels.")

ALL_SIZES = sorted({s.value for s in ImageSize} | {s.value for s in VideoSize})


def _resolve_api_key() -> str:
    """Resolve API key: env var > config file > interactive prompt."""
    api_key = os.getenv("PEXEL_API_KEY")
    if api_key:
        return api_key

    api_key = get_api_key()
    if api_key:
        return api_key

    api_key = typer.prompt("Please enter your Pexels API key", hide_input=True)
    save = typer.confirm("Save API key for future use?", default=True)
    if save:
        path = save_config(api_key=api_key)
        typer.echo(f"[INFO] API key saved to {path}")
    return api_key


@app.command()
def download(
    query: Annotated[str, typer.Argument(help="The search term for the content.")],
    num: Annotated[int, typer.Argument(help="Number of images or videos to download.")],
    content_type: Annotated[
        ContentType | None,
        typer.Argument(help="Type of content to download (image or video).", case_sensitive=False),
    ] = None,
    size: Annotated[
        str | None, typer.Option(help="Size of the image or video.")
    ] = None,
    save_directory: Annotated[
        str | None, typer.Option("--save-directory", "-o", help="Directory to save downloaded files.")
    ] = None,
    start_page: Annotated[
        int, typer.Option("--start-page", "-p", help="Page number to start downloading from.")
    ] = 1,
) -> None:
    """Download images or videos from Pexels."""
    api_key = _resolve_api_key()
    downloader = PexelDownloader(api_key=api_key)

    if content_type is None:
        content_type = ContentType(get_content_type())
    if size is None:
        size = get_size()
    if save_directory is None:
        save_directory = get_download_dir()

    try:
        if content_type == ContentType.image:
            downloader.download_images(
                query=query, num_images=num, save_directory=save_directory, size=size, page=start_page
            )
        else:
            downloader.download_videos(
                query=query, num_videos=num, save_directory=save_directory, size=size, page=start_page
            )
    except HTTPError as e:
        typer.echo(f"[ERROR] Pexels API error: {e}", err=True)
        raise typer.Exit(1)

    absolute_path = Path(save_directory).resolve()
    typer.echo(f"[INFO] Downloaded {num} {content_type.value}s to {absolute_path}")


@app.command()
def config(
    api_key: Annotated[
        str | None, typer.Option("--api-key", "-k", help="Your Pexels API key.")
    ] = None,
    download_dir: Annotated[
        str | None, typer.Option("--download-dir", "-d", help="Default download directory.")
    ] = None,
    content_type: Annotated[
        ContentType | None, typer.Option("--content-type", "-t", help="Default content type (image or video).", case_sensitive=False)
    ] = None,
    size: Annotated[
        str | None, typer.Option("--size", "-s", help="Default size for downloads.")
    ] = None,
) -> None:
    """Configure pexel-downloader settings."""
    interactive = api_key is None and download_dir is None and content_type is None and size is None

    if interactive:
        api_key = typer.prompt("Pexels API key", default=get_api_key() or "", hide_input=True)
        download_dir = typer.prompt("Default download directory", default=get_download_dir())
        import click

        content_type = ContentType(
            typer.prompt(
                "Default content type (image/video)",
                default=get_content_type(),
                type=click.Choice([t.value for t in ContentType], case_sensitive=False),
            )
        )
        size = typer.prompt(
            f"Default size ({', '.join(ALL_SIZES)})",
            default=get_size(),
        )

    path = save_config(
        api_key=api_key if api_key else None,
        download_dir=download_dir,
        content_type=content_type.value if content_type else None,
        size=size,
    )
    typer.echo(f"[INFO] Configuration saved to {path}")


def cli() -> None:
    app()


if __name__ == "__main__":
    cli()
