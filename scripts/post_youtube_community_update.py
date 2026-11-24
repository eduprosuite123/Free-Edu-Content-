#!/usr/bin/env python3
"""
YouTube Community Tab & Social Community Post Publisher
======================================================
Creates interactive community posts, discussion starters, and feedback polls
on the YouTube Channel Community/Posts tab and connected social channels.

Features:
- Dynamically retrieves Channel ID via YouTube Data API v3
- Publishes text/poll discussion starters to https://www.googleapis.com/youtube/v3/posts
- Prompts audience feedback on which equations/functions to sonify next
- Cross-posts to Meta Facebook Page if META_PAGE_ACCESS_TOKEN is configured
- 100% Cloud-native on GitHub Actions (Ubuntu/Linux)
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
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RECEIPT_FILE = DATA_DIR / "youtube_last_community_post.json"

# Rotating Community Post Prompts (Feedback & Conversation Starters)
COMMUNITY_PROMPTS = [
    {
        "id": "prompt_01_first_community_welcome",
        "text": """🎧 Welcome to the Acoustic Mathematics Lab!

We just premiered our 10-Equation Masterclass: "What 10 Iconic Math Equations Actually Sound Like" (Watch here: https://youtu.be/eUna7yEAdYc).

We want your feedback for our next episode! Which mathematical curve or equation should we sonify next?

1️⃣ The Mandelbrot Fractal Boundary 🌀
2️⃣ Gravitational Wave Chirp from Binary Black Holes 🌌
3️⃣ The Golden Ratio Logarithmic Spiral 🐚
4️⃣ Quantum Wavepacket Dispersion ⚛️

Drop your vote in the comments below, or tell us which equation blew your mind the most! 👇"""
    },
    {
        "id": "prompt_02_cursed_curve_discussion",
        "text": """🤯 Quick question for math enthusiasts:

When listening to y = x^x, the pitch takes a sudden dive near x = 1/e (~0.368) before rocketing exponentially into ultrasonic frequencies!

Did you know blind and visually impaired mathematicians use this exact stereo sonification in Desmos to detect minimums and vertical asymptotes without sight?

What's the most "cursed" equation you've ever graphed? Let us know below! 👇"""
    },
    {
        "id": "prompt_03_riemann_hypothesis",
        "text": """🎼 The Million-Dollar Sound of the Riemann Zeta Zeros:

All non-trivial zeros lie on the critical line Re(s) = 1/2. When sonified, they produce an eerie acoustic signature closely linked to prime number distributions and quantum chaos energy levels!

Should our next deep dive explore Prime Number Acoustic Patterns or Chaotic Attractors (Lorenz System)?

Vote below! 👇
A) Prime Number Acoustics
B) Lorenz Butterfly Chaos"""
    }
]

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

def get_channel_info(access_token: str):
    url = "https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers, timeout=20)
    if resp.status_code == 200:
        items = resp.json().get("items", [])
        if items:
            return items[0].get("id"), items[0].get("snippet", {}).get("title")
    print(f"[!] Warning fetching channel info: {resp.status_code} - {resp.text}")
    return None, None

def post_community_update():
    access_token = get_valid_access_token()
    channel_id, channel_title = get_channel_info(access_token)
    
    print("\n================================================================================")
    print("CREATING YOUTUBE COMMUNITY TAB POST")
    print(f"Channel: {channel_title} (ID: {channel_id})")
    print("================================================================================")
    
    # Pick prompt from rotation
    state_file = DATA_DIR / "community_post_state.json"
    idx = 0
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                idx = (json.load(f).get("last_index", -1) + 1) % len(COMMUNITY_PROMPTS)
        except Exception:
            idx = 0
            
    prompt = COMMUNITY_PROMPTS[idx]
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump({"last_index": idx, "last_id": prompt["id"]}, f, indent=2)
        
    print(f"Post Text:\n{prompt['text']}\n")
    
    # YouTube Data API v3 Posts endpoint
    post_url = "https://www.googleapis.com/youtube/v3/posts?part=snippet"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    body = {
        "snippet": {
            "channelId": channel_id,
            "textDisplay": prompt["text"]
        }
    }
    
    yt_post_success = False
    post_id = None
    try:
        resp = requests.post(post_url, headers=headers, json=body, timeout=30)
        if resp.status_code in (200, 201):
            res_data = resp.json()
            post_id = res_data.get("id")
            yt_post_success = True
            print("================================================================================")
            print("🎉 [SUCCESS] YOUTUBE COMMUNITY POST PUBLISHED!")
            print(f"Post ID: {post_id}")
            print(f"Channel Community Tab: https://www.youtube.com/channel/{channel_id}/community")
            print("================================================================================\n")
        else:
            print(f"[!] YouTube Posts API Notice (HTTP {resp.status_code}): {resp.text}")
            print("Note: If the channel hasn't completed Advanced Features identity check in YouTube Studio,")
            print("YouTube requires 1-time verification under Settings > Channel > Feature eligibility.")
    except Exception as e:
        print(f"[!] Exception calling YouTube Posts endpoint: {e}")
        
    # Cross-post to Meta Facebook Page if configured
    meta_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
    meta_page_id = os.environ.get("META_PAGE_ID", "1377035332156582")
    if meta_token:
        try:
            fb_url = f"https://graph.facebook.com/v19.0/{meta_page_id}/feed"
            fb_resp = requests.post(fb_url, data={"message": prompt["text"], "access_token": meta_token}, timeout=20)
            if fb_resp.status_code == 200:
                print(f"[+] Cross-posted to Facebook Page successfully: Post ID {fb_resp.json().get('id')}")
        except Exception as e:
            print(f"[!] Meta cross-post notice: {e}")
            
    # Save receipt
    receipt = {
        "channel_id": channel_id,
        "channel_title": channel_title,
        "prompt_id": prompt["id"],
        "post_id": post_id,
        "youtube_success": yt_post_success,
        "community_url": f"https://www.youtube.com/channel/{channel_id}/community" if channel_id else "https://www.youtube.com/@mathsproffesor96/community"
    }
    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
        
    return receipt

if __name__ == "__main__":
    post_community_update()
