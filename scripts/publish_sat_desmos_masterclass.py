#!/usr/bin/env python3
"""
Digital SAT Math Desmos 30-Minute Masterclass - YouTube Publishing Engine
Uploads the masterclass MP4 video to YouTube Data API v3 with complete SEO metadata,
chapter timestamps, tags, and EduProSuite study resource links.
"""

import os
import sys
import json
import argparse
import requests
from dotenv import dotenv_values

CURRICULUM_PATH = os.path.join("data", "sat_desmos_masterclass_curriculum.json")
DEFAULT_VIDEO_PATH = os.path.join("output", "sat_desmos_masterclass_30min.mp4")

TITLE = "The Ultimate Digital SAT Math Desmos Guide 2025/2026 (Score 800 with 10-Second Hacks)"

def build_description(curriculum_data):
    """Generate high-retention, SEO-optimized YouTube description with chapter timestamps."""
    chapters = []
    for mod in curriculum_data.get("modules", []):
        chapters.append(f"{mod['timestamp']} - Module {mod['module_id']}: {mod['title']}")
    
    chapters_text = "\n".join(chapters)
    
    desc = (
        "The Only Digital SAT Math Desmos Guide you'll ever need for 2025/2026. "
        "Learn the 10 most powerful Desmos cheat codes to solve College Board SAT math questions "
        "in 10 to 15 seconds without doing manual algebra or memorizing formulas!\n\n"
        "⏱️ MASTERCLASS CHAPTER TIMESTAMPS:\n"
        f"{chapters_text}\n\n"
        "🎯 WHAT THIS MASTERCLASS COVERS:\n"
        "• 5-Second System of Linear Equations Intersection Trick\n"
        "• Instant Quadratic Roots, Min/Max & Vertex Finding\n"
        "• The Secret Regression Cheat Code (y1 ~ ax1^2 + bx1 + c)\n"
        "• Visual Constant k (Infinite Solutions & No Solution)\n"
        "• Circle Equations & Radii without completing the square\n"
        "• Systems of Inequalities & Shaded Feasible Regions\n"
        "• Nested Function Transformations f(x) vs Tables\n"
        "• Exponential Multipliers & Percentage Growth\n"
        "• 3-Click Summary Statistics (Mean, Median, IQR, Box Plots)\n"
        "• Hard Geometry & Triangle Trigonometry on Desmos\n\n"
        "📥 DOWNLOAD FREE DIGITAL SAT DESMOS CHEAT SHEET & 500+ MCQs:\n"
        "https://eduprosuite.pro/sat-math-desmos-cheatsheet.html\n\n"
        "🔔 Subscribe to I am a Proffesor for weekly high-yield STEM & Exam Masterclasses!\n\n"
        "#DigitalSAT #SATMath #Desmos #SAT2025 #SAT2026 #SATPrep #CollegeBoard #DesmosTricks #MathHacks #HighSchoolMath"
    )
    return desc

TAGS = [
    "digital sat math",
    "sat desmos guide",
    "sat math tricks",
    "desmos graphing calculator sat",
    "digital sat 2025",
    "digital sat 2026",
    "how to use desmos on sat",
    "sat math shortcuts",
    "sat 800 math",
    "learnsatmath desmos",
    "college board digital sat",
    "sat desmos regression",
    "sat math tips"
]

def get_access_token():
    """Retrieve access token from environment or .env file."""
    env = dotenv_values(".env") if os.path.exists(".env") else {}
    
    client_id = None
    client_secret = None
    refresh_token = None

    env_secret = os.environ.get("YOUTUBE_CLIENT_SECRETS")
    if env_secret:
        try:
            tdata = json.loads(env_secret)
            client_id = tdata.get("client_id")
            client_secret = tdata.get("client_secret")
            refresh_token = tdata.get("refresh_token")
        except Exception as e:
            print(f"[!] Warning: Failed to parse YOUTUBE_CLIENT_SECRETS: {e}")

    if not client_id:
        client_id = os.environ.get("YOUTUBE_CLIENT_ID") or env.get("YOUTUBE_CLIENT_ID")
    if not client_secret:
        client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET") or env.get("YOUTUBE_CLIENT_SECRET")
    if not refresh_token:
        refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN") or env.get("YOUTUBE_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        # Check token.json fallback
        token_path = os.path.join("config", "token.json")
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                tdata = json.load(f)
                client_id = tdata.get("client_id")
                client_secret = tdata.get("client_secret")
                refresh_token = tdata.get("refresh_token")

    if not client_id or not client_secret or not refresh_token:
        raise ValueError("Missing YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, or YOUTUBE_REFRESH_TOKEN.")

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    resp = requests.post(token_url, data=payload, timeout=15)
    if resp.status_code == 200:
        return resp.json().get("access_token")
    else:
        raise RuntimeError(f"OAuth token refresh failed: {resp.status_code} - {resp.text}")

