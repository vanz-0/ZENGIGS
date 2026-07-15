"""
Retry uploading oversized videos using Supabase's TUS resumable upload protocol.
This bypasses the 50MB standard upload limit by uploading in 6MB chunks.
"""
import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
BUCKET_NAME = "videos"
VIDEOS_DIR = Path(__file__).parent.parent / "zen-portfolio" / "public" / "videos"
CHUNK_SIZE = 6 * 1024 * 1024  # 6MB chunks

FAILED_FILES = [
    "ECS_010.mp4", "ECS_013.mp4", "ECS_014.mp4", "ECS_017.mp4",
    "ECS_018.mp4", "ECS_021.mp4", "ECS_024.mp4", "ECS_025.mp4",
]

def b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

def resumable_upload(filepath: Path) -> bool:
    filename = filepath.name
    file_size = filepath.stat().st_size
    size_mb = file_size / (1024 * 1024)

    print(f"  Uploading {filename} ({size_mb:.1f} MB) via resumable upload...")

    # Step 1: Create the upload
    create_url = f"{SUPABASE_URL}/storage/v1/upload/resumable"
    metadata = f"bucketName {b64(BUCKET_NAME)},objectName {b64(filename)},contentType {b64('video/mp4')}"

    create_headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "apikey": SUPABASE_SERVICE_KEY,
        "tus-resumable": "1.0.0",
        "upload-length": str(file_size),
        "upload-metadata": metadata,
        "x-upsert": "true",
    }

    resp = requests.post(create_url, headers=create_headers)
    if resp.status_code not in (200, 201):
        print(f"    FAILED to create upload: {resp.status_code} {resp.text[:200]}")
        return False

    upload_url = resp.headers.get("Location")
    if not upload_url:
        print(f"    FAILED: No Location header returned")
        return False

    # Step 2: Upload in chunks
    offset = 0
    with open(filepath, "rb") as f:
        while offset < file_size:
            chunk = f.read(CHUNK_SIZE)
            chunk_len = len(chunk)

            patch_headers = {
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "apikey": SUPABASE_SERVICE_KEY,
                "tus-resumable": "1.0.0",
                "upload-offset": str(offset),
                "content-type": "application/offset+octet-stream",
            }

            patch_resp = requests.patch(upload_url, data=chunk, headers=patch_headers)

            if patch_resp.status_code not in (200, 204):
                print(f"    FAILED at offset {offset}: {patch_resp.status_code} {patch_resp.text[:200]}")
                return False

            offset += chunk_len
            pct = (offset / file_size) * 100
            print(f"    Progress: {pct:.0f}% ({offset / (1024*1024):.1f} / {size_mb:.1f} MB)", flush=True)

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
    print(f"    OK -> {public_url}")
    return True

def main():
    print("=" * 60)
    print("ZENGIGS — Resumable Video Upload (Retry)")
    print("=" * 60)

    success = 0
    failed = 0

    for i, filename in enumerate(FAILED_FILES, 1):
        filepath = VIDEOS_DIR / filename
        print(f"\n[{i}/{len(FAILED_FILES)}]", flush=True)
        if resumable_upload(filepath):
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Done! {success} uploaded, {failed} failed.")
    print("=" * 60)

if __name__ == "__main__":
    main()
