import argparse
import subprocess
import os
import static_ffmpeg
static_ffmpeg.add_paths()

def extract_audio(input_path: str, output_path: str):
    print(f"Extracting audio from {input_path} to {output_path}...")
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Audio extraction complete.")

def get_split_timestamps(audio_path: str) -> list[float]:
    import whisper
    print("Loading Whisper large model for maximum accuracy...")
    model = whisper.load_model("large")
    print("Transcribing audio to find 'thank you' timestamps...")
    result = model.transcribe(audio_path, word_timestamps=True, language="en")
    
    split_points = []
    all_words = []
    
    # Flatten all words across all segments
    for segment in result.get("segments", []):
        for word_info in segment.get("words", []):
            clean = ''.join(c for c in word_info["word"].strip().lower() if c.isalnum())
            all_words.append({"word": clean, "start": word_info["start"], "end": word_info["end"]})
    
    # Print full transcript for debugging
    full_text = " ".join(w["word"] for w in all_words)
    print(f"Full transcript preview: {full_text[:500]}...")
    
    # Match consecutive 'thank you' pairs with fuzzy support
    # Also catches single-word 'thanks' as a boundary
    THANK_VARIANTS = {"thank", "thanks", "thankyou", "thanku", "thnak", "thnk"}
    YOU_VARIANTS = {"you", "u", "ya", "yah"}
    
    i = 0
    while i < len(all_words):
        w = all_words[i]["word"]
        
        # Single word 'thanks' as complete phrase
        if w in THANK_VARIANTS and w not in {"thank"}:
            split_points.append(all_words[i]["end"])
            print(f"  -> Split at {all_words[i]['end']:.2f}s: '{w}'")
            i += 1
            continue
        
        # Two-word 'thank you'
        if w in THANK_VARIANTS and i + 1 < len(all_words):
            w2 = all_words[i+1]["word"]
            if w2 in YOU_VARIANTS:
                split_points.append(all_words[i+1]["end"])
                print(f"  -> Split at {all_words[i+1]['end']:.2f}s: '{w} {w2}'")
                i += 2
                continue
        i += 1
    
    print(f"Found {len(split_points)} split points: {[round(p, 2) for p in split_points]}")
    return split_points

def split_video(input_path: str, output_dir: str, split_points: list[float], starting_index: int):
    os.makedirs(output_dir, exist_ok=True)
    
    points = [0.0] + split_points
    
    # ffprobe to get duration so we know when the last clip ends
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_path]
    dur_res = subprocess.run(dur_cmd, capture_output=True, text=True)
    duration = float(dur_res.stdout.strip())
    points.append(duration)
    
    clips_generated = 0
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i+1]
        out_name = os.path.join(output_dir, f"clip_{starting_index + i:02d}.mp4")
        
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-ss", str(start), "-t", str(end - start),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            out_name
        ]
        
        print(f"Exporting {out_name} (start: {start:.2f}, end: {end:.2f})...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips_generated += 1
        
    print(f"Successfully created {clips_generated} clips in {output_dir}")
    return starting_index + clips_generated

def process_videos(video_paths: list[str], output_dir: str):
    clip_index = 1
    for i, vid in enumerate(video_paths):
        print(f"\n--- Processing Video {i+1}: {vid} ---")
        audio_temp = f"temp_audio_{i}.wav"
        try:
            extract_audio(vid, audio_temp)
            split_points = get_split_timestamps(audio_temp)
            if not split_points:
                print("No 'thank you' found in the video. Splitting whole video as one clip.")
            
            clip_index = split_video(vid, output_dir, split_points, clip_index)
        finally:
            if os.path.exists(audio_temp):
                os.remove(audio_temp)

def main():
    parser = argparse.ArgumentParser(description="Split multiple videos by 'thank you'")
    parser.add_argument("output_dir", help="Directory to save clips")
    parser.add_argument("videos", nargs="+", help="Paths to input videos")
    args = parser.parse_args()
    
    process_videos(args.videos, args.output_dir)

if __name__ == "__main__":
    main()
