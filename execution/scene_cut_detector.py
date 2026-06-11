#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
Scene Cut Detector - Visual Background/Character Change Detection

Detects scene changes (background/character changes) in videos using
PySceneDetect ContentDetector. Generates a visual HTML report with
thumbnails at every cut point, then splits the video into separate clips.

Usage:
    python execution/scene_cut_detector.py raw/Evans_Clones.mp4
    python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --threshold 20
    python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --preview-only

Threshold guide:
    15-20  = Very sensitive (catches subtle lighting/color shifts)
    25-30  = Default, good for background + character changes
    35-45  = Only hard cuts / major scene changes
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import static_ffmpeg
static_ffmpeg.add_paths()


# ──────────────────────────────────────────────────────────────────────────────
# Scene Detection
# ──────────────────────────────────────────────────────────────────────────────

def detect_scenes(input_path: str, threshold: float = 27.0):
    """
    Detect visual scene changes using PySceneDetect ContentDetector.
    Returns list of (start_timecode, end_timecode) tuples.
    """
    from scenedetect import detect, ContentDetector

    print(f"[SCENE] Scanning for visual changes...")
    print(f"        Threshold: {threshold}  (lower = more sensitive)")
    print(f"        Input:     {input_path}")
    print()

    scene_list = detect(input_path, ContentDetector(threshold=threshold))

    print(f"[SCENE] Found {len(scene_list)} scene(s) / {len(scene_list)-1} cut point(s)")
    for i, (start, end) in enumerate(scene_list):
        duration = end.seconds - start.seconds
        print(f"        Scene {i+1:03d}:  {start.get_timecode()} -> {end.get_timecode()}  ({duration:.1f}s)")

    return scene_list


# ──────────────────────────────────────────────────────────────────────────────
# Thumbnail Extraction
# ──────────────────────────────────────────────────────────────────────────────