def upload_video(video_path, privacy_status="public", dry_run=False):
    """Execute resumable upload of video to YouTube Data API v3."""
    if not os.path.exists(CURRICULUM_PATH):
        raise FileNotFoundError(f"Curriculum not found at {CURRICULUM_PATH}")

    with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
        curriculum_data = json.load(f)

    description = build_description(curriculum_data)

    print("=" * 65)
    print("DIGITAL SAT DESMOS MASTERCLASS - YOUTUBE PUBLISHER")
    print("=" * 65)
    print(f"Title:          {TITLE}")
    print(f"Privacy Status: {privacy_status}")
    print(f"Video File:     {video_path}")
    print(f"Chapters Count: {len(curriculum_data.get('modules', []))} modules")
    print("=" * 65)

    if dry_run:
        print("[DRY RUN] Validating YouTube OAuth credentials...")
        token = get_access_token()
        # Verify channel name
        ch_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if ch_resp.status_code == 200:
            items = ch_resp.json().get("items", [])
            ch_title = items[0]["snippet"]["title"] if items else "Unknown"
            print(f"[DRY RUN] Verified Channel: '{ch_title}'")
            print("[DRY RUN] Authentication successful! Skipping actual video upload.")
            return True
        else:
            raise RuntimeError(f"Channel inspection failed: {ch_resp.status_code} - {ch_resp.text}")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file does not exist at {video_path}")

    file_size = os.path.getsize(video_path)
    print(f"Video File Size: {file_size / (1024*1024):.2f} MB")

    token = get_access_token()

    # 1. Initiate Resumable Upload
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    headers = {
        "Authorization": f"Bearer {token}",
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

    print("Initiating resumable upload session with YouTube Data API...")
    init_resp = requests.post(init_url, json=body, headers=headers, timeout=25)
    if init_resp.status_code != 200:
        raise RuntimeError(f"Failed to initiate upload: {init_resp.status_code} - {init_resp.text}")

    upload_url = init_resp.headers.get("Location")
    if not upload_url:
        raise RuntimeError("No upload URL returned by YouTube.")

    # 2. Upload Video Bytes
    print("Uploading video stream...")
    with open(video_path, "rb") as vf:
        up_headers = {
            "Content-Length": str(file_size),
            "Content-Type": "video/mp4"
        }
        up_resp = requests.put(upload_url, data=vf, headers=up_headers, timeout=600)

    if up_resp.status_code in [200, 201]:
        vid_data = up_resp.json()
        video_id = vid_data.get("id")
        live_url = f"https://www.youtube.com/watch?v={video_id}"
        print("=" * 65)
        print("🎉 SUCCESS! Video published to YouTube!")
        print(f"Video ID:  {video_id}")
        print(f"Live URL:  {live_url}")
        print("=" * 65)
        return video_id
    else:
        raise RuntimeError(f"Video stream upload failed: {up_resp.status_code} - {up_resp.text}")

def main():
    parser = argparse.ArgumentParser(description="Publish SAT Desmos Masterclass to YouTube")
    parser.add_argument("--video-path", default=DEFAULT_VIDEO_PATH, help="Path to compiled MP4 video")
    parser.add_argument("--privacy-status", default="public", choices=["public", "unlisted", "private"], help="YouTube visibility")
    parser.add_argument("--dry-run", action="store_true", help="Validate credentials and description without uploading")
    args = parser.parse_args()

    upload_video(video_path=args.video_path, privacy_status=args.privacy_status, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
