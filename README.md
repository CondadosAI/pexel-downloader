# pexel-downloader

[![CI](https://github.com/Gabriellgpc/pexel-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/Gabriellgpc/pexel-downloader/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pexel-downloader)](https://pypi.org/project/pexel-downloader/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pexel-downloader)](https://pypi.org/project/pexel-downloader/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Download high-quality photos and videos from [Pexels.com](https://www.pexels.com/) with a simple CLI.

![pexel-downloader](https://github.com/Gabriellgpc/pexel-downloader/raw/main/pexel_downloader-logo.jpg)

## Quick Start

### 1. Install

```bash
# Using uv (recommended)
uv tool install pexel-downloader

# Or using pip
pip install pexel-downloader
```

### 2. Set your API key

Create a free account at [pexels.com](https://www.pexels.com/) to get an API key, then run:

```bash
pexel-downloader config --api-key YOUR_API_KEY
```

Or just run `pexel-downloader config` and you'll be prompted to enter it.

### 3. Download

```bash
# Download 10 images of nature (uses your configured defaults)
pexel-downloader download nature 10

# Download 5 videos of ocean
pexel-downloader download ocean 5 video
```

That's it! Files are saved to your configured download directory (default: `downloads/`) and the full path is shown after each download.

---

## Installation

### Prerequisites

- **Python 3.10+**
- **Pexels account** for an API key: [pexels.com](https://www.pexels.com/)

### Install uv

[uv](https://docs.astral.sh/uv/) is a fast Python package manager.

**Linux / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip (any platform):**
```bash
pip install uv
```

### Install pexel-downloader

**As a CLI tool [recommend]:**
```bash
uv tool install pexel-downloader
```

**As a library in your project:**
```bash
uv add pexel-downloader
```

**Run without installing:**
```bash
uvx pexel-downloader download nature 5 image
```

---

## Configuration

### Interactive setup

Run `pexel-downloader config` to configure all settings at once. You'll be prompted for:

- **API key** — your Pexels API key
- **Download directory** — where files are saved (default: `downloads`)
- **Content type** — `image` or `video` (default: `image`)
- **Size** — download size (default: `medium`)

```bash
pexel-downloader config
```

### Set individual settings

```bash
pexel-downloader config --api-key YOUR_API_KEY
pexel-downloader config --download-dir ~/Pictures/pexels
pexel-downloader config --content-type video
pexel-downloader config --size large
```

The configuration is stored at:
- **Linux:** `~/.config/pexel-downloader/config.json`
- **macOS:** `~/Library/Application Support/pexel-downloader/config.json`
- **Windows:** `C:\Users\<user>\AppData\Roaming\pexel-downloader\config.json`

### API key via environment variable

You can also use the `PEXEL_API_KEY` environment variable (takes priority over the config file):

**Linux / macOS:**
```bash
export PEXEL_API_KEY="your_api_key"
```

**Windows (Command Prompt):**
```cmd
set PEXEL_API_KEY=your_api_key
```

**Windows (PowerShell):**
```powershell
$env:PEXEL_API_KEY = "your_api_key"
```

---

## CLI Usage

```bash
pexel-downloader download QUERY NUM [CONTENT_TYPE] [OPTIONS]
```

`CONTENT_TYPE` is optional — if omitted, uses your configured default (`image` by default).

### Examples

```bash
# Download 10 images of "nature" (uses default content type and size)
pexel-downloader download nature 10

# Download 5 videos of "ocean" starting from page 2
pexel-downloader download ocean 5 video --start-page 2

# Specify output directory and size
pexel-downloader download cats 20 image --size large -o ./my_images

# Show help
pexel-downloader --help
pexel-downloader download --help
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--size` | | from config or `medium` | Size of the image or video |
| `--save-directory` | `-o` | from config or `downloads` | Directory to save files |
| `--start-page` | `-p` | `1` | Page number to start from |

### Available sizes

**Images:** original, large2x, large, medium, small, portrait, landscape, tiny

**Videos:** large, medium, small

---

## Python API

```python
import os
from pexel_downloader import PexelDownloader

api_key = os.environ.get("PEXEL_API_KEY")
downloader = PexelDownloader(api_key=api_key)

# Download images
downloader.download_images(query="beaches", num_images=100, save_directory="./images")

# Download videos
downloader.download_videos(query="nature", num_videos=5, save_directory="./videos", size="medium")

# Search without downloading
results = downloader.search_images(query="sunset", per_page=10)
print(results["photos"])
```

---

## Demonstration

<img width="663" height="625" alt="Screenshot" src="https://github.com/user-attachments/assets/48ad0040-a82f-4005-97bc-765c4e50af58" />
<img width="684" height="471" alt="Screenshot" src="https://github.com/user-attachments/assets/c8523d89-71fe-443a-b457-205bed77b223" />
<img width="895" height="66" alt="Screenshot" src="https://github.com/user-attachments/assets/6667dc07-76d7-4415-a13d-6a3c35fd43c0" />

---

## Development

```bash
# Clone the repo
git clone https://github.com/Gabriellgpc/pexel-downloader.git
cd pexel-downloader

# Install dependencies (including dev)
uv sync --group dev

# Run tests
uv run pytest tests/ -v

# Run the CLI locally
uv run pexel-downloader --help
```

## Publishing

Versioning is automatic — derived from git tags using [hatch-vcs](https://github.com/ofek/hatch-vcs). To release:

1. `git tag v0.5.0`
2. `git push origin v0.5.0`
3. Create a GitHub release from that tag
4. The workflow builds and publishes to PyPI automatically

**First-time setup:** Configure [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) for your GitHub repository and create a GitHub environment named `pypi`.

## License

MIT License. See [LICENSE](LICENSE) for details.
