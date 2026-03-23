#!/usr/bin/env python3
"""
Uninstall script for yt-dlp Web UI.
Removes installed Python packages and optionally deletes downloads/cookies folders.
Note: Python and ffmpeg are not uninstalled because they may be used by other applications.
"""

import os
import sys
import platform
import subprocess
import shutil

SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"

def run_cmd(cmd, check=False):
    """Run a shell command."""
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\n{e}")
        return False
    return True

def uninstall_pip_package(package):
    """Uninstall a Python package via pip."""
    print(f"Uninstalling {package}...")
    run_cmd(f"{sys.executable} -m pip uninstall -y {package}")

def main():
    print("=" * 50)
    print("yt-dlp Web UI - Uninstall Script")
    print("=" * 50)

    # Ask for confirmation
    confirm = input("This will remove installed Python packages (yt-dlp, Flask).\n"
                    "Optionally, it can also delete the downloads/ and cookies/ folders.\n"
                    "Proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        sys.exit(0)

    # Uninstall yt-dlp and Flask
    uninstall_pip_package("yt-dlp")
    uninstall_pip_package("flask")

    # Optionally remove downloads and cookies folders
    remove_data = input("Delete the 'downloads' and 'cookies' folders? (y/N): ").strip().lower()
    if remove_data == 'y':
        folders = ["downloads", "cookies"]
        for folder in folders:
            path = os.path.join(os.path.dirname(__file__), folder)
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    print(f"Removed {folder}/")
                except Exception as e:
                    print(f"Error removing {folder}: {e}")
            else:
                print(f"{folder}/ not found.")

    print("=" * 50)
    print("Uninstall completed.")
    print("Note: Python and ffmpeg are still installed on your system.")
    print("If you want to remove them, please do so manually using your package manager.")
    print("=" * 50)

if __name__ == "__main__":
    main()