# Scene Cut Detector (Visual Change-Based)

Automatically detects **background changes, character changes, and hard cuts** in a video using PySceneDetect's neural ContentDetector. Generates a visual HTML preview of every cut point with thumbnails, then splits the video into separate clips at those boundaries.

## Execution Script

`execution/scene_cut_detector.py`

---

## Quick Start

```bash
# Basic — detect changes and split video (output to done_videos/)
python execution/scene_cut_detector.py raw/Evans_Clones.mp4

# Preview only — generate visual report WITHOUT splitting
python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --preview-only

# More sensitive — catch subtle lighting/color shifts
python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --threshold 15

# Less sensitive — only hard cuts / major background swaps
python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --threshold 40

# Custom output folder
python execution/scene_cut_detector.py raw/Evans_Clones.mp4 --output-dir done_videos
```

---

## What It Does

1. **Detects scene changes** using PySceneDetect `ContentDetector` (compares pixel-level content between frames)
2. **Extracts thumbnails** (one per scene, 0.5s into each) into `.tmp/<videoname>_thumbs/`
3. **Generates HTML report** at `.tmp/<videoname>_scene_report.html` — a visual grid showing every cut point with thumbnails, timecodes, and durations
4. **Splits the video** into separate MP4 clips at every detected scene boundary → `done_videos/`

---

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `input` | required | Input video file |
| `--threshold` | 27.0 | Change sensitivity. Lower = more cuts detected |
| `--output-dir` | `done_videos/` | Where to save split clips |
| `--preview-only` | false | Generate report only, skip video splitting |

---

## Threshold Guide

| Range | Use Case |
|-------|----------|
| 10–18 | Very sensitive — catches lighting flickers, subtle colour shifts |
| 20–27 | Default — good for background/character changes |
| 30–45 | Major scene changes, hard cuts only |

---

## Output

- **Visual Report:** `.tmp/<name>_scene_report.html` — Open in browser to see every cut point with thumbnails
- **Clip Files:** `done_videos/<name>_scene_001.mp4`, `_scene_002.mp4`, etc.
- **Thumbnails:** `.tmp/<name>_thumbs/scene_001.jpg`, etc.

---

## Dependencies

- `scenedetect` — Scene detection (installed via pip)
- `opencv-python` — Video reading backend (already installed)
- `static_ffmpeg` — FFmpeg for thumbnail extraction and video splitting (already installed)
- `Pillow` — Already installed

---

## Known Notes

- Videos are large (~400–650MB) so detection + splitting can take 3–10 minutes depending on video length.
- If too many cuts are detected, raise `--threshold` (e.g. `--threshold 35`).
- If scene changes are being missed, lower `--threshold` (e.g. `--threshold 15`).
- Thumbnails are stored in `.tmp/` and can be deleted freely — they are regenerated each run.
- The HTML report opens in any web browser and requires no internet connection (thumbnails are embedded locally).
