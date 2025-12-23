# pexel-downloader
"Pexel Downloader: Python-based web scraper for effortlessly downloading high-quality photos and videos from Pexels.com, open-source with MIT License."

![pexel-downloader](https://github.com/Gabriellgpc/pexel-downloader/raw/main/pexel_downloader-logo.jpg)

📷 **Pexel Downloader - Your Gateway to Stunning Visuals!** 🎥
---
Welcome to the Pexel Downloader, a Python-based web scraper designed to help you effortlessly gather high-quality photos and videos from the Pexels.com website. Whether you're a content creator, developer, or just a visual enthusiast, this open-source tool is here to simplify your media acquisition process.

## ✨ Features
---
- Download photos and videos from Pexels easily.
- MIT License: Free to use, modify, and contribute to.
- Flexible command-line interface (CLI) for quick downloads.
- Integrates smoothly with Python projects.

Pexel Downloader offers a user-friendly interface, robust performance, and the flexibility to fit seamlessly into your projects. Join our community of developers and creators, and together, let's make this tool even better.

## 🤓 Demonstration
---
-  <img width="663" height="625" alt="Screenshot_20251106_211640" src="https://github.com/user-attachments/assets/48ad0040-a82f-4005-97bc-765c4e50af58" />
- <img width="684" height="471" alt="Screenshot_20251106_203553" src="https://github.com/user-attachments/assets/c8523d89-71fe-443a-b457-205bed77b223" />
- <img width="895" height="66" alt="Screenshot_20251106_203649" src="https://github.com/user-attachments/assets/6667dc07-76d7-4415-a13d-6a3c35fd43c0" />
---

### Prerequisites
- **Python**: You’ll need Python 3.7 or later installed.
- **Pexels acccount**: You'll need Pexels Account to create your own API key [pexels.com](https://www.pexels.com/).

#### How to Install Python

1. **Windows**:
   - Download the latest version of Python from [python.org](https://www.python.org/downloads/).
   - Run the installer and check "Add Python to PATH" during installation.
   - Verify by opening Command Prompt and typing `python --version`.

2. **Linux**:
   - Open Terminal and install Python with your package manager:
     ```bash
     sudo apt-get update -y
     sudo apt-get install python3
     ```
   - Verify installation:
     ```bash
     python3 --version
     ```

### Installing Pexel Downloader
---
Once Python is installed, you can install Pexel Downloader directly from Python pip package manager:

```bash
pip install pexel-downloader
```

#### 🔑 API Key Setup
---
To use Pexel Downloader, you need a Pexels API key:
1. Create an Account on Pexels 
2. Set API Key:
    - Recommended: Set your API key as an environment variable PEXEL_API_KEY. Set your API key as system environment variable but to prevent by running/writing `export PEXEL_API_KEY = "YOUR_API_KEY"` in terminal as root & copy/pasting it into `/etc/profile` (for all users) or `~/.profile` (for yourself).
    - Alternatively: Pexel Downloader will prompt you to enter it securely when you run it where you'll have to enter the key mannually or by copy/pasting it.


#### ⚠️Warning- I have only tested setting the API Key as an Environment Variable in Linux, not in Windows 
---
1. **Windows**:
    ```bash
    setx PEXEL_API_KEY "your_actual_api_key"
    ```
2. **Linux**:
    ```bash
    export PEXEL_API_KEY="your_actual_api_key"
    ```

Replace your_actual_api_key with the your key you received from Pexels.


## 🔄 CI/CD
---
This project uses GitHub Actions for automated testing, publishing to PyPI, and creating releases. Every merge to the main branch automatically:
- Tests the package on Linux, macOS, and Windows (Python 3.8-3.12)
- Bumps the version number
- Publishes to PyPI
- Creates a GitHub release

For more details, see [`.github/README.md`](.github/README.md).


📜 **License:**
---
Pexel Downloader is released under the MIT License, granting you the freedom to use and modify it for your projects.


Get started with Pexel Downloader today, and elevate your visual content game. Happy scraping!
