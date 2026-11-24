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

token_path = os.path.join(os.path.dirname(__file__), "..", "config", "token.json")
env_secret = os.environ.get("YOUTUBE_CLIENT_SECRETS")
t = {}
if env_secret:
    try:
        t = json.loads(env_secret)
    except Exception as e:
        print(f"[!] Warning parsing YOUTUBE_CLIENT_SECRETS: {e}")

if not t and os.path.exists(token_path):
    with open(token_path, "r", encoding="utf-8") as f:
        t = json.load(f)

if not t:
    print(f"[!] Warning: Neither YOUTUBE_CLIENT_SECRETS env nor {token_path} found. Skipping YouTube upload.")
    sys.exit(0)

video_path = os.path.join(os.path.dirname(__file__), "..", "data", "eduprosuite_comment_magnet_short.mp4")
file_size = os.path.getsize(video_path) if os.path.exists(video_path) else 0

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "youtube_uploaded_shorts_ledger.json")
uploaded_ledger = {"uploaded_shorts": []}
if os.path.exists(LEDGER_PATH):
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            uploaded_ledger = json.load(f)
    except Exception as e:
        print(f"[!] Warning reading upload ledger: {e}")

metadata_path = os.path.join(os.path.dirname(__file__), "..", "data", "youtube_short_active_metadata.json")
current_id = "unknown"
if os.path.exists(metadata_path):
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            current_id = meta.get("id", "unknown")
            title = meta.get("title", "Secret TI-84 Hack for AP Stats Exam 2026! 📊 (Comment STATS for 90% OFF) #Shorts")
            description = meta.get("description", "")
            tags = meta.get("tags", ["Shorts", "EduProSuite", "ExamPrep"])
            print(f"[+] Loaded rotated YouTube metadata for subject: {current_id.upper()}")
            print(f"    Title: {title}")
    except Exception as e:
        print(f"[!] Warning reading rotated metadata: {e}")
        title = "Secret TI-84 Hack for AP Stats Exam 2026! 📊 (Comment STATS for 90% OFF) #Shorts"
        description = "Master your exam with EduProSuite! Visit https://eduprosuite.pro"
        tags = ["Shorts", "EduProSuite"]
else:
    title = "Secret TI-84 Hack for AP Stats Exam 2026! 📊 (Comment STATS for 90% OFF) #Shorts"

# Anti-duplicate verification: ensure old shorts are never reposted
for item in uploaded_ledger.get("uploaded_shorts", []):
    if item.get("id") == current_id or item.get("title") == title:
        print(f"[!] NOTICE: Subject '{current_id}' ('{title}') was ALREADY uploaded to YouTube on {item.get('uploaded_at')}.")
        print(f"[!] Existing Video URL: {item.get('url')}")
        print("[!] Anti-duplicate rule enforced: Skipping upload to prevent reposting old shorts.")
        sys.exit(0)

payload = {
    "client_id": t.get("client_id"),
    "client_secret": t.get("client_secret"),
    "refresh_token": t.get("refresh_token"),
    "grant_type": "refresh_token"
}
access_token = None
try:
    r = requests.post("https://oauth2.googleapis.com/token", data=payload, timeout=20)
    data = r.json()
    access_token = data.get("access_token")
    if not access_token:
        print(f"[!] Warning: YouTube OAuth token refresh failed ({r.status_code}): {data.get('error_description', data.get('error', 'No access_token'))}")
        print("[!] Video generated locally, but skipping YouTube upload gracefully.")
        sys.exit(0)
except Exception as e:
    print(f"[!] Warning: Failed connecting to YouTube OAuth: {e}")
    sys.exit(0)

init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json; charset=UTF-8",
    "X-Upload-Content-Type": "video/mp4",
    "X-Upload-Content-Length": str(file_size)
}
metadata = {
    "snippet": {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": "27" # Education
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    }
}

init_res = requests.post(init_url, headers=headers, json=metadata)
if init_res.status_code != 200:
    print(f"[!] Warning: YouTube init upload failed ({init_res.status_code}): {init_res.text}")
    print("[!] Skipping YouTube upload gracefully without failing workflow.")
    sys.exit(0)

upload_url = init_res.headers.get("Location")

with open(video_path, "rb") as f:
    upload_res = requests.put(
        upload_url,
        headers={"Content-Type": "video/mp4", "Content-Length": str(file_size)},
        data=f
    )

print(f"Upload status: {upload_res.status_code}")
if upload_res.status_code in [200, 201]:
    new_video_id = upload_res.json()["id"]
    new_url = f"https://youtube.com/shorts/{new_video_id}"
    print(f"[+] SUCCESS! Comment-Magnet Short Uploaded!")
    print(f"[+] Video ID: {new_video_id}")
    print(f"[+] Watch Short URL: {new_url}")
    
    # Record to persistent upload ledger
    import datetime
    uploaded_ledger["uploaded_shorts"].append({
        "id": current_id,
        "title": title,
        "video_id": new_video_id,
        "url": new_url,
        "uploaded_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })
    try:
        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(uploaded_ledger, f, indent=2)
        print(f"[+] Logged upload into {LEDGER_PATH} (Total unique uploads: {len(uploaded_ledger['uploaded_shorts'])})")
    except Exception as e:
        print(f"[!] Warning saving to ledger: {e}")
else:
    print(f"Error: {upload_res.text}")
