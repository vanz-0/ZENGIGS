#!/usr/bin/env python3
"""
setup.py - One-click environment bootstrap for GTA 6 Stream Clipper
Verifies FFmpeg, installs Python packages, and downloads Whisper model.
"""

import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
BIN_DIR = ROOT / "bin"

WHISPER_URL = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin"

def run_cmd(cmd):
    return subprocess.run(cmd, check=True)

def check_python_packages():
    print("📦 Checking Python dependencies...")
    run_cmd([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")])
    print("   ✓ Python packages installed.")

def check_binaries():
    print("🔍 Checking system binaries...")
    ffmpeg_ok = shutil.which("ffmpeg") or (BIN_DIR / ("ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg")).exists()
    if not ffmpeg_ok:
        print("   ⚠️ ffmpeg was not found on your PATH or in bin/.")
        print("      Windows: winget install Gyan.FFmpeg or download from https://ffmpeg.org")
        print("      macOS  : brew install ffmpeg")
        print("      Linux  : sudo apt install ffmpeg")
    else:
        print("   ✓ ffmpeg detected.")

def download_model():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    target = MODELS_DIR / "ggml-small.en.bin"
    if target.exists() and target.stat().st_size > 100_000_000:
        print(f"   ✓ Whisper model already present ({target.stat().st_size / 1e6:.1f} MB).")
        return

    # Check parent workspace cache if running inside clone
    parent_cache = ROOT.parent / ".niche-machine" / "models" / "ggml-small.en.bin"
    if parent_cache.exists():
        print("   ✓ Copying Whisper model from existing cache...")
        shutil.copy(parent_cache, target)
        return

    print("📥 Downloading Whisper small.en model (~487 MB)...")
    try:
        urllib.request.urlretrieve(WHISPER_URL, target)
        print("   ✓ Whisper model downloaded.")
    except Exception as e:
        print(f"   ⚠️ Could not automatically download model: {e}")
        print(f"      Download manually from: {WHISPER_URL}")
        print(f"      and save to: {target}")

def main():
    print("=" * 60)
    print("🚀 GTA 6 Stream Shorts Clipper - Setup")
    print("=" * 60)
    check_python_packages()
    check_binaries()
    download_model()
    print("\n🎉 Setup complete! You are ready to clip.")
    print("   Run: python clipper.py --help\n")

if __name__ == "__main__":
    main()
