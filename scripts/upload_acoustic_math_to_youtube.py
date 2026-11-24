#!/usr/bin/env python3
"""
Official YouTube Data API v3 Uploader for Acoustic Mathematics
==============================================================
Publishes 1080p Masterclass videos with 100% SEO-optimized Metadata
(Title, Dynamic Chapter Timestamps, High-Intent Search Tags, Category 27).
"""

import os
import sys
import glob
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

TITLE = "What 10 Iconic Math Equations Actually Sound Like (Desmos Sonification)"

TAGS = [
    "math sounds",
    "desmos sound",
    "what math sounds like",
    "equation sonification",
    "acoustic mathematics",
    "cursed desmos",
    "riemann hypothesis sound",
    "fourier transform audio",
    "audio trace desmos",
    "math visualizer",
    "sine wave sound",
    "stem education",
    "calculus animations",
    "frequency modulation math",
    "educational documentary",
    "math songs",
    "desmos cursed"
]

def build_dynamic_description() -> str:
    chapters_file = DATA_DIR / "masterclass_chapters.json"
    chapters_lines = []
    
    if chapters_file.exists():
        try:
            with open(chapters_file, "r", encoding="utf-8") as f:
                chapters = json.load(f)
                for ch in chapters:
                    chapters_lines.append(f"{ch['timestamp']} - {ch['title']}")
        except Exception as e:
            print(f"[!] Warning reading chapters: {e}")
            
    if not chapters_lines:
        chapters_lines = [
            "00:00 - 1. Pure Harmonic Oscillation: y = sin(x)",
            "00:50 - 2. The Cursed Curve: y = x^x",
            "01:40 - 3. The Quadratic Laser Chirp: y = sin(x^2)",
            "02:30 - 4. The Infinite Barrier: y = tan(x)",
            "03:20 - 5. The Cardinal Sinc Wave: y = sin(x)/x",
            "04:10 - 6. Topologist's Infinite Sine: y = sin(1/x)",
            "05:00 - 7. Riemann Zeta Critical Zeros: Re(s) = 1/2",
            "05:50 - 8. The Razor Curve: y = tan(sin(x))",
            "06:40 - 9. The Golden Logarithmic Spiral: r = e^(0.15*theta)",
            "07:30 - 10. Fourier Square Wave Synthesis (7 Harmonics)",
            "08:20 - Conclusion & Desmos Accessibility for Blind Mathematicians"
        ]
        
    chapters_block = "\n".join(chapters_lines)
    
    desc = f"""Have you ever wondered what mathematical equations sound like when converted into acoustic sound? In this visual and acoustic mathematics masterclass, we sonify 10 iconic equations—from the pure harmonic baseline to the cursed exponential x^x curve and the million-dollar non-trivial zeros of the Riemann Zeta hypothesis.

Using the sonification standard utilized by Desmos and screen-reader accessibility software for visually impaired and blind mathematicians, each equation's x-coordinate glides across time and stereo space (Left to Right ear), while vertical y-values map continuously to audio pitch frequencies.

🎧 Headphone Recommended for Full Stereo Audio Panning.

⏱️ Chapter Timestamps:
{chapters_block}

👉 Download Formula Sheets & Interactive Desmos Guides:
https://eduprosuite.pro/

#Mathematics #Desmos #AcousticMath #Calculus #STEM #Science #MathVisualizer #AudioTrace #MathSounds"""
    return desc

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
                
    if not token_data:
        print("[ERROR] Neither YOUTUBE_CLIENT_SECRETS env nor config/token.json found.")
        sys.exit(1)
        
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
    if resp.status_code != 200:
        print(f"[ERROR] Failed to refresh OAuth token: {resp.status_code} - {resp.text}")
        sys.exit(1)
        
    return resp.json().get("access_token")

def upload_video(privacy_status="public"):
    # Find generated MP4 in output/
    video_files = sorted(list(OUTPUT_DIR.glob("*.mp4")), key=lambda p: p.stat().st_mtime, reverse=True)
    if not video_files:
        print(f"[ERROR] No rendered video found in {OUTPUT_DIR}")
        sys.exit(1)
        
    target_video = video_files[0]
    file_size = target_video.stat().st_size
    description = build_dynamic_description()
    
    print("=" * 80)
    print("PUBLISHING ACOUSTIC MATHEMATICS MASTERCLASS TO YOUTUBE")
    print(f"Video File: {target_video.name} ({file_size / (1024 * 1024):.2f} MB)")
    print(f"Title: {TITLE}")
    print(f"Privacy Status: {privacy_status}")
    print(f"Category: 27 (Education)")
    print(f"Tags Count: {len(TAGS)}")
    print("=" * 80)
    
    access_token = get_valid_access_token()
    
    # 1. Initiate Resumable Upload
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(file_size)
    }
    
    body = {
        "snippet": {
            "title": TITLE,
            "description": description,
            "tags": TAGS,
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }
    
    init_resp = requests.post(init_url, json=body, headers=headers, timeout=30)
    if init_resp.status_code != 200:
        print(f"[ERROR] Failed to initiate upload: {init_resp.status_code} - {init_resp.text}")
        sys.exit(1)
        
    upload_url = init_resp.headers.get("Location")
    if not upload_url:
        print("[ERROR] No upload Location header returned by YouTube.")
        sys.exit(1)
        
    print("[+] Resumable session established. Uploading video binary data...")
    
    # 2. Upload Video Binary
    with open(target_video, "rb") as vf:
        video_data = vf.read()
        
    upload_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "video/mp4",
        "Content-Length": str(file_size)
    }
    
    upload_resp = requests.put(upload_url, data=video_data, headers=upload_headers, timeout=180)
    if upload_resp.status_code in [200, 201]:
        res_data = upload_resp.json()
        video_id = res_data.get("id")
        print("\n" + "=" * 80)
        print("🎉 [SUCCESS] 1080P MASTERCLASS IS LIVE ON YOUTUBE!")
        print("=" * 80)
        print(f"YouTube Video ID: {video_id}")
        print(f"Watch URL: https://youtu.be/{video_id}")
        print(f"Studio Edit URL: https://studio.youtube.com/video/{video_id}/edit")
        print("=" * 80 + "\n")
        
        # Save upload receipt to data/
        receipt_path = ROOT_DIR / "data" / "youtube_last_published_masterclass.json"
        with open(receipt_path, "w", encoding="utf-8") as rf:
            json.dump({
                "video_id": video_id,
                "url": f"https://youtu.be/{video_id}",
                "title": TITLE,
                "privacy": privacy_status,
                "file": target_video.name
            }, rf, indent=2)
            
        return video_id
    else:
        print(f"[ERROR] Failed to upload video binary: {upload_resp.status_code} - {upload_resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    privacy = "public"
    if len(sys.argv) > 1:
        privacy = sys.argv[1]
    upload_video(privacy_status=privacy)
