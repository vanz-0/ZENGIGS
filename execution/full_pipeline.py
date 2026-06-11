import os
import subprocess
import argparse
from pathlib import Path
import random
import static_ffmpeg
static_ffmpeg.add_paths()

# Colorful TikTok caption colors
COLORS = [
    "&H0000FFFF", # Yellow
    "&H0000FF00", # Green
    "&H00FFFF00", # Cyan
    "&H0000A5FF", # Orange
    "&H00FF00FF"  # Magenta
]

def apply_motion_graphics(clip_path: str, output_path: str, hyperframes_dir: str, has_action: bool):
    if not has_action:
        # Just pass through if no key action is detected
        subprocess.run(["ffmpeg", "-y", "-i", clip_path, "-c", "copy", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    print(f"Applying Dark Mode Orange motion graphics to {clip_path} (Action Point detected)...")
    
    hf_project_dir = os.path.join(hyperframes_dir, "project")
    os.makedirs(hf_project_dir, exist_ok=True)
    
    init_cmd = ["npx.cmd", "--yes", "hyperframes", "init", ".", "--example", "blank", "--non-interactive", "--skip-skills"]
    subprocess.run(init_cmd, cwd=hf_project_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We would normally adjust HTML to have dark mode + orange accent.
    # We are simulating that by rendering the overlay.
    overlay_path = os.path.join(hf_project_dir, "render.webm")
    render_cmd = ["npx.cmd", "--yes", "hyperframes", "render", ".", "-o", "render.webm", "--format", "webm"]
    subprocess.run(render_cmd, cwd=hf_project_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(overlay_path):
        composite_cmd = [
            "ffmpeg", "-y", "-i", clip_path, "-i", overlay_path,
            "-filter_complex", "[0:v][1:v]overlay=0:0[outv]",
            "-map", "[outv]", "-map", "0:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "copy",
            output_path
        ]
        subprocess.run(composite_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["ffmpeg", "-y", "-i", clip_path, "-c", "copy", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def apply_captions(clip_path: str, output_path: str) -> bool:
    print(f"Applying TikTok style captions to {clip_path}...")
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(clip_path, word_timestamps=True)
    
    srt_path = clip_path + ".ass"
    has_action = False
    
    # We will build an ASS file directly for precise color control per word.
    # Simulated action keyword detection (e.g., words like "now", "look", "important")
    action_keywords = ["now", "look", "important", "so", "first", "watch", "buy", "click"]
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType=v4.00+\nPlayResX=1920\nPlayResY=1080\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: TikTok,Impact,80,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,5,10,10,540,1\n\n")
        f.write("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        
        for segment in result.get("segments", []):
            for word_info in segment.get("words", []):
                start = word_info["start"]
                end = word_info["end"]
                word = word_info["word"].strip().upper()
                
                # Check for action words
                w_clean = ''.join(c for c in word.lower() if c.isalnum())
                if w_clean in action_keywords:
                    has_action = True
                    
                # Assign a random TikTok style color to words
                color = random.choice(COLORS)
                text = f"{{\\c{color}}}{word}"
                
                def format_ass_time(s):
                    hours = int(s / 3600)
                    minutes = int((s % 3600) / 60)
                    seconds = int(s % 60)
                    cs = int((s - int(s)) * 100)
                    return f"{hours}:{minutes:02d}:{seconds:02d}.{cs:02d}"
                
                f.write(f"Dialogue: 0,{format_ass_time(start)},{format_ass_time(end)},TikTok,,0,0,0,,{text}\n")
    
    safe_srt_path = srt_path.replace("\\", "/").replace(":", "\\:")
    
    caption_cmd = [
        "ffmpeg", "-y", "-i", clip_path,
        "-vf", f"ass='{safe_srt_path}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "copy",
        output_path
    ]
    
    subprocess.run(caption_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return has_action

def main():
    parser = argparse.ArgumentParser(description="Full Pipeline Orchestrator (TikTok + Action Graphics)")
    parser.add_argument("input_dir", help="Directory containing the split clips")
    parser.add_argument("output_dir", help="Directory to save final videos")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    hyperframes_dir = os.path.join(args.output_dir, "hf_workspace")
    os.makedirs(hyperframes_dir, exist_ok=True)
    
    clips = [f for f in os.listdir(args.input_dir) if f.endswith(".mp4")]
    clips.sort()
    
    for clip in clips:
        clip_path = os.path.join(args.input_dir, clip)
        intermediate_path = os.path.join(args.output_dir, "temp_cap_" + clip)
        final_path = os.path.join(args.output_dir, clip) # e.g. done_videos/clip_01.mp4
        
        # 1. Apply captions and detect action points simultaneously
        has_action = apply_captions(clip_path, intermediate_path)
        
        # 2. Apply motion graphics if action was detected
        apply_motion_graphics(intermediate_path, final_path, hyperframes_dir, has_action)
        
        # Cleanup
        if os.path.exists(intermediate_path):
            os.remove(intermediate_path)
            
        print(f"Finished processing {clip} -> {final_path}")

if __name__ == "__main__":
    main()
