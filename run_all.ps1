# Run the entire ZENGIGS video processing pipeline

$ErrorActionPreference = "Stop"

Write-Host "Step 1: Splitting videos into clips..."
python execution/split_by_keyword.py "portfolio/clips" "raw/Untitled Video_1080p.mp4" "raw/Evans_Clones.mp4"

Write-Host "Step 2: Applying TikTok Captions and Action Graphics..."
python execution/full_pipeline.py "portfolio/clips" "done_videos"

Write-Host "All processing complete! Check the 'done_videos' folder."
