# GitHub Actions CI/CD Workflow

This directory contains GitHub Actions workflows for automated testing, publishing to PyPI, and creating releases.

## Workflows

### `publish.yml` - Publish to PyPI and Create Release

This workflow automatically:
1. Tests the package on multiple platforms (Linux, macOS, Windows) and Python versions (3.8-3.12)
2. Bumps the version number (patch version)
3. Publishes the package to PyPI
4. Creates a GitHub release with automatic release notes

**Trigger:** Push to `main` branch

## Setup Instructions

To enable this workflow, you need to configure the following secret in your GitHub repository:

### Required Secret: `PYPI_API_TOKEN`

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll down to "API tokens" section
3. Click "Add API token"
4. Give it a descriptive name (e.g., "GitHub Actions - pexel-downloader")
5. Set the scope to "Entire account" or limit it to the specific project
6. Copy the generated token (it starts with `pypi-`)
7. Go to your GitHub repository settings
8. Navigate to "Settings" → "Secrets and variables" → "Actions"
9. Click "New repository secret"
10. Name: `PYPI_API_TOKEN`
11. Value: Paste the PyPI token
12. Click "Add secret"

### Permissions

The workflow requires the following permissions (configured automatically):
- `contents: write` - To create releases and push version bumps
- `id-token: write` - For trusted publishing to PyPI

## How It Works

1. **Test Job**: Runs on every push to main, testing across:
   - Operating Systems: Ubuntu, macOS, Windows
   - Python Versions: 3.8, 3.9, 3.10, 3.11, 3.12

2. **Publish Job**: After tests pass:
   - Bumps the patch version in `setup.py` (e.g., 0.4.0 → 0.4.1)
   - Commits the version bump with `[skip ci]` to avoid triggering another workflow
   - Builds the package using `python -m build`
   - Publishes to PyPI using the API token
   - Creates a GitHub release with the new version tag

## Skipping CI

To skip the CI workflow, include `[skip ci]` or `[ci skip]` in your commit message.

## Version Management

The version is automatically bumped on each merge to main. If you need to bump a major or minor version, update the version in `setup.py` manually before merging.

## Troubleshooting

- **PyPI publish fails**: Check that your `PYPI_API_TOKEN` secret is correctly configured
- **Version bump fails**: Ensure the version format in `setup.py` follows `X.Y.Z` pattern
- **Release creation fails**: Verify that the repository has write permissions enabled for Actions
