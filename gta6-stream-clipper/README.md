# Stream Shorts Clipper

An automated open-source pipeline to convert long gameplay live streams into high-retention 9:16 vertical Shorts, TikToks, and Reels.

---

## Highlights

- **Smart Video Layouts**:
  - `facecam`: Dynamic split screen with gameplay on top and streamer reaction on the bottom.
  - `blur`: Blurred background fill with full-frame gameplay centered in 9:16.
- **Whisper AI Subtitles**: Word-by-word timestamp generation for animated subtitles.
- **Dynamic Karaoke Highlighting**: Active spoken words highlighted in bright yellow with black stroke outlines.
- **Built-in Swear Filter**: Automatic tracking and censoring of profanities across subtitles, hook badges, and post descriptions using `*`.
- **EBU R128 Audio Normalization**: Automatic `loudnorm` filter balancing audio levels for social feed playback.
- **Complete Post Kits**: Automatically generates the vertical MP4 video, cover thumbnail image, social caption text file, and JSON metadata.

---

## Architecture Overview

```
                      Stream URL / Video File
                                |
                   [yt-dlp Section Extractor]
                                |
             +------------------+------------------+
             |                                     |
       [Audio Track]                         [Video Track]
             |                                     |
    [Whisper AI Engine]                     [Layout Mode]
             |                              /           \
  [Word Timestamps & Tokens]       [Blur Vertical]  [Split Facecam]
             |                               \         /
   [Profanity Filter (*)]                     [Base Canvas]
             |                                     |
 [Karaoke PNG Frame Generator]                     |
             |                                     |
             +------------------+------------------+
                                |
                    [FFmpeg Filter Complex]
                                |
                    +-----------+-----------+
                    |                       |
               [Video MP4]             [Cover JPG]
               [Post TXT]              [Meta JSON]
```

---

## Quickstart

### 1. Requirements

- Python 3.10+
- FFmpeg installed and available on system PATH
- Git

### 2. Installation

Clone this repository and run the setup script:

```bash
git clone https://github.com/vanz-0/gta6-stream-clipper.git
cd gta6-stream-clipper
python setup.py
```

The setup script automatically installs necessary Python packages and configures the Whisper speech model.

---

## Usage

### Clip Directly from a Stream URL

```bash
python clipper.py --url "https://www.youtube.com/watch?v=EXAMPLE" --ss 30 --dur 25 --hook "UNREAL MOMENT"
```

### Clip from a Local File

```bash
python clipper.py --file "gameplay.mp4" --ss 60 --dur 30 --layout blur --hook "HE COULD NOT BELIEVE THIS"
```

### Split-Screen Facecam Mode

```bash
python clipper.py --file "stream.mp4" --ss 120 --dur 35 --layout facecam --hook "INSANE REACTION"
```

---

## Command Line Arguments

| Flag | Type | Default | Description |
|---|---|---|---|
| `--url` | string | `None` | YouTube or Twitch video URL |
| `--file` | string | `None` | Local video file path |
| `--ss` | float | `0.0` | Start offset time in seconds |
| `--dur` | float | `25.0` | Duration of the clip in seconds |
| `--hook` | string | `"VIRAL MOMENT"` | Hook title displayed on badge |
| `--layout` | string | `blur` | Layout mode: `blur` or `facecam` |
| `--no-censor` | flag | `False` | Disable automatic profanity censoring |
| `--output` | string | `output/` | Destination folder for export files |

---

## YouTube Description Snippet

If you share this workflow with your audience, you can paste this into your video description:

```text
Download the free open-source Stream Clipper tool here:
https://github.com/vanz-0/gta6-stream-clipper

Features:
- Automated 9:16 Shorts converter
- Split screen facecam + gameplay
- AI word-by-word karaoke subtitles
- Built-in swear filter and audio normalization
```

---

## License

This project is licensed under the MIT License.
