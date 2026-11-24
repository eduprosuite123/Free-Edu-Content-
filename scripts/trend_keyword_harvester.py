#!/usr/bin/env python3
"""
scripts/trend_keyword_harvester.py
===================================
EduProSuite Real-Time Search & Telemetry Harvester (Google & YouTube Auto-Suggest).
Harvests high-velocity, real-time search queries (last 24h - 72h intent) for EduProSuite's
approved non-medical niches:
1. Trades: Journeyman Electrician (NEC Code), Journeyman Plumber (UPC/IPC Math), HVAC EPA 608.
2. STEM: AP Calculus AB/BC, AP Statistics, AP Physics.
3. Tech/DevSecOps: GitSEO, Programmatic SEO, SOC 2 Compliance.

Outputs:
- data/daily_trending_keywords.json: Real-time categorized keyword bank.
- Updates data/social_active_rotation_metadata.json with top live search hook.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# Setup logging & UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Strict Non-Medical Product Seed Catalog
PRODUCT_SEEDS = {
    "electrical": {
        "badge": "JOURNEYMAN ELECTRICIAN NEC EXAM",
        "seeds": [
            "journeyman electrician exam prep 2026",
            "nec box fill calculations",
            "conduit bending formulas trade math",
            "electrician apprentice test cheat sheet"
        ],
        "destination_url": "https://eduprosuite.pro/electrician-exam.html",
        "coupon": "TRADEPRO",
        "price": "$29.00",
        "cta_keyword": "NEC"
    },
    "plumbing": {
        "badge": "JOURNEYMAN PLUMBER UPC EXAM",
        "seeds": [
            "journeyman plumber exam study guide",
            "plumbing 45 offset math formulas",
            "upc code test practice questions"
        ],
        "destination_url": "https://eduprosuite.pro/plumber-exam.html",
        "coupon": "TRADEPRO",
        "price": "$29.00",
        "cta_keyword": "PLUMBER"
    },
    "hvac": {
        "badge": "EPA 608 HVAC CERTIFICATION",
        "seeds": [
            "epa 608 universal practice test 2026",
            "hvac evacuation vacuum micron limits",
            "epa 608 core exam cheat sheet"
        ],
        "destination_url": "https://eduprosuite.pro/hvac-exam.html",
        "coupon": "TRADEPRO",
        "price": "$29.00",
        "cta_keyword": "HVAC"
    },
    "ap_calculus": {
        "badge": "AP CALCULUS AB/BC SCORE 5",
        "seeds": [
            "ap calculus ab cheat sheet pdf",
            "ti 84 fnint shortcut ap calculus",
            "ap calculus fundamental theorem traps"
        ],
        "destination_url": "https://eduprosuite.pro/ap-calc-exam.html",
        "coupon": "SCORE5",
        "price": "$29.00",
        "cta_keyword": "CALC"
    },
    "ap_statistics": {
        "badge": "AP STATISTICS SCORE 5",
        "seeds": [
            "ap statistics normalcdf invnorm ti 84",
            "ap stats formula sheet shortcuts",
            "ap stats hypothesis testing p value"
        ],
        "destination_url": "https://eduprosuite.pro/ap-stats-exam.html",
        "coupon": "SCORE5",
        "price": "$29.00",
        "cta_keyword": "STATS"
    },
    "gitseo": {
        "badge": "GITSEO PROGRAMMATIC ENGINE",
        "seeds": [
            "programmatic seo github pages",
            "self hosted programmatic seo",
            "google search console sitemap auto index"
        ],
        "destination_url": "https://eduprosuite.pro/tools/",
        "coupon": "DEVPRO",
        "price": "$29.00",
        "cta_keyword": "GITSEO"
    }
}

def fetch_google_suggestions(query: str) -> list:
    """Fetch live Google search auto-completions."""
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if len(data) > 1 and isinstance(data[1], list):
                return data[1][:5]
    except Exception as e:
        pass
    return []

def fetch_youtube_suggestions(query: str) -> list:
    """Fetch live YouTube search auto-completions."""
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if len(data) > 1 and isinstance(data[1], list):
                return data[1][:5]
    except Exception as e:
        pass
    return []

def harvest_all_trends() -> dict:
    """Harvest real-time queries across all seed groups."""
    print("[+] Harvesting live Google & YouTube auto-suggest telemetry...")
    results = {}
    timestamp = datetime.now(timezone.utc).isoformat()
    
    for prod_id, info in PRODUCT_SEEDS.items():
        results[prod_id] = {
            "badge": info["badge"],
            "google_queries": [],
            "youtube_queries": [],
            "top_hook": ""
        }
        
        seen_g = set()
        seen_yt = set()
        
        for seed in info["seeds"]:
            g_suggs = fetch_google_suggestions(seed)
            for s in g_suggs:
                if s not in seen_g:
                    seen_g.add(s)
                    results[prod_id]["google_queries"].append(s)
            
            yt_suggs = fetch_youtube_suggestions(seed)
            for s in yt_suggs:
                if s not in seen_yt:
                    seen_yt.add(s)
                    results[prod_id]["youtube_queries"].append(s)
                    
        # Pick top hook (first high-intent query found or fallback to first seed)
        top = results[prod_id]["google_queries"][0] if results[prod_id]["google_queries"] else info["seeds"][0]
        results[prod_id]["top_hook"] = top.title()

    output_payload = {
        "last_updated_utc": timestamp,
        "niche_count": len(results),
        "products": results
    }
    
    output_path = DATA_DIR / "daily_trending_keywords.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)
    print(f"[SUCCESS] Saved live trending keywords to: {output_path}")
    
    # Update active social rotation metadata with today's live search hook
    update_active_rotation_metadata(results)
    return output_payload

def update_active_rotation_metadata(harvested: dict):
    """Injects live search intent into data/social_active_rotation_metadata.json."""
    meta_path = DATA_DIR / "social_active_rotation_metadata.json"
    
    # Read existing or pick electrical by default
    active_id = "electrical"
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                cur = json.load(f)
                active_id = cur.get("id", "electrical")
        except Exception:
            pass
            
    if active_id not in PRODUCT_SEEDS:
        active_id = "electrical"
        
    info = PRODUCT_SEEDS[active_id]
    h_data = harvested.get(active_id, {})
    top_hook = h_data.get("top_hook", info["seeds"][0].title())
    yt_top = h_data.get("youtube_queries", [top_hook])[0]
    
    updated_meta = {
        "id": active_id,
        "exam_badge": info["badge"],
        "title": f"{top_hook} (Comment {info['cta_keyword']}) #Shorts",
        "pin_title": f"{top_hook} (Only {info['price']} with Code {info['coupon']})",
        "pin_desc": (
            f"Pass your {info['badge']}! Master {top_hook}. "
            f"Download the full 300+ page exam blueprint and 500 practice MCQs for only {info['price']} "
            f"(90% OFF with code {info['coupon']}) at {info['destination_url']}! "
            f"Pin this to your study board! #Shorts #TradeExam #EduProSuite"
        ),
        "reel_caption": (
            f"⚡ STOP FAILING YOUR {info['badge']}!\n\n"
            f"Here is the proven 2026 shortcut for: {top_hook}\n\n"
            f"CRITICAL EXAM TRAP:\n"
            f"Inspectors and exam writers deliberately test this trap every cycle!\n\n"
            f"SPECIAL 2026 EXAM PREP PASS (90% OFF):\n"
            f"- Full 300+ Page Blueprint & Step-by-Step Problem Solutions\n"
            f"- 500+ Practice MCQs with Instant Explanations\n"
            f"TODAY: ONLY {info['price']} (with code: {info['coupon']})\n\n"
            f"COMMENT '{info['cta_keyword']}' BELOW for free PDF cheat sheet!\n"
            f"Direct Access: {info['destination_url']}"
        ),
        "fb_title": f"{top_hook} (Comment {info['cta_keyword']})",
        "fb_description": (
            f"Stop losing easy points on your {info['badge']}!\n\n"
            f"Mastering: {top_hook}\n\n"
            f"Get complete study blueprint for {info['price']} with promo code: {info['coupon']}\n"
            f"Full Study Guide: {info['destination_url']}"
        ),
        "destination_url": info["destination_url"],
        "coupon": info["coupon"],
        "price": info["price"],
        "cta_keyword": info["cta_keyword"],
        "live_trending_hook": top_hook,
        "youtube_search_intent": yt_top,
        "tags": ["Shorts", "ExamPrep", info["cta_keyword"], "StudyGuide", "EduProSuite"]
    }
    
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(updated_meta, f, indent=2)
    print(f"[SUCCESS] Updated {meta_path} with live trend: '{top_hook}'")

if __name__ == "__main__":
    harvest_all_trends()
