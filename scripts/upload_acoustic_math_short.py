#!/usr/bin/env python3
"""
Official YouTube Shorts Uploader for Acoustic Mathematics
=========================================================
Uploads 1080x1920 (9:16) vertical Shorts to YouTube Data API v3
with #Shorts in Title/Description, Category 27 (Education), and
links to the full 10-Equation Masterclass.
"""

import os
import sys
import json
from pathlib import Path
import requests

# Ensure console supports UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "output"
DATA_DIR = ROOT_DIR / "data"

METADATA_FILE = DATA_DIR / "acoustic_short_active_metadata.json"
RECEIPT_FILE = DATA_DIR / "youtube_last_published_short.json"

def get_valid_access_token():
    env_secret = os.environ.get("YOUTUBE_CLIENT_SECRETS")
    token_data = {}
    if env_secret:
        try:
            token_data = json.loads(env_secret)
        except Exception as e:
            print(f"[!] Warning parsing YOUTUBE_CLIENT_SECRETS: {e}")
            
    if not token_data:
        token_path = ROOT_DIR / "config" / "token.json"
        if token_path.exists():
            with open(token_path, "r", encoding="utf-8") as f:
                token_data = json.load(f)
                
    refresh_token = token_data.get("refresh_token") or os.environ.get("YOUTUBE_REFRESH_TOKEN")
    client_id = token_data.get("client_id") or os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = token_data.get("client_secret") or os.environ.get("YOUTUBE_CLIENT_SECRET")
    
    if not refresh_token:
        print("[ERROR] No refresh_token found in credentials.")
        sys.exit(1)
        
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    resp = requests.post(url, data=payload, timeout=20)
    if resp.status_code == 200:
        access_token = resp.json().get("access_token")
        return access_token
    else:
        print(f"[ERROR] Failed to refresh OAuth token: {resp.status_code} - {resp.text}")
        sys.exit(1)

def upload_short(privacy_status: str = "public"):
    # Load metadata
    if not METADATA_FILE.exists():
        print(f"[ERROR] Metadata file not found at {METADATA_FILE}")
        sys.exit(1)
        
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    video_path = Path(meta.get("file", OUTPUT_DIR / "acoustic_math_short.mp4"))
    if not video_path.exists():
        video_path = OUTPUT_DIR / "acoustic_math_short.mp4"
    if not video_path.exists():
        print(f"[ERROR] Short video file not found at {video_path}")
        sys.exit(1)
        
    title = meta.get("short_title", meta.get("title", "Acoustic Math #Shorts"))
    description = meta.get("description", "Acoustic Mathematics #Shorts")
    tags = meta.get("tags", ["Shorts", "math sounds", "desmos sound"])
    
    file_size = video_path.stat().st_size
    print(f"\n================================================================================")
    print(f"PUBLISHING ACOUSTIC MATH SHORT TO YOUTUBE")
    print(f"Video File: {video_path.name} ({file_size / 1024 / 1024:.2f} MB)")
    print(f"Title: {title}")
    print(f"Privacy Status: {privacy_status}")
    print(f"Category: 27 (Education)")
    print(f"Tags Count: {len(tags)}")
    print(f"================================================================================")
    
    access_token = get_valid_access_token()
    
    # Resumable session init
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Length": str(file_size),
        "X-Upload-Content-Type": "video/mp4"
    }
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27",
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }
    
    init_resp = requests.post(init_url, headers=headers, json=body, timeout=30)
    if init_resp.status_code != 200:
        print(f"[ERROR] Failed to start resumable upload: {init_resp.status_code} - {init_resp.text}")
        sys.exit(1)
        
    upload_url = init_resp.headers.get("Location")
    if not upload_url:
        print("[ERROR] No upload Location header in response.")
        sys.exit(1)
        
    print("[+] Resumable session established. Uploading video binary data...")
    with open(video_path, "rb") as f:
        video_bytes = f.read()
        
    upload_headers = {
        "Content-Type": "video/mp4",
        "Content-Length": str(file_size)
    }
    
    up_resp = requests.put(upload_url, headers=upload_headers, data=video_bytes, timeout=120)
    if up_resp.status_code in (200, 201):
        res_data = up_resp.json()
        video_id = res_data.get("id")
        watch_url = f"https://youtube.com/shorts/{video_id}"
        print(f"\n================================================================================")
        print(f"🎉 [SUCCESS] YOUTUBE SHORT IS LIVE!")
        print(f"================================================================================")
        print(f"YouTube Video ID: {video_id}")
        print(f"Shorts URL: {watch_url}")
        print(f"Standard Watch URL: https://youtu.be/{video_id}")
        print(f"Studio Edit URL: https://studio.youtube.com/video/{video_id}/edit")
        print(f"================================================================================\n")
        
        receipt = {
            "video_id": video_id,
            "shorts_url": watch_url,
            "url": f"https://youtu.be/{video_id}",
            "title": title,
            "privacy": privacy_status,
            "file": video_path.name
        }
        with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2)
            
        return receipt
    else:
        print(f"[ERROR] Upload failed with HTTP {up_resp.status_code}: {up_resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    privacy = sys.argv[1] if len(sys.argv) > 1 else "public"
    upload_short(privacy)
