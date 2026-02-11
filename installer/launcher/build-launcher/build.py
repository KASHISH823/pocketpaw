#!/usr/bin/env python3
# PocketPaw Desktop Launcher — Build Script
# Builds the launcher into a native app for the current platform.
# Created: 2026-02-10
#
# Usage:
#   python installer/launcher/build/build.py
#
# Requirements:
#   pip install pyinstaller pystray Pillow

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent  # repo root
SPEC_FILE = Path(__file__).parent / "launcher.spec"
DIST_DIR = ROOT / "dist" / "launcher"


def check_deps() -> bool:
    """Verify build dependencies are installed."""
    missing = []
    for pkg in ("PyInstaller", "pystray", "PIL"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg.lower() if pkg != "PIL" else "Pillow")

    if missing:
        print(f"Missing build dependencies: {', '.join(missing)}")
        print(f"Run: pip install {' '.join(missing)}")
        return False
    return True


def build() -> int:
    """Run the PyInstaller build."""
    if not check_deps():
        return 1

    print(f"Building PocketPaw Launcher for {platform.system()}...")
    print(f"Spec file: {SPEC_FILE}")
    print(f"Output: {DIST_DIR}")
    print()

    # Clean previous build
    build_dir = ROOT / "build" / "launcher"
    if build_dir.exists():
        shutil.rmtree(build_dir)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(SPEC_FILE),
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(build_dir),
        "--clean",
        "--noconfirm",
    ]

    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=str(ROOT))

    if result.returncode == 0:
        print("\nBuild successful!")
        print(f"Output: {DIST_DIR / 'PocketPaw'}")

        if platform.system() == "Darwin":
            app_path = DIST_DIR / "PocketPaw.app"
            if app_path.exists():
                print(f"macOS app: {app_path}")
                print("\nTo create .dmg:")
                print(
                    f"  hdiutil create -volname PocketPaw -srcfolder {app_path} -ov -format UDZO {DIST_DIR / 'PocketPaw.dmg'}"
                )

        elif platform.system() == "Windows":
            exe_path = DIST_DIR / "PocketPaw" / "PocketPaw.exe"
            if exe_path.exists():
                print(f"Windows exe: {exe_path}")
                print(
                    f"\nTo create installer, use Inno Setup or NSIS with the {DIST_DIR / 'PocketPaw'} folder."
                )

    return result.returncode


if __name__ == "__main__":
    sys.exit(build())
