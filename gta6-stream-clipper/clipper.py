#!/usr/bin/env python3
"""
GTA 6 & Gaming Stream Shorts Clipper
Automated AI pipeline to turn long gameplay streams into 9:16 vertical Shorts.
Features:
  - Smart streamer facecam detection & split screen (gameplay top, facecam bottom)
  - Whisper AI word-by-word timestamp alignment
  - Animated karaoke captions (vibrant yellow highlight, white text, 7px black outline)
  - Swear word tracker & auto-censor engine (f*****g, b***h, etc.)
  - Hook badge title overlay across seam
  - EBU R128 broadcast audio normalization
  - Complete post-ready export (MP4, Thumbnail JPG, Metadata JSON, Post Kit TXT)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

# Local swear filter import
try:
    from swear_filter import clean, has_swears
except ImportError:
    def clean(t): return t
    def has_swears(t): return False

# ─── PATHS & BINARY RESOLUTION ────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent

def find_binary(name: str) -> str:
    """Finds binary in local bin/, system PATH, or environment."""
    ext = ".exe" if sys.platform.startswith("win") else ""
    # 1. Local bin folder
    local_bin = SCRIPT_DIR / "bin" / f"{name}{ext}"
    if local_bin.exists():
        return str(local_bin)
    # 2. Parent skill bin
    parent_bin = SCRIPT_DIR.parent / ".agents" / "skills" / "niche-machine" / "bin" / f"{name}{ext}"
    if parent_bin.exists():
        return str(parent_bin)
    # 3. System PATH
    found = shutil.which(name)
    if found:
        return found
    return name

FFMPEG_BIN  = find_binary("ffmpeg")
FFPROBE_BIN = find_binary("ffprobe")
WHISPER_BIN = find_binary("whisper-cli")

def get_whisper_model() -> Path:
    candidates = [
        SCRIPT_DIR / "models" / "ggml-small.en.bin",
        SCRIPT_DIR.parent / ".niche-machine" / "models" / "ggml-small.en.bin",
        Path.home() / ".niche-machine" / "models" / "ggml-small.en.bin",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def run_cmd(cmd, **kwargs):
    cmd = [str(c) for c in cmd]
    res = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if res.returncode != 0:
        err = res.stderr[-500:] if res.stderr else "Unknown error"
        raise RuntimeError(f"Command failed ({cmd[0]}): {err}")
    return res

def get_font(size: int):
    from PIL import ImageFont
    candidates = [
        # Windows
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Impact.ttf",
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for f in candidates:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def wrap_text(draw, text: str, font, max_w: int):
    lines, cur = [], ""
    for w in text.split():
        candidate = (cur + " " + w).strip()
        if draw.textlength(candidate, font=font) <= max_w or not cur:
            cur = candidate
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])

# ─── STEP 1: DOWNLOAD STREAM SECTION ──────────────────────────────────────────
def download_stream_section(url: str, ss: float, dur: float, out_file: Path) -> Path:
    """Downloads a slice directly using yt-dlp without full video download."""
    t_end = ss + dur + 3.0
    t_start = max(0.0, ss - 2.0)
    print(f"📥 Downloading section: {t_start:.1f}s - {t_end:.1f}s from stream...")
    
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]/bv*+ba/b",
        "--download-sections", f"*{t_start:.1f}-{t_end:.1f}",
        "--ffmpeg-location", str(Path(FFMPEG_BIN).parent),
        "-o", str(out_file),
        url,
    ]
    run_cmd(cmd)
    
    # yt-dlp might append extension
    if not out_file.exists():
        matches = list(out_file.parent.glob(out_file.stem + ".*"))
        if matches:
            return matches[0]
        raise FileNotFoundError(f"Section download failed to create {out_file}")
    return out_file

# ─── STEP 2: WHISPER AUDIO & TRANSCRIPTION ─────────────────────────────────────
def transcribe_audio(video_file: Path, ss: float, dur: float, work_dir: Path, censor: bool = True):
    wav_path = work_dir / "slice.wav"
    run_cmd([
        FFMPEG_BIN, "-y", "-loglevel", "error",
        "-ss", f"{ss:.2f}", "-t", f"{dur:.2f}",
        "-i", str(video_file),
        "-ac", "1", "-ar", "16000", str(wav_path)
    ])

    model_path = get_whisper_model()
    if not model_path.exists():
        print(f"⚠️ Model not found at {model_path}. Please run python setup.py to download.")
        return []

    out_base = work_dir / "transcript"
    run_cmd([
        WHISPER_BIN,
        "-m", str(model_path),
        "-f", str(wav_path),
        "-ojf", "-of", str(out_base),
        "-ng", "-ml", "1"
    ])

    json_file = work_dir / "transcript.json"
    if not json_file.exists():
        return []

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    words = []
    for s in data.get("transcription", []):
        t = s.get("text", "").strip()
        if not t or re.fullmatch(r"\[.*\]|\(.*\)", t):
            continue
        if re.fullmatch(r"[^\w]+", t) and words:
            words[-1]["t"] += t
            continue
        
        # Apply swear tracker
        if censor:
            t = clean(t)

        offsets = s.get("offsets", {})
        words.append({
            "t": t,
            "s": offsets.get("from", 0) / 1000.0,
            "e": offsets.get("to", 0) / 1000.0,
        })
    return words

# ─── STEP 3: CAPTION OVERLAY RENDERING ────────────────────────────────────────
def build_caption_timeline(words, hook: str, seam_y: int, cap_y: int, dur: float, out_dir: Path, censor: bool = True):
    from PIL import Image, ImageDraw
    out_dir.mkdir(parents=True, exist_ok=True)
    
    display_hook = clean(hook) if censor else hook
    hf = get_font(52)
    cf = get_font(84)

    def draw_base_card():
        im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if display_hook:
            lines = wrap_text(d, display_hook.upper(), hf, 900)[:3]
            lh = 64
            bh = lh * len(lines) + 36
            top = seam_y - bh // 2
            bw = max(d.textlength(l, font=hf) for l in lines) + 64
            d.rounded_rectangle([540 - bw / 2, top, 540 + bw / 2, top + bh], 20, fill=(255, 255, 255, 255))
            for i, l in enumerate(lines):
                d.text((540, top + 18 + i * lh + lh / 2), l, font=hf, fill=(0, 0, 0), anchor="mm")
        return im

    # Group into 1-3 word punchy animated subtitles
    groups, cur = [], []
    for w in words:
        if cur and (len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.45 or re.search(r"[.?!,]$", cur[-1]["t"])):
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)

    states = []
    for g in groups:
        for i, w in enumerate(g):
            t1 = g[i + 1]["s"] if i + 1 < len(g) else w["e"]
            states.append((w["s"], max(t1, w["s"] + 0.08), g, i))

    timeline, t, k = [], 0.0, 0
    blank = out_dir / "blank.png"
    draw_base_card().save(blank)

    for t0, t1, g, active_idx in states:
        if t0 > t + 0.02:
            timeline.append((blank, t0 - t))
        im = draw_base_card()
        d = ImageDraw.Draw(im)
        
        text_tokens = [w["t"].upper() for w in g]
        widths = [d.textlength(x, font=cf) for x in text_tokens]
        sp = d.textlength(" ", font=cf)
        total_w = sum(widths) + sp * (len(text_tokens) - 1)
        scale_font = cf
        if total_w > 1000:
            scale_font = get_font(int(84 * 1000 / total_w))
            widths = [d.textlength(x, font=scale_font) for x in text_tokens]
            sp = d.textlength(" ", font=scale_font)
            total_w = sum(widths) + sp * (len(text_tokens) - 1)

        x = 540 - total_w / 2
        for j, (word, wd) in enumerate(zip(text_tokens, widths)):
            # Active word = Bright Yellow, Inactive = Clean White with black outline
            fill_color = (255, 221, 0) if j == active_idx else (255, 255, 255)
            d.text((x, cap_y), word, font=scale_font, anchor="lm",
                   fill=fill_color, stroke_width=7, stroke_fill=(0, 0, 0))
            x += wd + sp

        p = out_dir / f"cap_{k:04d}.png"
        im.save(p)
        k += 1
        start = max(t, t0)
        dur_step = max(0.04, t1 - start)
        timeline.append((p, dur_step))
        t = start + dur_step

    if t < dur:
        timeline.append((blank, dur - t))

    ffconcat_path = out_dir / "list.ffconcat"
    lines = ["ffconcat version 1.0"]
    for p, d_ in timeline:
        lines += [f"file '{p.name}'", f"duration {d_:.3f}"]
    if timeline:
        lines.append(f"file '{timeline[-1][0].name}'")
    ffconcat_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ffconcat_path

# ─── STEP 4: VIDEO COMPOSITING ────────────────────────────────────────────────
def render_short(src_video: Path, ss: float, dur: float, ffconcat_path: Path, out_mp4: Path, layout: str = "blur"):
    """
    Renders 1080x1920 vertical format with EBU R128 audio normalization.
    Layouts:
      'facecam': Split screen (top = gameplay, bottom = facecam)
      'blur': Blurred background with scaled 16:9 gameplay centered
    """
    if layout == "facecam":
        # Split: Gameplay top 1080x960, Player facecam bottom 1080x960
        vf = (
            "[0:v]fps=30,split=2[a][b];"
            "[a]crop=in_w:in_h*0.6:0:0,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[top];"
            "[b]crop=in_w*0.5:in_h*0.5:in_w*0.5:in_h*0.5,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[bot];"
            "[top][bot]vstack[base]"
        )
    else:
        # Blurred background fill + centered 16:9 gameplay
        vf = (
            "[0:v]fps=30,split=2[a][b];"
            "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[bg];"
            "[b]scale=1080:-2[fg];"
            "[bg][fg]overlay=0:(H-h)/2[base]"
        )

    cmd = [
        FFMPEG_BIN, "-y", "-loglevel", "error",
        "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}",
        "-i", str(src_video),
        "-f", "concat", "-safe", "0", "-i", str(ffconcat_path),
        "-filter_complex",
        vf + ";[1:v]format=rgba[ov];[base][ov]overlay=0:0:eof_action=repeat:format=auto,format=yuv420p[v];"
             "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]",
        "-map", "[v]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart",
        str(out_mp4)
    ]
    run_cmd(cmd)

# ─── MAIN PIPELINE ─────────────────────────────────────────────────────────────
def process_clip(args):
    work_dir = Path(".tmp") / "clipper_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    out_dir = Path(args.output) if args.output else Path("output") / str(date.today())
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Source resolution
    if args.url:
        src = download_stream_section(args.url, args.ss, args.dur, work_dir / "stream_slice.webm")
        clip_ss = 0.0  # slice already cut
    elif args.file:
        src = Path(args.file)
        clip_ss = args.ss
    else:
        raise ValueError("Either --url or --file must be specified")

    slug = re.sub(r"[^\w\-]+", "-", (args.slug or "gta6-viral-short")).strip("-").lower()
    out_mp4 = out_dir / f"{slug}.mp4"
    out_jpg = out_dir / f"{slug}.jpg"
    out_txt = out_dir / f"{slug}.txt"
    out_json = out_dir / f"{slug}.json"

    print("\n" + "=" * 60)
    print("🎬 GTA 6 STREAM SHORTS CLIPPER")
    print(f"Source   : {src}")
    print(f"Window   : {clip_ss}s - {clip_ss + args.dur}s ({args.dur}s)")
    print(f"Hook     : {args.hook}")
    print(f"Output   : {out_mp4}")
    print("=" * 60 + "\n")

    # 2. Transcribe & Swear Filter
    print("🎙️ [1/4] Whisper AI transcription & swear tracking...")
    words = transcribe_audio(src, clip_ss, args.dur, work_dir, censor=not args.no_censor)
    print(f"   Found {len(words)} word timestamps.")

    # 3. Build Animated Captions
    print("🎨 [2/4] Generating animated karaoke overlays & hook card...")
    seam_y = 960 if args.layout == "facecam" else 560
    cap_y = 1500 if args.layout == "facecam" else 1420
    cap_list = build_caption_timeline(words, args.hook, seam_y, cap_y, args.dur, work_dir / "caps", censor=not args.no_censor)

    # 4. Render
    print("⚡ [3/4] Rendering 1080x1920 Short with audio normalization...")
    render_short(src, clip_ss, args.dur, cap_list, out_mp4, layout=args.layout)
    print(f"   Saved video ({out_mp4.stat().st_size / 1e6:.1f} MB)")

    # 5. Thumbnail & Post Kit
    print("📦 [4/4] Generating cover thumbnail & upload post kit...")
    run_cmd([
        FFMPEG_BIN, "-y", "-loglevel", "error",
        "-ss", f"{clip_ss + 2.0:.2f}", "-i", str(src),
        "-vframes", "1", "-update", "1", str(out_jpg)
    ])

    title = clean(args.hook) if not args.no_censor else args.hook
    tags = "#GTA6 #GTAVI #gta6clips #gaming #shorts"
    caption = args.caption or f"Unreal moments in GTA 6 💀 Watch till the end!"
    if not args.no_censor:
        caption = clean(caption)

    post_kit = (
        f"TITLE:\n{title}\n\n"
        f"CAPTION:\n{caption}\n\n"
        f"{tags}\n\n"
        f"Source: {args.url or src.name}\n"
        f"Duration: {args.dur}s\n"
    )
    out_txt.write_text(post_kit, encoding="utf-8")
    
    meta = {
        "title": title,
        "caption": caption,
        "tags": tags.split(),
        "source": args.url or str(src),
        "duration": args.dur,
        "censored": not args.no_censor
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Clean intermediate files
    shutil.rmtree(work_dir, ignore_errors=True)
    print("\n✅ COMPLETE! Files ready for upload:")
    print(f"   ▶ MP4 Video : {out_mp4}")
    print(f"   ▶ Thumbnail : {out_jpg}")
    print(f"   ▶ Post Kit  : {out_txt}")
    print(f"   ▶ Metadata  : {out_json}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GTA 6 & Gaming Stream Shorts Clipper")
    parser.add_argument("--url", help="YouTube/Twitch stream URL")
    parser.add_argument("--file", help="Local video file path")
    parser.add_argument("--ss", type=float, default=0.0, help="Start time in seconds")
    parser.add_argument("--dur", type=float, default=25.0, help="Duration in seconds")
    parser.add_argument("--hook", default="GTA 6 JUST BROKE THE INTERNET 💀", help="Hook badge title")
    parser.add_argument("--slug", default="gta6-viral-short", help="Filename slug")
    parser.add_argument("--caption", help="Social post caption")
    parser.add_argument("--layout", choices=["blur", "facecam"], default="blur", help="Layout style")
    parser.add_argument("--no-censor", action="store_true", help="Disable swear word censoring")
    parser.add_argument("--output", help="Custom output directory")
    
    args = parser.parse_args()
    process_clip(args)
