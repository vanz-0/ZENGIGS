"""
Upload all videos from public/videos/ to Supabase Storage.
Creates a public 'videos' bucket and uploads each MP4 file.
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
BUCKET_NAME = "videos"
VIDEOS_DIR = Path(__file__).parent.parent / "zen-portfolio" / "public" / "videos"

headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
}

def create_bucket():
    """Create a public 'videos' bucket if it doesn't exist."""
    url = f"{SUPABASE_URL}/storage/v1/bucket"
    payload = {
        "id": BUCKET_NAME,
        "name": BUCKET_NAME,
        "public": True,
        "allowed_mime_types": ["video/mp4"],
        "file_size_limit": 104857600,  # 100MB
    }
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        print(f"[OK] Created bucket '{BUCKET_NAME}'")
    elif "already exists" in resp.text.lower() or resp.status_code == 409:
        print(f"[OK] Bucket '{BUCKET_NAME}' already exists")
    else:
        print(f"[WARN] Bucket creation response: {resp.status_code} {resp.text}")

def upload_video(filepath: Path):
    """Upload a single video file to the bucket."""
    filename = filepath.name
    size_mb = filepath.stat().st_size / (1024 * 1024)
    
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
    
    upload_headers = {
        **headers,
        "Content-Type": "video/mp4",
        "x-upsert": "true",  # overwrite if exists
    }
    
    print(f"  Uploading {filename} ({size_mb:.1f} MB)...", end=" ", flush=True)
    
    with open(filepath, "rb") as f:
        resp = requests.post(url, data=f, headers=upload_headers)
    
    if resp.status_code in (200, 201):
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
        print(f"OK -> {public_url}")
        return True
    else:
        print(f"FAILED ({resp.status_code}: {resp.text[:200]})")
        return False

def main():
    print("=" * 60)
    print("ZENGIGS — Supabase Video Upload")
    print("=" * 60)
    print(f"Source: {VIDEOS_DIR}")
    print(f"Target: {SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/")
    print()
    
    # 1. Create bucket
    create_bucket()
    print()
    
    # 2. Find all MP4 files
    mp4_files = sorted(VIDEOS_DIR.glob("*.mp4"))
    print(f"Found {len(mp4_files)} MP4 files to upload.\n")
    
    # 3. Upload each one
    success = 0
    failed = 0
    for i, mp4 in enumerate(mp4_files, 1):
        print(f"[{i}/{len(mp4_files)}]", end=" ")
        if upload_video(mp4):
            success += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Done! {success} uploaded, {failed} failed.")
    print("=" * 60)

if __name__ == "__main__":
    main()
