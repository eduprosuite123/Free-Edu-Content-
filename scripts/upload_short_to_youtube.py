"""
EduProSuite YouTube Shorts Uploader
===================================
Uploads a local MP4 vertical video to YouTube Data API v3 using
the stored OAuth 2.0 refresh token.
"""

import os
import sys
import json
import requests

# Ensure console supports UTF-8 on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "token.json")
VIDEO_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "eduprosuite_ap_short.mp4")

# విధానం 1: Auto-Suggestions + OCR + Optimized Description (Clean title <= 60 chars, 3-5 tags)
TITLE = "AP Statistics Type I vs Type II Errors in 30s"
DESCRIPTION = (
    "Master Type 1 and Type 2 error phrasing for AP Statistics. Solve hypothesis testing FRQ questions without getting tricked.\n\n"
    "👉 Download Full AP Stats Formula Sheet & MCQs:\n"
    "https://eduprosuite.pro/ap-stats-formula-sheet.html\n\n"
    "#Shorts #APStatistics #APStats #ExamPrep"
)
TAGS = ["Shorts", "AP Statistics", "AP Stats", "Exam Prep"]

def get_valid_access_token():
    env_secret = os.environ.get("YOUTUBE_CLIENT_SECRETS")
    token_data = {}
    if env_secret:
        try:
            token_data = json.loads(env_secret)
        except Exception as e:
            print(f"[!] Warning: Failed to parse YOUTUBE_CLIENT_SECRETS JSON: {e}")
            
    if not token_data and os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as f:
            token_data = json.load(f)
            
    if not token_data:
        print(f"Error: Neither YOUTUBE_CLIENT_SECRETS env nor {TOKEN_PATH} found.")
        sys.exit(1)
        
    refresh_token = token_data.get("refresh_token")
    client_id = token_data.get("client_id")
    client_secret = token_data.get("client_secret")
    
    if not refresh_token:
        print("Error: No refresh_token found in credentials.")
        sys.exit(1)
        
    # Refresh to get a fresh access token
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    resp = requests.post(url, data=payload, timeout=15)
    if resp.status_code == 200:
        access_token = resp.json().get("access_token")
        return access_token
    else:
        print(f"Error refreshing access token: {resp.status_code} - {resp.text}")
        sys.exit(1)

def upload_short(privacy_status="public"):
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Video file not found at {VIDEO_PATH}")
        sys.exit(1)
        
    access_token = get_valid_access_token()
    file_size = os.path.getsize(VIDEO_PATH)
    
    print("\n" + "=" * 60)
    print("Uploading EduProSuite Short to YouTube...")
    print(f"Video File: {VIDEO_PATH} ({file_size / 1024:.1f} KB)")
    print(f"Title: {TITLE}")
    print(f"Status: {privacy_status}")
    print("=" * 60)
    
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
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }
    
    init_resp = requests.post(init_url, json=body, headers=headers, timeout=20)
    if init_resp.status_code != 200:
        print(f"Failed to initiate upload: {init_resp.status_code} - {init_resp.text}")
        sys.exit(1)
        
    upload_url = init_resp.headers.get("Location")
    if not upload_url:
        print("Error: No upload location returned by YouTube.")
        sys.exit(1)
        
    print("[+] Resumable session created. Uploading video data...")
    
    # 2. Upload Video Binary
    with open(VIDEO_PATH, "rb") as vf:
        video_data = vf.read()
        
    upload_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "video/mp4",
        "Content-Length": str(file_size)
    }
    
    upload_resp = requests.put(upload_url, data=video_data, headers=upload_headers, timeout=60)
    if upload_resp.status_code in [200, 201]:
        res_data = upload_resp.json()
        video_id = res_data.get("id")
        print("\n" + "=" * 60)
        print("[+] SUCCESS! EduProSuite Short is LIVE on YouTube!")
        print("=" * 60)
        print(f"YouTube Video ID: {video_id}")
        print(f"Watch Short URL: https://youtube.com/shorts/{video_id}")
        print(f"Standard URL: https://youtu.be/{video_id}")
        print("=" * 60 + "\n")
        return video_id
    else:
        print(f"Failed to upload video: {upload_resp.status_code} - {upload_resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    privacy = "public"
    if len(sys.argv) > 1:
        privacy = sys.argv[1]
    upload_short(privacy_status=privacy)
