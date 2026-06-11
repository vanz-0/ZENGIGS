#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
Motion Graphics Overlay

Adds professional motion graphics to scene clips:
  - Lower third (name/title bar) at scene start
  - Animated fade-in / fade-out on the lower third
  - Optional scene number badge (top-right)
  - Optional ZENGIGS watermark (bottom-right)
  - Platform-specific exports: horizontal (YouTube/LinkedIn), vertical (TikTok/IG Reels)

Usage:
    # Basic - add lower thirds to all clips in done_videos/
    python execution/motion_graphics.py done_videos/

    # With custom label
    python execution/motion_graphics.py done_videos/ --name "Evans" --title "AI & Automation Expert"

    # Export vertical versions too (for TikTok/IG)
    python execution/motion_graphics.py done_videos/ --platforms all

    # No lower third, just watermark
    python execution/motion_graphics.py done_videos/ --no-lower-third --watermark
"""

import argparse
import os
import subprocess
import time
from pathlib import Path

import static_ffmpeg
static_ffmpeg.add_paths()


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

BRAND_NAME   = "ZENGIGS"
BRAND_COLOR  = "0x7C6DFA"   # purple accent (hex for drawbox)
TEXT_COLOR   = "white"
SHADOW_COLOR = "black@0.6"

# Lower third display: show for first N seconds of clip
LOWER_THIRD_DURATION = 4.0   # seconds


# ──────────────────────────────────────────────────────────────────────────────
# FFmpeg Filter Builders
# ──────────────────────────────────────────────────────────────────────────────

def build_lower_third_filter(name: str, title: str, video_width: int = 1920, video_height: int = 1080) -> str:
    """
    Build an FFmpeg drawtext filter chain that produces an animated lower third:
    - Solid purple accent bar (bottom-left)
    - Name text (large, white, bold)
    - Title text (smaller, light purple)
    - Fade in over 0.3s, hold, fade out over 0.3s
    """
    fade_in_end   = 0.3
    hold_end      = LOWER_THIRD_DURATION - 0.3
    fade_out_end  = LOWER_THIRD_DURATION

    # Alpha expression: fade in, hold, fade out
    alpha_expr = (
        f"if(lt(t,{fade_in_end}), t/{fade_in_end},"
        f"if(lt(t,{hold_end}), 1,"
        f"if(lt(t,{fade_out_end}), ({fade_out_end}-t)/0.3, 0)))"
    )

    bar_y    = video_height - 120
    name_y   = video_height - 110
    title_y  = video_height - 75

    filters = []

    # 1. Accent bar (drawbox - no alpha support so use drawtext with block char)
    filters.append(
        f"drawbox=x=60:y={bar_y}:w=6:h=80:color=0x7C6DFA@1.0:t=fill"
        f":enable='between(t,0,{fade_out_end})'"
    )

    # 2. Name text
    filters.append(
        f"drawtext=text='{name}':"
        f"fontsize=36:fontcolor={TEXT_COLOR}:fontfile='C\\\\:/Windows/Fonts/arialbd.ttf':"
        f"x=80:y={name_y}:"
        f"shadowcolor={SHADOW_COLOR}:shadowx=2:shadowy=2:"
        f"alpha='{alpha_expr}'"
    )

    # 3. Title text (slightly muted)
    filters.append(
        f"drawtext=text='{title}':"
        f"fontsize=22:fontcolor=CCBBFF:fontfile='C\\\\:/Windows/Fonts/arial.ttf':"
        f"x=80:y={title_y}:"
        f"shadowcolor={SHADOW_COLOR}:shadowx=1:shadowy=1:"
        f"alpha='{alpha_expr}'"
    )

    return ",".join(filters)


def build_watermark_filter(brand: str, video_width: int = 1920, video_height: int = 1080) -> str:
    """Small brand watermark in the bottom-right corner."""
    return (
        f"drawtext=text='{brand}':"
        f"fontsize=18:fontcolor=white@0.45:"
        f"fontfile='C\\\\:/Windows/Fonts/arial.ttf':"
        f"x=w-tw-24:y=h-th-20"
    )


def build_scene_badge_filter(scene_num: int) -> str:
    """Scene number badge in top-right corner."""
    return (
        f"drawtext=text='#{scene_num:03d}':"
        f"fontsize=20:fontcolor=white@0.6:"
        f"fontfile='C\\\\:/Windows/Fonts/arialbd.ttf':"
        f"x=w-tw-24:y=24:"
        f"shadowcolor=black@0.5:shadowx=1:shadowy=1"
    )


# ──────────────────────────────────────────────────────────────────────────────
# Platform Export
# ──────────────────────────────────────────────────────────────────────────────

def apply_motion_graphics(
    clip_path: str,
    output_path: str,
    name: str,
    title: str,
    scene_num: int,
    lower_third: bool = True,
    watermark: bool = True,
    badge: bool = False,
    vertical: bool = False
):
    """Apply motion graphics overlay and optionally reformat for platform."""
    filters = []

    # Vertical crop for TikTok/IG (9:16 from centre of 16:9)
    if vertical:
        filters.append("crop=ih*9/16:ih:(iw-ih*9/16)/2:0")
        filters.append("scale=1080:1920")

    if lower_third:
        w = 1080 if vertical else 1920
        h = 1920 if vertical else 1080
        filters.append(build_lower_third_filter(name, title, w, h))

    if watermark:
        filters.append(build_watermark_filter(BRAND_NAME))

    if badge:
        filters.append(build_scene_badge_filter(scene_num))

    vf = ",".join(filters) if filters else "copy"

    cmd = [
        "ffmpeg", "-y",
        "-i", clip_path,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "copy",
        "-movflags", "+faststart",
        "-loglevel", "error",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    [ERR] {result.stderr[:400]}")
        return False
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Main Pipeline
# ──────────────────────────────────────────────────────────────────────────────

def process_folder(
    folder: str,
    name: str,
    title: str,
    platforms: str = "horizontal",
    lower_third: bool = True,
    watermark: bool = True,
    badge: bool = False,
):
    """Apply motion graphics to all scene clips in folder."""
    clips = sorted(Path(folder).glob("*_scene_*.mp4"))
    # Exclude already-processed files
    clips = [c for c in clips if "_mg_" not in c.stem and "_captioned" not in c.stem]

    if not clips:
        print(f"[WARN] No scene clips (*_scene_*.mp4) found in: {folder}")
        return

    do_horizontal = platforms in ("horizontal", "all")
    do_vertical   = platforms in ("vertical", "all")

    print(f"\n[MG] Motion Graphics Pipeline")
    print(f"     Clips      : {len(clips)}")
    print(f"     Name       : {name}")
    print(f"     Title      : {title}")
    print(f"     Platforms  : {platforms}")
    print(f"     Lower Third: {lower_third}")
    print()

    overall_start = time.time()
    done = 0

    for clip in clips:
        clip_path = str(clip)
        stem      = clip.stem
        parent    = clip.parent

        # Extract scene number from filename
        try:
            scene_num = int(stem.split("_scene_")[-1])
        except ValueError:
            scene_num = clips.index(clip) + 1

        print(f"[{clips.index(clip)+1}/{len(clips)}] {clip.name}")
        t0 = time.time()

        if do_horizontal:
            out_h = str(parent / f"{stem}_mg_horizontal.mp4")
            ok = apply_motion_graphics(
                clip_path, out_h, name, title, scene_num,
                lower_third=lower_third, watermark=watermark, badge=badge,
                vertical=False
            )
            if ok:
                size_mb = os.path.getsize(out_h) / (1024 * 1024)
                print(f"    [H] Horizontal -> {os.path.basename(out_h)} ({size_mb:.1f} MB)")
                done += 1

        if do_vertical:
            out_v = str(parent / f"{stem}_mg_vertical.mp4")
            ok = apply_motion_graphics(
                clip_path, out_v, name, title, scene_num,
                lower_third=lower_third, watermark=watermark, badge=badge,
                vertical=True
            )
            if ok:
                size_mb = os.path.getsize(out_v) / (1024 * 1024)
                print(f"    [V] Vertical   -> {os.path.basename(out_v)} ({size_mb:.1f} MB)")
                done += 1

        print(f"    [{time.time()-t0:.1f}s]")
        print()

    total = time.time() - overall_start
    print("=" * 60)
    print(f"[DONE] {done} output(s) created in {total:.1f}s")
    print(f"       Output: {folder}/")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Add motion graphics (lower thirds, watermark) to scene clips"
    )
    parser.add_argument("folder", help="Folder containing scene clip .mp4 files")
    parser.add_argument("--name", default="Evans", help="Person name for lower third")
    parser.add_argument("--title", default="AI & Automation | ZenGigs", help="Title for lower third")
    parser.add_argument(
        "--platforms", default="horizontal",
        choices=["horizontal", "vertical", "all"],
        help="Export format: horizontal (16:9), vertical (9:16), or all (default: horizontal)"
    )
    parser.add_argument("--no-lower-third", action="store_true", help="Skip lower third overlay")
    parser.add_argument("--watermark", action="store_true", default=True, help="Add ZENGIGS watermark")
    parser.add_argument("--badge", action="store_true", help="Add scene number badge (top-right)")
    args = parser.parse_args()

    process_folder(
        folder=args.folder,
        name=args.name,
        title=args.title,
        platforms=args.platforms,
        lower_third=not args.no_lower_third,
        watermark=args.watermark,
        badge=args.badge,
    )


if __name__ == "__main__":
    main()
