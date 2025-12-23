#!/usr/bin/env python3
"""
Script to bump version in setup.py
"""
import re
import sys

def bump_version(setup_file='setup.py'):
    """Bump the patch version in setup.py"""
    with open(setup_file, 'r') as f:
        content = f.read()
    
    # Find current version
    version_pattern = r"version='(\d+)\.(\d+)\.(\d+)'"
    match = re.search(version_pattern, content)
    
    if not match:
        print("Error: Could not find version in setup.py")
        sys.exit(1)
    
    major, minor, patch = match.groups()
    current_version = f"{major}.{minor}.{patch}"
    
    # Bump patch version
    new_patch = int(patch) + 1
    new_version = f"{major}.{minor}.{new_patch}"
    
    # Replace version in content
    new_content = content.replace(
        f"version='{current_version}'",
        f"version='{new_version}'"
    )
    
    # Write back
    with open(setup_file, 'w') as f:
        f.write(new_content)
    
    print(f"Version bumped from {current_version} to {new_version}")
    print(f"::set-output name=new_version::{new_version}")
    print(f"new_version={new_version}")
    
    return new_version

if __name__ == '__main__':
    bump_version()
