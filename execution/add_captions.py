#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
Add Captions (Transcription + Burn-In)

For each scene clip in a folder:
  1. Runs Whisper to transcribe speech -> generates .srt subtitle file
  2. Burns subtitles into the video using FFmpeg (white text, black outline)
  3. Also saves a plain .txt transcript alongside each clip

Usage:
    python execution/add_captions.py done_videos/
    python execution/add_captions.py done_videos/ --model base
    python execution/add_captions.py done_videos/ --model medium --no-burn
"""

import argparse
import os
import subprocess
import time
from pathlib import Path

import static_ffmpeg
static_ffmpeg.add_paths()


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def format_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def whisper_to_srt(segments, output_path: str):
    """Convert Whisper segments to a .srt subtitle file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_srt_time(seg["start"])
            end   = format_srt_time(seg["end"])
            text  = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def whisper_to_txt(segments, output_path: str):
    """Save full plain-text transcript."""
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(seg["text"].strip() + " ")


# ──────────────────────────────────────────────────────────────────────────────
# Transcription
# ──────────────────────────────────────────────────────────────────────────────

def transcribe_clip(clip_path: str, model_name: str = "base"):
    """Run Whisper on a single clip. Returns list of segments."""
    import whisper
    print(f"    [WHISPER] Transcribing with '{model_name}' model...")
    model = whisper.load_model(model_name)
    result = model.transcribe(clip_path, fp16=False)
    print(f"    [WHISPER] Done - {len(result['segments'])} segment(s) detected")
    return result["segments"]


# ──────────────────────────────────────────────────────────────────────────────
# Caption Burn-In
# ──────────────────────────────────────────────────────────────────────────────

def burn_captions(clip_path: str, srt_path: str, output_path: str):
    """
    Burn subtitles from an .srt file into the video using FFmpeg subtitles filter.
    Style: white text, black outline, bottom-center.
    """
    # Use absolute path with forward slashes for FFmpeg on Windows
    srt_abs = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")

    subtitle_style = (
        "FontName=Arial,"
        "FontSize=22,"
        "PrimaryColour=&H00FFFFFF,"   # white
        "OutlineColour=&H00000000,"   # black outline
        "BackColour=&H80000000,"      # semi-transparent background
        "Bold=1,"
        "Outline=2,"
        "Shadow=0,"
        "Alignment=2,"               # bottom-center
        "MarginV=30"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", clip_path,
        "-vf", f"subtitles='{srt_abs}':force_style='{subtitle_style}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "copy",
        "-movflags", "+faststart",
        "-loglevel", "error",
        output_path
    ]

    print(f"    [BURN] Burning captions into video...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    [ERR] FFmpeg error: {result.stderr[:400]}")
        return False
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Main Pipeline
# ──────────────────────────────────────────────────────────────────────────────

def process_folder(folder: str, model_name: str = "base", burn: bool = True):
    """Process all MP4 clips in a folder: transcribe + optionally burn captions."""
    clips = sorted(Path(folder).glob("*.mp4"))

    # Skip clips that already have _captioned suffix
    clips = [c for c in clips if "_captioned" not in c.stem]

    if not clips:
        print(f"[WARN] No MP4 clips found in: {folder}")
        return

    print(f"\n[CAPTION] Processing {len(clips)} clip(s) in: {folder}")
    print(f"          Whisper model : {model_name}")
    print(f"          Burn captions : {burn}")
    print()

    overall_start = time.time()
    success_count = 0

    for clip in clips:
        clip_path = str(clip)
        stem      = clip.stem
        parent    = clip.parent

        srt_path = str(parent / f"{stem}.srt")
        txt_path = str(parent / f"{stem}.txt")
        out_path = str(parent / f"{stem}_captioned.mp4")

        print(f"[{clips.index(clip)+1}/{len(clips)}] {clip.name}")

        # 1. Transcribe
        t0 = time.time()
        try:
            segments = transcribe_clip(clip_path, model_name)
        except Exception as e:
            print(f"    [ERR] Transcription failed: {e}")
            continue

        # 2. Save SRT + TXT
        whisper_to_srt(segments, srt_path)
        whisper_to_txt(segments, txt_path)
        print(f"    [SRT] Saved -> {srt_path}")
        print(f"    [TXT] Saved -> {txt_path}")

        # 3. Burn captions
        if burn:
            ok = burn_captions(clip_path, srt_path, out_path)
            if ok:
                size_mb = os.path.getsize(out_path) / (1024 * 1024)
                print(f"    [OUT] Captioned clip -> {out_path} ({size_mb:.1f} MB)")
                success_count += 1
        else:
            print(f"    [SKIP] Burn-in disabled, only SRT/TXT saved.")
            success_count += 1

        elapsed = time.time() - t0
        print(f"    [TIME] {elapsed:.1f}s")
        print()

    total = time.time() - overall_start
    print("=" * 60)
    print(f"[DONE] {success_count}/{len(clips)} clips captioned in {total:.1f}s")
    print(f"       Output: {folder}/")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe clips with Whisper and burn in captions"
    )
    parser.add_argument("folder", help="Folder containing scene clip .mp4 files")
    parser.add_argument(
        "--model", default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)"
    )
    parser.add_argument(
        "--no-burn", action="store_true",
        help="Transcribe only — do NOT burn captions into video"
    )
    args = parser.parse_args()

    process_folder(
        folder=args.folder,
        model_name=args.model,
        burn=not args.no_burn
    )


if __name__ == "__main__":
    main()