def extract_thumbnail(video_path: str, timestamp_sec: float, output_path: str):
    """Extract a single JPEG thumbnail from the video at a given timestamp."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{timestamp_sec:.3f}",
        "-i", video_path,
        "-vframes", "1",
        "-vf", "scale=400:225:force_original_aspect_ratio=decrease,pad=400:225:(ow-iw)/2:(oh-ih)/2",
        "-q:v", "4",
        "-loglevel", "error",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)


def extract_all_thumbnails(video_path: str, scene_list: list, thumbs_dir: str):
    """Extract one thumbnail per scene (at start + 0.5s offset)."""
    os.makedirs(thumbs_dir, exist_ok=True)
    print(f"\n[THUMB] Extracting {len(scene_list)} thumbnails...")

    thumb_paths = []
    for i, (start, end) in enumerate(scene_list):
        start_sec = start.seconds
        # Grab frame 0.5s into each scene (avoids transition blur)
        sample_sec = min(start_sec + 0.5, end.seconds - 0.1)
        thumb_path = os.path.join(thumbs_dir, f"scene_{i+1:03d}.jpg")
        extract_thumbnail(video_path, sample_sec, thumb_path)
        thumb_paths.append(thumb_path)
        print(f"        Scene {i+1:03d} @ {sample_sec:.2f}s -> {thumb_path}")

    return thumb_paths


# ──────────────────────────────────────────────────────────────────────────────
# HTML Visual Report
# ──────────────────────────────────────────────────────────────────────────────

def generate_html_report(input_path: str, scene_list: list, thumb_paths: list, output_html: str):
    """Generate a rich HTML report showing every detected cut point."""
    video_name = Path(input_path).name
    total_duration = scene_list[-1][1].get_seconds() if scene_list else 0

    scene_cards = ""
    for i, ((start, end), thumb_path) in enumerate(zip(scene_list, thumb_paths)):
        start_sec = start.seconds
        end_sec   = end.seconds
        duration  = end_sec - start_sec
        start_tc  = start.get_timecode()
        end_tc    = end.get_timecode()

        # Make thumbnail path relative to the HTML file
        rel_thumb = os.path.relpath(thumb_path, os.path.dirname(output_html)).replace("\\", "/")
        is_last   = (i == len(scene_list) - 1)

        cut_badge = "" if is_last else f'<span class="cut-badge">CUT @ {end_tc}</span>'

        scene_cards += f"""
        <div class="scene-card" id="scene-{i+1}">
          <div class="scene-thumb-wrap">
            <img class="scene-thumb" src="{rel_thumb}" alt="Scene {i+1}" loading="lazy"
                 onerror="this.parentElement.innerHTML='<div class=\\'no-thumb\\'>No Preview</div>'">
            <div class="scene-number">#{i+1}</div>
          </div>
          <div class="scene-info">
            <div class="scene-title">Scene {i+1}</div>
            <div class="timecodes">
              <span class="tc start">▶ {start_tc}</span>
              <span class="tc end">⏹ {end_tc}</span>
            </div>
            <div class="duration">{duration:.2f}s &nbsp;·&nbsp; {duration/60:.1f} min</div>
            {cut_badge}
          </div>
        </div>"""

    n_scenes = len(scene_list)
    n_cuts   = n_scenes - 1

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scene Report — {video_name}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:       #0c0c12;
      --surface:  #14141f;
      --surface2: #1e1e2e;
      --accent:   #7c6dfa;
      --accent2:  #c084fc;
      --text:     #e2e2f0;
      --muted:    #6b6b88;
      --cut:      #f43f5e;
      --border:   #2a2a40;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', system-ui, sans-serif;
      padding: 32px 24px;
      min-height: 100vh;
    }}

    header {{
      margin-bottom: 32px;
    }}
    header h1 {{
      font-size: 1.9rem;
      font-weight: 700;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 6px;
    }}
    header p {{
      color: var(--muted);
      font-size: 0.88rem;
    }}

    .stats-row {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 32px;
    }}
    .stat-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px 24px;
      min-width: 140px;
    }}
    .stat-label {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    .stat-value {{
      font-size: 2rem;
      font-weight: 700;
      color: var(--accent);
    }}
    .stat-unit {{
      font-size: 0.8rem;
      color: var(--muted);
      margin-top: 2px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
    }}

    .scene-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
      cursor: default;
    }}
    .scene-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 32px rgba(124, 109, 250, 0.18);
      border-color: var(--accent);
    }}

    .scene-thumb-wrap {{
      position: relative;
      width: 100%;
      aspect-ratio: 16/9;
      background: var(--surface2);
      overflow: hidden;
    }}
    .scene-thumb {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .no-thumb {{
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      font-size: 0.8rem;
    }}
    .scene-number {{
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(0,0,0,0.72);
      color: #fff;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 20px;
      backdrop-filter: blur(4px);
    }}

    .scene-info {{
      padding: 14px 16px 16px;
    }}
    .scene-title {{
      font-weight: 600;
      font-size: 0.95rem;
      margin-bottom: 8px;
    }}
    .timecodes {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 6px;
    }}
    .tc {{
      font-size: 0.75rem;
      font-family: 'Courier New', monospace;
      background: var(--surface2);
      border-radius: 6px;
      padding: 3px 8px;
      color: var(--muted);
    }}
    .tc.start {{ color: #4ade80; }}
    .tc.end   {{ color: #fb923c; }}
    .duration {{
      font-size: 0.78rem;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .cut-badge {{
      display: inline-block;
      background: rgba(244, 63, 94, 0.12);
      border: 1px solid rgba(244, 63, 94, 0.35);
      color: var(--cut);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 3px 10px;
      border-radius: 20px;
      letter-spacing: 0.02em;
    }}

    footer {{
      margin-top: 48px;
      text-align: center;
      color: var(--muted);
      font-size: 0.78rem;
    }}
  </style>
</head>
<body>

<header>
  <h1>🎬 Scene Detection Report</h1>
  <p>Source: <strong>{video_name}</strong></p>
</header>

<div class="stats-row">
  <div class="stat-card">
    <div class="stat-label">Total Scenes</div>
    <div class="stat-value">{n_scenes}</div>
    <div class="stat-unit">detected</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Cut Points</div>
    <div class="stat-value">{n_cuts}</div>
    <div class="stat-unit">transitions</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Total Duration</div>
    <div class="stat-value">{(total_duration/60):.1f}</div>
    <div class="stat-unit">minutes</div>
  </div>
</div>

<div class="grid">
  {scene_cards}
</div>

<footer>
  Generated by ZenGigs Scene Cut Detector · {time.strftime('%Y-%m-%d %H:%M')}
</footer>

</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[REPORT] Visual report saved → {output_html}")
    return output_html


# ──────────────────────────────────────────────────────────────────────────────
# Video Splitting
# ──────────────────────────────────────────────────────────────────────────────

def split_video_at_scenes(input_path: str, scene_list: list, output_dir: str):
    """Cut video into separate clips at each scene boundary using FFmpeg."""
    video_name = Path(input_path).stem
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[CUT] Splitting into {len(scene_list)} clip(s) → {output_dir}/")

    clips = []
    t0 = time.time()

    for i, (start, end) in enumerate(scene_list):
        start_sec = start.seconds
        end_sec   = end.seconds
        duration  = end_sec - start_sec
        out_path  = os.path.join(output_dir, f"{video_name}_scene_{i+1:03d}.mp4")

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start_sec:.6f}",
            "-i", input_path,
            "-t", f"{duration:.6f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-loglevel", "error",
            out_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and os.path.exists(out_path):
            size_mb = os.path.getsize(out_path) / (1024 * 1024)
            print(f"        Scene {i+1:03d}  {start.get_timecode()} -> {end.get_timecode()}  "
                  f"({duration:.1f}s)  ->  {os.path.basename(out_path)}  [{size_mb:.1f} MB]")
            clips.append(out_path)
        else:
            print(f"        [ERR] Scene {i+1}: {result.stderr[:300]}")

    elapsed = time.time() - t0
    print(f"\n[CUT] Done in {elapsed:.1f}s  —  {len(clips)} clip(s) saved")
    return clips


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Detect visual scene/background changes and cut video at those points",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python execution/scene_cut_detector.py raw/Evans_Clones.mp4
  python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --threshold 20
  python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --preview-only
  python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --output-dir done_videos
        """
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument(
        "--threshold", type=float, default=27.0,
        help="Scene change sensitivity (default: 27.0 | lower=more sensitive)"
    )
    parser.add_argument(
        "--output-dir", default="done_videos",
        help="Folder to save split clips (default: done_videos/)"
    )
    parser.add_argument(
        "--preview-only", action="store_true",
        help="Generate visual report only — do NOT split the video"
    )
    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"[ERR] File not found: {input_path}")
        sys.exit(1)

    video_name = Path(input_path).stem
    thumbs_dir  = os.path.join(".tmp", f"{video_name}_thumbs")
    report_path = os.path.join(".tmp", f"{video_name}_scene_report.html")

    print()
    print("=" * 62)
    print("  SCENE CUT DETECTOR - Visual Background/Character Changes")
    print("=" * 62)
    print(f"  Input   : {input_path}")
    print(f"  Thresh  : {args.threshold}")
    print(f"  Output  : {args.output_dir}/")
    print(f"  Preview : {report_path}")
    print("=" * 62)
    print()

    overall_start = time.time()

    # 1. Detect scenes
    scene_list = detect_scenes(input_path, threshold=args.threshold)

    if not scene_list:
        print("\n[WARN] No scene changes detected. Try a lower --threshold (e.g. 15).")
        sys.exit(0)

    # 2. Extract thumbnails
    thumb_paths = extract_all_thumbnails(input_path, scene_list, thumbs_dir)

    # 3. Generate HTML report
    generate_html_report(input_path, scene_list, thumb_paths, report_path)

    # 4. Split video (unless preview-only)
    if args.preview_only:
        print("\n[INFO] Preview-only mode — skipping video split.")
    else:
        split_video_at_scenes(input_path, scene_list, args.output_dir)

    elapsed = time.time() - overall_start
    print()
    print("=" * 62)
    print(f"  COMPLETE in {elapsed:.1f}s")
    print(f"  Visual report : {report_path}")
    if not args.preview_only:
        print(f"  Clips folder  : {args.output_dir}/")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
