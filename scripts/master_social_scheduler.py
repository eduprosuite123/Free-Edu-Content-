#!/usr/bin/env python3
"""
scripts/master_social_scheduler.py
===================================
EduProSuite Official 15-Slot Daily Multi-Channel Social Scheduler (2026 Edition).
Orchestrates automated daily publishing across:
- Facebook (Reels, Link Posts)
- Instagram (Reels, Carousels)
- Pinterest (Video Pins, 2:3 Static Pins)
- Threads (Meta)
- Bluesky (AT Protocol)
- YouTube (Shorts, Long-form Lessons)

Aligned with US Eastern Time (EST), India Standard Time (IST), and UTC.
Strictly non-medical (Trades, STEM, DevSecOps/Software).
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# UTF-8 Console Safety
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 15 Master Scheduled Slots Specification
SCHEDULE_SLOTS = {
    "threads_morning": {
        "est": "08:30 AM", "ist": "06:00 PM", "utc_time": "12:30",
        "platform": "Threads", "type": "Morning Quick Tip",
        "description": "Morning Quick Tip (Formula / Quiz Question)"
    },
    "fb_reel_1": {
        "est": "09:00 AM", "ist": "06:30 PM", "utc_time": "13:00",
        "platform": "Facebook", "type": "Reel",
        "description": "Morning Commute Discovery (Explore / Watch Feed)"
    },
    "bluesky_1": {
        "est": "09:30 AM", "ist": "07:00 PM", "utc_time": "13:30",
        "platform": "Bluesky", "type": "Discussion Post",
        "description": "Tech/Trade Formula & Discussion"
    },
    "ig_carousel": {
        "est": "11:30 AM", "ist": "09:00 PM", "utc_time": "15:30",
        "platform": "Instagram", "type": "Carousel",
        "description": "Lunch Study Break: Educational Slides & Saves"
    },
    "fb_link_post": {
        "est": "01:00 PM", "ist": "10:30 PM", "utc_time": "17:00",
        "platform": "Facebook", "type": "Link Post",
        "description": "Lunch Break Reading: High-CTR Article / Test Links"
    },
    "pinterest_video": {
        "est": "01:30 PM", "ist": "11:00 PM", "utc_time": "17:30",
        "platform": "Pinterest", "type": "Video Pin",
        "description": "Afternoon Impression Spike (Top-of-Funnel Reach)"
    },
    "threads_midday": {
        "est": "02:30 PM", "ist": "12:00 AM", "utc_time": "18:30",
        "platform": "Threads", "type": "Discussion Question",
        "description": "Mid-Day Trade / Exam Question"
    },
    "youtube_long": {
        "est": "03:00 PM", "ist": "12:30 AM", "utc_time": "19:00",
        "platform": "YouTube", "type": "Long Video",
        "description": "In-depth Lesson (Uploaded for evening peak indexing)"
    },
    "bluesky_2": {
        "est": "04:30 PM", "ist": "02:00 AM", "utc_time": "20:30",
        "platform": "Bluesky", "type": "Resource Link",
        "description": "Exam Resource & Practice Question Guide"
    },
    "ig_reel": {
        "est": "06:00 PM", "ist": "03:30 AM", "utc_time": "22:00",
        "platform": "Instagram", "type": "Reel",
        "description": "Evening Viral Discovery (High Shares & DM Sends)"
    },
    "pinterest_static_1": {
        "est": "06:30 PM", "ist": "04:00 AM", "utc_time": "22:30",
        "platform": "Pinterest", "type": "Static Pin 2:3",
        "description": "Evening Planning: 2:3 High Outbound CTR Pin"
    },
    "fb_reel_2": {
        "est": "07:00 PM", "ist": "04:30 AM", "utc_time": "23:00",
        "platform": "Facebook", "type": "Reel",
        "description": "Night Entertainment: Prime-Time Video Watch Window"
    },
    "youtube_shorts": {
        "est": "07:30 PM", "ist": "05:00 AM", "utc_time": "23:30",
        "platform": "YouTube", "type": "Shorts",
        "description": "Mobile Swiping Window: Rapid Subscriber Acquisition"
    },
    "pinterest_static_2": {
        "est": "08:30 PM", "ist": "06:00 AM", "utc_time": "00:30",
        "platform": "Pinterest", "type": "Static Pin 2:3",
        "description": "Night Study Pinning: High-Intent Buyer Traffic"
    },
    "threads_night": {
        "est": "09:00 PM", "ist": "06:30 AM", "utc_time": "01:00",
        "platform": "Threads", "type": "Night Recap",
        "description": "Night Exam Tip / Cheat Sheet Recap"
    }
}

def load_env():
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if not os.environ.get(k.strip()):
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env()

def get_closest_slot() -> str:
    """Calculates the best slot matching current UTC time."""
    now = datetime.now(timezone.utc)
    current_minutes = now.hour * 60 + now.minute
    
    closest_slot = None
    min_diff = 99999
    
    for slot_id, slot_info in SCHEDULE_SLOTS.items():
        sh, sm = map(int, slot_info["utc_time"].split(":"))
        slot_minutes = sh * 60 + sm
        diff = abs(current_minutes - slot_minutes)
        # Handle day wrap around midnight (00:30 / 23:30)
        diff = min(diff, 1440 - diff)
        if diff < min_diff:
            min_diff = diff
            closest_slot = slot_id
            
    return closest_slot or "threads_morning"

def load_active_metadata() -> dict:
    meta_path = DATA_DIR / "social_active_rotation_metadata.json"
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "vector_optimization" not in data:
                    try:
                        import importlib.util
                        spec = importlib.util.spec_from_file_location("social_vector_embedding_optimizer", ROOT_DIR / "scripts" / "social_vector_embedding_optimizer.py")
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        mod.audit_and_optimize_active_rotation()
                        with open(meta_path, "r", encoding="utf-8") as rf:
                            data = json.load(rf)
                    except Exception:
                        pass
                return data
        except Exception:
            pass
    return {
        "id": "electrical",
        "exam_badge": "JOURNEYMAN ELECTRICIAN NEC EXAM",
        "title": "Master Electrician Exam Prep 2026",
        "pin_title": "NEC Box Fill Calculations ($29 with Code TRADEPRO)",
        "destination_url": "https://eduprosuite.pro/electrician-exam.html",
        "price": "$29.00",
        "coupon": "TRADEPRO",
        "cta_keyword": "NEC",
        "live_trending_hook": "Master Electrician Exam Prep 2026"
    }

def get_latest_outlier_reel() -> dict:
    catalog_path = DATA_DIR / "daily_outlier_reels_catalog.json"
    if catalog_path.exists():
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and isinstance(data, list) and len(data) > 0:
                    return data[0]
        except Exception:
            pass
    return {}

def log_dispatch(slot_id: str, mode: str):
    ledger_path = DATA_DIR / "social_dispatch_history.json"
    history = []
    if ledger_path.exists():
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
            
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "slot_id": slot_id,
        "platform": SCHEDULE_SLOTS.get(slot_id, {}).get("platform", "Unknown"),
        "type": SCHEDULE_SLOTS.get(slot_id, {}).get("type", "Unknown"),
        "mode": mode
    }
    history.append(entry)
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(history[-200:], f, indent=2)

def dispatch_make_webhook(payload: dict, dry_run: bool = False):
    webhook_url = os.environ.get("MAKE_WEBHOOK_URL", "https://hook.eu1.make.com/u2mm9t728ojuul02kvalsjbvejofaxrf")
    if dry_run:
        print(f"[DRY-RUN] Make.com Webhook Payload Prepared:")
        print(f"          Target: {webhook_url}")
        print(f"          Action: {payload.get('action', 'social_post')}")
        print(f"          Subject: {payload.get('exam', payload.get('topic'))}")
        return True
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "EduProSuiteScheduler/2.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"[SUCCESS] Make.com Webhook Triggered! Status: {resp.getcode()}")
            return True
    except Exception as e:
        print(f"[-] Make.com Webhook notice: {e}")
        return False

def dispatch_bluesky(title: str, url: str, body: str, dry_run: bool = False):
    handle = os.environ.get("BLUESKY_HANDLE", "eduprosuite.bsky.social")
    password = os.environ.get("BLUESKY_APP_PASSWORD")
    if not password:
        print("[-] Bluesky password not found in .env; skipping.")
        return
    if dry_run:
        print(f"[DRY-RUN] Bluesky Post Prepared for @{handle}:")
        print(f"          Title: {title}")
        print(f"          URL: {url}")
        return
    try:
        sys.path.insert(0, str(ROOT_DIR / "scripts"))
        import bluesky_publisher
        session = bluesky_publisher.create_session()
        post_text = f"⚡ {title}\n\n{body}\n\n👉 Complete Guide: {url}\n\n#TradeMath #ExamPrep #EduProSuite"
        res = bluesky_publisher.create_post(session, post_text)
        print(f"[SUCCESS] Bluesky Post Live! CID: {res.get('cid')}")
    except Exception as e:
        print(f"[-] Bluesky post notice: {e}")

def execute_slot(slot_id: str, dry_run: bool = False):
    slot_info = SCHEDULE_SLOTS.get(slot_id)
    if not slot_info:
        print(f"[-] Unknown slot: {slot_id}")
        return

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n{'=' * 70}")
    print(f" EduProSuite Daily Social Scheduler — Slot: [{slot_id.upper()}]")
    print(f" Platform: {slot_info['platform']} | Format: {slot_info['type']}")
    print(f" Target Schedule: {slot_info['est']} EST | {slot_info['ist']} IST ({slot_info['utc_time']} UTC)")
    print(f" Mode: {'DRY-RUN (Simulated)' if dry_run else 'LIVE PRODUCTION'}")
    print(f" Timestamp: {now_utc}")
    print(f"{'=' * 70}")

    meta = load_active_metadata()
    outlier = get_latest_outlier_reel()
    hook = meta.get("live_trending_hook", meta.get("title", "Exam Prep 2026"))
    badge = meta.get("exam_badge", "EXAM PREP")
    url = meta.get("destination_url", "https://eduprosuite.pro/electrician-exam.html")
    price = meta.get("price", "$29.00")
    coupon = meta.get("coupon", "TRADEPRO")
    cta = meta.get("cta_keyword", "PASS")
    meta_reels = meta.get("meta_reels_payload", {})
    optimized_meta_caption = meta_reels.get("caption") if meta_reels else None

    # Common media URLs (prefer freshly rendered outlier video if available)
    video_url = "https://raw.githubusercontent.com/eduprosuite-org/eduprosuite-pro-landing/main/eduprosuite_viral_trend_reel.mp4"
    pin_image = "https://raw.githubusercontent.com/eduprosuite-org/eduprosuite-pro-landing/main/eduprosuite_viral_trend_pin.png"
    if outlier and outlier.get("file_path"):
        outlier_name = Path(outlier["file_path"]).name
        video_url = f"https://raw.githubusercontent.com/eduprosuite-org/eduprosuite-pro-landing/main/reels/{outlier_name}"

    # Slot-Specific Orchestration
    if slot_id == "threads_morning":
        body = f"Morning Tip: Stop losing points on {hook}! Exam writers test this exact trick. Comment '{cta}' for cheat sheet."
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Threads",
            "message": f"⚡ {badge}: {hook}\n\n{body}\n\n{url}"
        }, dry_run)

    elif slot_id == "fb_reel_1":
        fb_msg = optimized_meta_caption or (outlier.get("captions", {}).get("facebook_reels") if outlier else f"⚡ {hook} Made Simple:\nMaster {badge} rules. Comment '{cta}' for free cheat sheet!\n🔗 {url}\n#TradeMath #{cta} #ExamPrep #EduProSuite")
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Facebook", "format": "Reel",
            "exam": badge, "topic": outlier.get("title", hook) if outlier else hook,
            "facebook_message": fb_msg,
            "video_url": video_url, "image_url": pin_image
        }, dry_run)

    elif slot_id == "bluesky_1":
        dispatch_bluesky(f"{badge}: {hook}", url, f"Morning Discussion: How to master {hook} in under 60 seconds without calculator errors. Use code {coupon} for {price} access.", dry_run)

    elif slot_id == "ig_carousel":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Instagram", "format": "Carousel",
            "caption": f"📘 5 Critical Formulas for {badge} ({hook})! Swipe through and SAVE this post for exam night. Link in bio: {url} #StudyHacks #{cta}",
            "image_url": pin_image, "url": url
        }, dry_run)

    elif slot_id == "fb_link_post":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Facebook", "format": "Link",
            "facebook_post": f"📘 LUNCH BREAK STUDY GUIDE: {badge}\n\nMastering {hook} with full diagnostic formulas.\n\n👉 Complete 300+ Page Blueprint: {url}",
            "link": url, "url": url
        }, dry_run)

    elif slot_id == "pinterest_video":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Pinterest", "format": "Video Pin",
            "pin_title": f"⚡ {hook} | 2026 {badge} Shortcut",
            "pin_description": f"Master {hook}. Download full study guide for {price} (Code {coupon}) at {url}",
            "video_url": video_url, "image_url": pin_image, "board_id": "1111263345495432591"
        }, dry_run)

    elif slot_id == "threads_midday":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Threads",
            "message": f"Mid-Day Quiz: What is the most common mistake in {hook} calculations? Drop your answer below 👇 #ExamPrep"
        }, dry_run)

    elif slot_id == "youtube_long":
        print(f"[+] YouTube Long-form Lesson slot triggered (Mon/Wed/Fri priority).")
        if not dry_run:
            try:
                os.system(f"{sys.executable} scripts/upload_focused_horizontal_video.py")
            except Exception as e:
                print(f"[-] YouTube long notice: {e}")

    elif slot_id == "bluesky_2":
        dispatch_bluesky(f"Study Resource: {badge}", url, f"Afternoon Practice: Reviewing diagnostic MCQs for {hook}. Save this link for pre-exam review.", dry_run)

    elif slot_id == "ig_reel":
        ig_caption = optimized_meta_caption or (outlier.get("captions", {}).get("instagram_reels") if outlier else f"⚡ {hook} Made Simple:\nMaster {badge} rules. Comment '{cta}' for cheat sheet!\n🔗 {url}\n#TradeMath #{cta} #ExamPrep #EduProSuite")
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Instagram", "format": "Reel",
            "caption": ig_caption,
            "video_url": video_url
        }, dry_run)

    elif slot_id == "pinterest_static_1":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Pinterest", "format": "Static Pin",
            "pin_title": f"📌 {hook} Cheat Sheet (Only {price})",
            "pin_description": f"Save this 2:3 pin! Master {hook} for your {badge}. Full prep blueprint at {url}",
            "image_url": pin_image, "link": url, "board_id": "1111263345495432591"
        }, dry_run)

    elif slot_id == "fb_reel_2":
        fb_msg2 = optimized_meta_caption or (outlier.get("captions", {}).get("facebook_reels") if outlier else f"⚡ {hook} Made Simple:\nMaster {badge} rules. Comment '{cta}' for free PDF cheat sheet!\n🔗 {url}\n#TradeMath #{cta} #ExamPrep #EduProSuite")
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Facebook", "format": "Reel",
            "facebook_message": fb_msg2,
            "video_url": video_url
        }, dry_run)

    elif slot_id == "youtube_shorts":
        print(f"[+] YouTube Shorts slot triggered.")
        if not dry_run:
            try:
                os.system(f"{sys.executable} scripts/upload_comment_magnet_short.py")
            except Exception as e:
                print(f"[-] YouTube shorts notice: {e}")

    elif slot_id == "pinterest_static_2":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Pinterest", "format": "Static Pin",
            "pin_title": f"Master {hook} Formulas (Code: {coupon})",
            "pin_description": f"Pin to your exam study board! Full 500 practice MCQs for {badge} at {url}",
            "image_url": pin_image, "link": url, "board_id": "1111263345495432591"
        }, dry_run)

    elif slot_id == "threads_night":
        dispatch_make_webhook({
            "slot": slot_id, "platform": "Threads",
            "message": f"Night Recap: If you are taking the {badge} this month, make sure you have memorized the formulas for {hook}. Sleep well and crush it tomorrow! 🚀 {url}"
        }, dry_run)

    log_dispatch(slot_id, "dry_run" if dry_run else "live")
    print(f"\n[PASS] Successfully executed slot: [{slot_id}]")

def main():
    parser = argparse.ArgumentParser(description="EduProSuite 15-Slot Daily Master Social Scheduler")
    parser.add_argument(
        "--slot",
        choices=list(SCHEDULE_SLOTS.keys()) + ["auto", "list"],
        default="auto",
        help="Slot to execute (default: auto detects current UTC time)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate without firing live webhooks/posts")
    parser.add_argument("--live", action="store_true", help="Run live broadcast")
    args = parser.parse_args()

    if args.slot == "list":
        print(f"\n{'=' * 75}")
        print(f"{'SLOT ID':<20} | {'EST (US)':<10} | {'IST (India)':<12} | {'PLATFORM & TYPE'}")
        print(f"{'=' * 75}")
        for s_id, s_info in SCHEDULE_SLOTS.items():
            print(f"{s_id:<20} | {s_info['est']:<10} | {s_info['ist']:<12} | {s_info['platform']} - {s_info['type']}")
        print(f"{'=' * 75}")
        return

    slot = args.slot
    if slot == "auto":
        slot = get_closest_slot()
        print(f"[+] Auto-detected nearest scheduled slot: {slot}")

    dry_run = not args.live if args.dry_run else not args.live
    execute_slot(slot, dry_run=dry_run)

if __name__ == "__main__":
    main()
