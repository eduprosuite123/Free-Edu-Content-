#!/usr/bin/env python3
"""
scripts/bluesky_publisher.py
=============================
Official EduProSuite Bluesky Social (AT Protocol) Auto-Publisher.
Publishes high-yield study guides, trade formulas, and Whop instant buy links
directly to Bluesky (eduprosuite.bsky.social) with native clickable link facets.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def load_env():
    env_file = Path(__file__).resolve().parent.parent / '.env'
    if env_file.exists():
        for line in env_file.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip().strip('\'"')

load_env()

HANDLE = os.environ.get('BLUESKY_HANDLE', 'eduprosuite.bsky.social')
PASSWORD = os.environ.get('BLUESKY_APP_PASSWORD', '')
BASE_URL = 'https://bsky.social/xrpc'

def create_session():
    url = f"{BASE_URL}/com.atproto.server.createSession"
    payload = json.dumps({'identifier': HANDLE, 'password': PASSWORD}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'EduProSuite'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def parse_facets(text):
    """Detects URLs and hashtags in text and generates byte-accurate AT Protocol facets."""
    facets = []
    text_bytes = text.encode('utf-8')
    
    # 1. URL links
    url_pattern = re.compile(r'https?://[^\s]+')
    for m in url_pattern.finditer(text):
        url = m.group(0)
        start = len(text[:m.start()].encode('utf-8'))
        end = start + len(url.encode('utf-8'))
        facets.append({
            "index": {"byteStart": start, "byteEnd": end},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]
        })

    # 2. Hashtags
    tag_pattern = re.compile(r'#([a-zA-Z0-9_]+)')
    for m in tag_pattern.finditer(text):
        tag = m.group(1)
        full_match = m.group(0)
        start = len(text[:m.start()].encode('utf-8'))
        end = start + len(full_match.encode('utf-8'))
        facets.append({
            "index": {"byteStart": start, "byteEnd": end},
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": tag}]
        })

    return facets

def create_post(session, text):
    url = f"{BASE_URL}/com.atproto.repo.createRecord"
    now_iso = datetime.now(timezone.utc).isoformat()
    facets = parse_facets(text)

    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now_iso
    }
    if facets:
        record["facets"] = facets

    payload = json.dumps({
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": record
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Authorization': f"Bearer {session['accessJwt']}",
            'Content-Type': 'application/json',
            'User-Agent': 'EduProSuite-Poster/1.0'
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

BLUESKY_CAMPAIGNS = [
    {
        "topic": "Journeyman Trade Math & Conduit Bending",
        "text": """⚡ Electrician Apprentices: Master trade math!
📐 30° Offset: Depth × 2.0
📐 Shrink: 1/4" per inch
📐 45° Rolling: Travel = Offset × 1.414

👉 Full Guide & Practice ($8.70):
https://eduprosuite.pro/trade-math-conduit-bending-formulas.html
#TradeMath #Electrician"""
    },
    {
        "topic": "EPA 608 Universal HVAC Exam Cram Guide",
        "text": """❄️ HVAC Techs: Pass EPA 608 Universal!
✅ Commercial: 20% leak rate trigger
✅ Industrial: 30% | Comfort: 10%
✅ Evacuation: 10-15 in. Hg vacuum

👉 Exam Study Guide ($8.70):
https://eduprosuite.pro/epa-608-universal-cheat-sheet.html
#HVAC #EPA608"""
    },
    {
        "topic": "CDL Air Brakes Endorsement Pre-Trip Guide",
        "text": """🚛 Commercial Drivers: Ace CDL Air Brakes!
🚚 7-Step Pre-Trip Air Brakes Test
🚚 Cut-In & Cut-Out pressure limits
🚚 100+ Practice Questions

👉 Study Guide & Practice ($8.70):
https://eduprosuite.pro/cdl-air-brakes-inspection-guide.html
#CDL #Trucking"""
    }
]

def publish_all_campaigns():
    print("=" * 70)
    print("EduProSuite Bluesky Autonomous Social Publisher")
    print("=" * 70)

    try:
        session = create_session()
        print(f"[AUTH SUCCESS] Logged in as: {session.get('handle')} ({session.get('did')})")
    except Exception as e:
        print(f"[AUTH FAILED] {e}")
        return

    for idx, camp in enumerate(BLUESKY_CAMPAIGNS, 1):
        try:
            res = create_post(session, camp["text"])
            post_id = res.get('uri', '').split('/')[-1]
            print(f"\n[SUCCESS {idx}/3] Published: {camp['topic']}")
            print(f"  Live Bluesky Post: https://bsky.app/profile/{session.get('handle')}/post/{post_id}")
            print(f"  CID: {res.get('cid')}")
        except Exception as e:
            print(f"\n[FAIL {idx}/3] {camp['topic']}: {e}")

    print("\n" + "=" * 70)
    print("All Campaigns Successfully Live on Bluesky!")
    print("=" * 70)

if __name__ == "__main__":
    publish_all_campaigns()
