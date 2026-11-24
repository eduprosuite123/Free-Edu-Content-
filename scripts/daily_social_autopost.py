"""
EduProSuite Daily Multi-Channel Social Media Auto-Poster
=========================================================
Automates daily high-value educational content & exam prep tips
distribution across multiple channels:
  - Telegram Channel / Group (Bot API)
  - Discord Community (Webhook)
  - LinkedIn (Share API)
  - Pinterest (Pins API v5)
  - Unified Social Media API (Ayrshare / Upload-Post)
  - YouTube Shorts (Data API v3)

Features:
  - Zero Local RAM requirement (Runs on GitHub Actions cloud)
  - Full Dry-Run simulation & compliance auditing
  - Automatic fallback if specific channel secrets are omitted
  - Structured QA Audit output for CI/CD logs
"""

import os
import sys
import json
import logging
import argparse
import datetime
from typing import Dict, Any, List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("SocialAutoPoster")

# Auto-load local .env if present
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if not os.environ.get(k.strip()):
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env()

# High Buyer-Intent E-Commerce Product Pool for EduProSuite (Diverse Exams & Rotating Fresh Pins)
RAW_ASSETS = "https://raw.githubusercontent.com/eduprosuite-org/eduprosuite-pro-landing/main"

EXAM_TIPS_POOL = [
    {
        "exam": "GitSEO Engine",
        "category": "Developer Tool",
        "topic": "Self-Hosted Programmatic SEO & Multi-Search Auto-Indexing",
        "hook": "🚀 Stop paying $99/mo for SEO SaaS! Self-Host 1,000+ Programmatic Landing Pages for $0 on GitHub:",
        "body": "• Instant Static Page Generator (1,000+ pages built in 1.4s)\n• Automated Google Search Console Sitemaps API Integration\n• Real-Time Bing IndexNow & AI llms.txt Broadcasts\n• 100% Core Web Vitals 99/100 with Zero Server Maintenance",
        "cta": "👉 Get Instant Private GitHub Repository Access:",
        "url": "https://eduprosuite.pro/tools/",
        "image_url": f"{RAW_ASSETS}/pins/pin_git_seo_engine.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_git_seo_engine.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#ProgrammaticSEO", "#GitHubActions", "#WebDev", "#IndieHacker", "#EduProSuite"]
    },
    {
        "exam": "EU AI Act Suite",
        "category": "AI Governance",
        "topic": "Article 9 Risk Management & Annex IV Technical Documentation",
        "hook": "⚖️ The EU AI Act is here! Avoid €35M fines with an Audit-Ready Markdown Compliance Kit in Git:",
        "body": "• Article 9 Risk Assessment & Hazard Register Templates\n• Article 50 AI Transparency Disclosures & Human Oversight SOPs\n• Annex IV Technical File Blueprints for High-Risk AI Systems\n• Pre-configured GitHub Actions Automated Compliance Validator",
        "cta": "👉 Download the Turnkey EU AI Act Git Suite:",
        "url": "https://eduprosuite.pro/tools/",
        "image_url": f"{RAW_ASSETS}/pins/pin_ai_act_compliance.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_ai_act_compliance.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#EUAIAct", "#AIGovernance", "#TechCompliance", "#ISO42001", "#EduProSuite"]
    },
    {
        "exam": "ISO 27001:2022 ISMS",
        "category": "Cloud Security & GRC",
        "topic": "ISO/IEC 27001:2022 ISMS Markdown Control System",
        "hook": "🔒 Cloud & SaaS Founders: Stop paying $12,000/yr for bloated GRC software! Manage your ISO 27001 ISMS in Git:",
        "body": "• Aligned with ISO/IEC 27001:2022 & Annex A (93 security controls)\n• Statement of Applicability (SoA) & Quantitative Risk Register\n• Immutable Git commit history serving as auditor-grade evidence\n• Ready-to-deploy GitHub Actions continuous compliance scanner",
        "cta": "👉 Access the Full ISO 27001 Git ISMS Suite:",
        "url": "https://eduprosuite.pro/tools/",
        "image_url": f"{RAW_ASSETS}/pins/pin_soc2_terraform.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_soc2_terraform.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#ISO27001", "#CyberSecurity", "#DevSecOps", "#CloudSecurity", "#EduProSuite"]
    },
    {
        "exam": "SOC 2 Type II",
        "category": "Cloud Security",
        "topic": "Terraform Policy-as-Code & Automated Audit Evidence Collector",
        "hook": "🛡️ Preparing for SOC 2 Type II? Save $15,000 in DevOps consulting with Policy-as-Code in Git:",
        "body": "• Hardened OpenTofu/Terraform AWS/GCP infrastructure security modules\n• Pre-integrated Checkov & Trivy static analysis on pull requests\n• GitHub Actions cron pipelines for continuous automated evidence collection\n• 100% Auditor-Approved controls for Access Management & Encryption",
        "cta": "👉 Deploy the SOC 2 Policy-as-Code Suite:",
        "url": "https://eduprosuite.pro/tools/",
        "image_url": f"{RAW_ASSETS}/pins/pin_soc2_terraform.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_soc2_terraform.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#SOC2", "#Terraform", "#DevSecOps", "#CyberSecurity", "#EduProSuite"]
    },
    {
        "exam": "Engineering Calculation Suite",
        "category": "Structural Engineering",
        "topic": "Python & Streamlit Eurocode & ASME Sec VIII Pressure Vessel Engine",
        "hook": "🏗️ Engineers: Cancel your $1,000/yr Mathcad license! Automated Eurocode & ASME calculations in Python:",
        "body": "• Validated Eurocode EN 1990-1999 concrete, steel & timber ULS/SLS checks\n• ASME Section VIII Div 1 shell thickness & nozzle reinforcement calculators\n• Automated, vector-sharp PDF calculation note exports for regulatory permits\n• Zero black-box spreadsheet formula corruption errors",
        "cta": "👉 Access the Engineering Python Suite:",
        "url": "https://eduprosuite.pro/tools/",
        "image_url": f"{RAW_ASSETS}/pins/pin_engineering_python.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_engineering_python.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#CivilEngineering", "#StructuralEngineer", "#ASME", "#Eurocodes", "#EduProSuite"]
    },
    {
        "exam": "Certified Fiber Optic Technician (CFOT)",
        "category": "Telecom Credential",
        "topic": "FOA Standards, OTDR Testing & Fiber Splicing Master Guide",
        "hook": "💡 Pass the FOA Certified Fiber Optic Technician (CFOT) Exam! Essential Math & Practice Questions:",
        "body": "• Optical loss budget calculations & dB/km attenuation limits\n• Fusion splicing protocols, cleave angles & mechanical connector standards\n• OTDR event analysis: dead zones, backscatter & reflectance interpretation\n• 250+ Realistic practice test questions with answer explanations",
        "cta": "👉 Download the CFOT Exam Prep Guide:",
        "url": "https://eduprosuite.pro/cfot-fiber-optic.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_cfot_fiber.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_cfot_fiber.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#FiberOptics", "#CFOT", "#Telecommunications", "#NetworkTech", "#EduProSuite"]
    },
    {
        "exam": "Trade Math Formula Sheet",
        "category": "Skilled Trades Math",
        "topic": "Pipe Offsets, 45° Rolling Offsets & Bend Multipliers Cheat Sheet",
        "hook": "📐 Never miscut pipe or conduit again! Printable Trade Math Cheat Sheet for Apprentices & Journeymen:",
        "body": "• 45° and 60° Rolling offset formulas with exact trigonometric travel constants\n• Conduit bending multipliers for 10°, 22.5°, 30°, 45° and 60° bends\n• Hydraulic pressure (psi), head pressure & gallons-per-cubic-foot formulas\n• Printable pocket-sized reference guide for toolboxes and field trucks",
        "cta": "👉 Download the Trade Math Formula Sheet PDF:",
        "url": "https://eduprosuite.pro/review-sheet-trade-math.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_trade_math_sheet.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_trade_math_sheet.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#TradeMath", "#Pipefitter", "#ElectricianApprentice", "#PlumbingMath", "#EduProSuite"]
    },
    {
        "exam": "National Home Inspector Exam (NHIE)",
        "category": "Licensing Exam",
        "topic": "NHIE 200-Question Diagnostic Practice & Code Breakdown",
        "hook": "🏡 The NHIE has a 55% fail rate! Pass your Home Inspector Licensing Exam on your first try:",
        "body": "• Structural systems, foundations & roof framing defect identification\n• Electrical service panels, grounding, bonding & AFCI/GFCI code rules\n• HVAC combustion air, flue clearances & venting requirements\n• 400+ Realistic NHIE practice questions with full diagnostic rationales",
        "cta": "👉 Practice with the NHIE Exam Simulator:",
        "url": "https://eduprosuite.pro/home-inspection.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_home_inspection.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_home_inspection.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#HomeInspector", "#NHIE", "#RealEstateInspection", "#HomeInspectionExam", "#EduProSuite"]
    },
    {
        "exam": "Journeyman Plumber",
        "category": "Trade License",
        "topic": "UPC 2024 Math, DFU Sizing & Venting Rules",
        "hook": "🔧 Master the IPC & UPC Journeyman Plumber Exam! Sizing Fixtures, Venting & Drainage:",
        "body": "• Drainage Fixture Unit (DFU) load tables & minimum slope requirements\n• Water Supply Fixture Units (WSFU) & pressure drop sizing calculations\n• Maximum trap arm distance rules & wet venting configurations\n• 500+ Questions with step-by-step code citations",
        "cta": "👉 Launch the Timed Plumber Exam Simulator:",
        "url": "https://eduprosuite.pro/mock-test-plumber.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_plumber_upc_math.png",
        "facebook_image_url": f"{RAW_ASSETS}/pins/pin_plumber_upc_math.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#PlumberExam", "#JourneymanPlumber", "#PlumbingCode", "#TradeSchool", "#EduProSuite"]
    },
    {
        "exam": "AP Statistics",
        "category": "Book",
        "topic": "300+ Page Mastery Book & CED Blueprint",
        "hook": "📖 Look Inside the 2026 AP Statistics Mastery Book! 300+ pages of step-by-step CED proofs & formulas:",
        "body": "• Complete 9-Unit College Board Syllabus Breakdown\n• 500+ Practice MCQs with Diagnostic Distractor Explanations\n• Step-by-Step FRQ Scoring Rubrics & Calculator Commands (TI-84 NormalCDF & LinReg)\n• Verified Zero Fluff — 100% CED Aligned",
        "cta": "👉 Download the full 300+ Page Book PDF instantly:",
        "url": "https://eduprosuite.pro/ap-stats.html",
        "image_url": f"{RAW_ASSETS}/ap_stats_official_book_pin.png",
        "facebook_image_url": f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "video_url": f"{RAW_ASSETS}/ap_stats_book_look_inside_promo.mp4",
        "tags": ["#APStats", "#APStatisticsBook", "#StudyGuide", "#EduProSuite", "#TextbookPDF"]
    },
    {
        "exam": "AP Statistics",
        "category": "Inference Tree",
        "topic": "Hypothesis Testing & Inference Decision Tree",
        "hook": "⚡ Stop confusing Z-Test vs T-Test! AP Statistics Inference Decision Tree Flowchart:",
        "body": "• 1-Prop Z-Test vs 2-Samp T-Test Conditions (Random, 10%, Normal/Large Counts)\n• Type I vs Type II Error Decision Matrix (α vs β vs Power)\n• Chi-Square Tests of Homogeneity vs Independence breakdown\n• Visual PANIC & PHANTOM Mnemonics for FRQs",
        "cta": "👉 Get the Free High-Res Inference Flowchart PDF:",
        "url": "https://eduprosuite.pro/flashcards-ap-stats.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_stats_inference_tree.png",
        "facebook_image_url": f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "video_url": f"{RAW_ASSETS}/ap_stats_book_look_inside_promo.mp4",
        "tags": ["#APStats", "#HypothesisTesting", "#FormulaSheet", "#CheatSheet", "#EduProSuite"]
    },
    {
        "exam": "AP Calculus AB/BC",
        "category": "Cram Guide",
        "topic": "450+ Essential Theorems, Limits & Derivatives",
        "hook": "📐 Master AP Calculus AB & BC in one sitting! 450+ Theorems, Derivatives & Integral Matrix:",
        "body": "• Complete 10-Unit CED Roadmap from Limits to Infinite Series\n• L'Hopital's Rule, Related Rates 4-Step Algorithm & U-Substitution\n• Integration by Parts, Taylor Series & Lagrange Error Bound\n• Full Step-by-Step FRQ Answer Keys & Score 5 Tips",
        "cta": "👉 Access the AP Calculus AB/BC Formula Cheat Sheet:",
        "url": "https://eduprosuite.pro/ap-calc.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_ap_calculus_matrix.png",
        "facebook_image_url": f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#APCalc", "#CalculusAB", "#CalculusBC", "#STEM", "#EduProSuite"]
    },
    {
        "exam": "Journeyman Plumber",
        "category": "Trade License",
        "topic": "UPC 2024 Math & Drainage Fixture Units (DFU)",
        "hook": "🔧 Pass your Journeyman Plumber Exam on the first attempt! UPC 2024 Math & DFU Cheat Sheet:",
        "body": "• Sizing Drainage Fixture Units (DFU) & Cleanouts under UPC Chapter 7\n• Water Supply Fixture Units (WSFU) & Pressure Drop Calculations\n• Vent Pipe Sizing & Minimum Trap Arm Distances (Table 1002.2)\n• 400+ Realistic Code & Trade Math Practice Questions",
        "cta": "👉 Download the Journeyman Plumber Study Companion:",
        "url": "https://eduprosuite.pro/trade-math.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_plumber_upc_math.png",
        "facebook_image_url": f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#PlumberExam", "#JourneymanPlumber", "#TradeSchool", "#PlumbingCode", "#EduProSuite"]
    },
    {
        "exam": "Journeyman Electrician",
        "category": "Trade License",
        "topic": "NEC 2026 Box Fill, Conduit Bending & Ohm's Law",
        "hook": "⚡ Ace the Journeyman Electrician License Exam! NEC 2026 Calculations & Cheat Sheet:",
        "body": "• Article 314 Box Fill Calculations with Equipment Grounding Conductor allowances\n• Conduit Fill (Chapter 9, Table 1) & 3-Point Saddle Bending formulas\n• Motor Branch Circuit Protection (Article 430) & Continuous Load Rules\n• 500+ Realistic Practice Questions with NEC Article Citations",
        "cta": "👉 Practice with the Timed Electrician Exam Simulator:",
        "url": "https://eduprosuite.pro/mock-test-electrician.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_electrician_nec_math.png",
        "facebook_image_url": f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#ElectricianExam", "#JourneymanElectrician", "#NEC2026", "#TradeMath", "#EduProSuite"]
    },
    {
        "exam": "EPA 608 Universal HVAC",
        "category": "Trade License",
        "topic": "Refrigerant Safety, Recovery & EPA Regulations",
        "hook": "❄️ Get EPA 608 Universal Certified! Core, Type I, Type II & Type III Quick-Cram Guide:",
        "body": "• Clean Air Act Section 608 Venting Prohibition & De-Minimis Release Rules\n• Evacuation Levels for High-Pressure & Low-Pressure Appliances\n• Montreal Protocol & SNAP Approved Low-GWP Refrigerants (A2L Safety)\n• Realistic 100-Question Simulated Exam with Instant Rationales",
        "cta": "👉 Get the EPA 608 Universal Exam Study Guide:",
        "url": "https://eduprosuite.pro/epa-608-technician.html",
        "image_url": f"{RAW_ASSETS}/pins/pin_epa608_hvac_cram.png",
        "facebook_image_url": f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "video_url": f"{RAW_ASSETS}/video.mp4",
        "tags": ["#EPA608", "#HVACTech", "#EPAUniversal", "#HVACR", "#EduProSuite"]
    }
]

def fetch_platform_suggestions(query: str, platform: str = "youtube", limit: int = 5) -> List[str]:
    """
    Harvests native search bar auto-suggestions directly from YouTube or Web suggestions.
    platform='youtube': Queries YouTube's live search-bar suggest API (window.google.ac.h).
    platform='web': Queries Web suggestion API.
    """
    import urllib.parse
    import urllib.request
    import re
    encoded = urllib.parse.quote(query)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    if platform == "youtube":
        url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={encoded}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    raw = resp.read().decode("utf-8", errors="replace")
                    m = re.search(r"window\.google\.ac\.h\((.*)\)", raw)
                    if m:
                        data = json.loads(m.group(1))
                        if len(data) > 1 and isinstance(data[1], list):
                            return [item[0].strip() for item in data[1][:limit] if item and len(item) > 0]
        except Exception as e:
            logger.debug(f"YouTube suggest lookup failed for '{query}': {e}")
            
    # Web / Pinterest-intent suggest query
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={encoded}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                if len(data) > 1 and isinstance(data[1], list):
                    return [s.strip() for s in data[1][:limit] if s.strip()]
    except Exception as e:
        logger.debug(f"Web suggest lookup failed for '{query}': {e}")
        
    return []

def harvest_alphabetical_suggestions(seed_phrase: str, platform: str = "youtube", max_letters: int = 5) -> List[str]:
    """
    Alphabetical Amazon-style keyword harvester:
    Combines the seed query with alphabetical suffixes ('a', 'b', 'c', 'd', 'e'...)
    to uncover high-intent long-tail keywords that appear in native search bars.
    """
    import string
    alphabetical_results = []
    letters_to_check = list(string.ascii_lowercase)[:max_letters]
    
    for char in letters_to_check:
        query = f"{seed_phrase} {char}"
        suggestions = fetch_platform_suggestions(query, platform=platform, limit=2)
        for s in suggestions:
            if s not in alphabetical_results and len(s) > len(seed_phrase):
                alphabetical_results.append(s)
                
    return alphabetical_results

def get_todays_content() -> Dict[str, Any]:
    """
    Selects a deterministically rotated daily tip based on day of year,
    and enriches it with:
    1. YouTube search-bar auto-suggestions (direct from YouTube suggest API)
    2. Alphabetical Amazon-style harvested high-intent exam keywords
    3. Optimized Pinterest pin title, structured description, and direct link.
    """
    day_of_year = datetime.datetime.now(datetime.timezone.utc).timetuple().tm_yday
    item = dict(EXAM_TIPS_POOL[day_of_year % len(EXAM_TIPS_POOL)])
    
    # 1. Platform-Specific Search Bar Harvesting
    search_seed = f"{item['exam']} {item['topic']}".lower()
    exam_seed = f"{item['exam']}".lower()

    # YouTube Native Search Bar Suggestions
    yt_suggestions = fetch_platform_suggestions(search_seed, platform="youtube", limit=4)
    if not yt_suggestions:
        yt_suggestions = fetch_platform_suggestions(f"{item['exam']} cheat sheet", platform="youtube", limit=4)

    # Pinterest Search Bar Auto-Suggestions & Study Board Intent
    pinterest_suggestions = fetch_platform_suggestions(f"{exam_seed} study notes", platform="web", limit=4)
    if not pinterest_suggestions:
        pinterest_suggestions = fetch_platform_suggestions(f"{exam_seed} cheat sheet", platform="web", limit=4)

    # Instagram Search Bar Hashtags & Topic Autocomplete
    clean_tag_base = item['exam'].lower().replace(" ", "").replace("/", "")
    instagram_tags = [
        f"#{clean_tag_base}prep",
        f"#{clean_tag_base}tips",
        f"#{clean_tag_base}review",
        f"#{clean_tag_base}cheatsheet",
        "#studygram",
        "#examprep2026"
    ]

    # 2. Alphabetical Long-Tail Harvesting (A to E query expansion)
    alpha_keywords = harvest_alphabetical_suggestions(exam_seed, platform="youtube", max_letters=5)

    # Combined deduplicated keywords
    item["youtube_suggestions"] = yt_suggestions
    item["pinterest_suggestions"] = pinterest_suggestions
    item["instagram_tags"] = instagram_tags
    item["alphabetical_keywords"] = alpha_keywords[:4]
    item["auto_keywords"] = (pinterest_suggestions + yt_suggestions + alpha_keywords)[:8]

    # Architect high-ranking Pinterest Title & Rich Pin Description strictly from Pinterest Study Board Intent
    top_pin_keyword = pinterest_suggestions[0] if pinterest_suggestions else f"{item['exam']} Study Guide"
    item["pin_title"] = f"📌 {top_pin_keyword.title()} | {item['exam']}"[:95]

    kw_bullet_points = "\n".join([f"✓ {kw.title()}" for kw in item["pinterest_suggestions"][:4]])
    item["pin_description"] = (
        f"{item['hook']}\n\n"
        f"📌 Popular Pinterest Study Board Topics:\n{kw_bullet_points}\n\n"
        f"🎯 Full formula guides, 500+ practice MCQs, and bluebook simulators:\n"
        f"{item['cta']} {item['url']}\n\n"
        f"{' '.join(item['tags'])}"
    )[:790]  # Pinterest description safe limit (<800 chars)

    # Direct claimed link
    item["pin_link"] = item["url"]
    return item

def format_plain_message(content: Dict[str, Any]) -> str:
    """Formats standard text for Telegram, LinkedIn, Pinterest."""
    tags_str = " ".join(content["tags"])
    return (
        f"{content['hook']}\n\n"
        f"📚 Topic: {content['exam']} — {content['topic']}\n\n"
        f"{content['body']}\n\n"
        f"{content['cta']} {content['url']}\n\n"
        f"{tags_str}"
    )

def format_facebook_message(content: Dict[str, Any]) -> str:
    """
    Meta/Facebook Algorithm-Optimized Post:
    - Zero external links in the main post body (bypasses 40%-60% organic reach penalty).
    - Meaningful Social Interaction (MSI) hook: asks a conversational diagnostic question.
    - Explicit call-to-action pointing users to the 1st pinned comment.
    """
    tags_str = " ".join(content["tags"][:3])
    return (
        f"{content['hook']}\n\n"
        f"📚 Focus Topic: {content['exam']} — {content['topic']}\n\n"
        f"{content['body']}\n\n"
        f"💡 Quick Challenge / Question: What is the most difficult concept in this unit for you? Let us know below!\n\n"
        f"📌 [LINK IN FIRST COMMENT 👇] We've pinned the direct download link for the full study guide & practice exam below!\n\n"
        f"{tags_str}"
    )

def format_facebook_comment(content: Dict[str, Any]) -> str:
    """Official 1st Comment containing the destination link (bypasses main-feed link demotion)."""
    return (
        f"👉 Download the complete {content['exam']} study guide & formula sheets here:\n"
        f"🔗 {content['url']}\n"
        f"Includes full 500+ realistic practice questions, formula matrices & interactive scoring!"
    )

def format_twitter_message(content: Dict[str, Any]) -> str:
    """
    X (Twitter) Open-Source Algorithm-Optimized Post:
    - Zero external links in the root tweet to bypass the 30%-70% 'For You' penalty.
    - High-retention educational takeaways under 250 characters.
    - Prompts bookmarks and thread continuation.
    """
    clean_hook = content['hook'].replace("📖 ", "").replace("⚡ ", "").replace("🎯 ", "").replace("🚀 ", "")
    tags_str = " ".join([t for t in content["tags"] if t.startswith("#")][:2])
    first_body_line = content['body'].split("\n")[0] if "\n" in content['body'] else content['body']
    tweet = (
        f"⚡ {content['exam']}: {content['topic']}\n\n"
        f"{clean_hook[:95]}\n"
        f"{first_body_line[:85]}\n\n"
        f"📌 Bookmark this! (Link in reply below 👇)\n{tags_str}"
    )
    return tweet[:280]

def format_twitter_reply(content: Dict[str, Any]) -> str:
    """X 1st reply containing the external link."""
    return f"🔗 Download the full {content['exam']} prep guide & simulator here: {content['url']}"

def format_instagram_caption(content: Dict[str, Any]) -> str:
    """
    Instagram Algorithm-Optimized Post:
    - High-retention educational text.
    - Saves trigger ("Save this post").
    - DM trigger ("Comment below to receive the PDF via DM") for algorithmic velocity.
    - Directs to Link in Bio instead of broken dead URLs in captions.
    """
    clean_tag = content['exam'].replace(" ", "").upper()[:5]
    tags_str = " ".join(content.get("instagram_tags", []) + content["tags"][:3])
    return (
        f"{content['hook']}\n\n"
        f"📚 Topic: {content['exam']} — {content['topic']}\n\n"
        f"{content['body']}\n\n"
        f"💾 SAVE this post to study before your 2026 exam!\n\n"
        f"💬 COMMENT '{clean_tag}' below and we'll automatically send you the complete formula book PDF + simulator access directly to your DMs! 📩\n\n"
        f"🔗 Link also available in bio: eduprosuite.pro\n\n"
        f"{tags_str}"
    )

def post_to_telegram(message: str, dry_run: bool = False) -> Dict[str, Any]:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return {"channel": "Telegram", "status": "SKIPPED", "reason": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing"}
    
    if dry_run:
        return {"channel": "Telegram", "status": "DRY_RUN_PASS", "length": len(message), "target": chat_id}
    
    try:
        import requests
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "disable_web_page_preview": False}
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code == 200:
            return {"channel": "Telegram", "status": "SUCCESS", "response_code": 200}
        return {"channel": "Telegram", "status": "FAILED", "code": resp.status_code, "error": resp.text}
    except Exception as e:
        return {"channel": "Telegram", "status": "ERROR", "error": str(e)}

def post_to_discord(content: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        return {"channel": "Discord", "status": "SKIPPED", "reason": "DISCORD_WEBHOOK_URL missing"}
    
    embed = {
        "title": f"🔥 {content['exam']}: {content['topic']}",
        "description": f"{content['hook']}\n\n{content['body']}",
        "color": 3447003,  # Blue
        "fields": [
            {
                "name": "🎯 Complete Practice Series",
                "value": f"[Enroll & Practice at EduProSuite]({content['url']})",
                "inline": False
            }
        ],
        "footer": {
            "text": "EduProSuite Daily Exam Prep Engine • Free Study Resource"
        },
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    if dry_run:
        return {"channel": "Discord", "status": "DRY_RUN_PASS", "embed_fields": len(embed["fields"])}
    
    try:
        import requests
        resp = requests.post(webhook_url, json={"embeds": [embed]}, timeout=15)
        if resp.status_code in [200, 204]:
            return {"channel": "Discord", "status": "SUCCESS", "response_code": resp.status_code}
        return {"channel": "Discord", "status": "FAILED", "code": resp.status_code, "error": resp.text}
    except Exception as e:
        return {"channel": "Discord", "status": "ERROR", "error": str(e)}

def post_to_linkedin(message: str, dry_run: bool = False) -> Dict[str, Any]:
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.environ.get("LINKEDIN_AUTHOR_URN")
    
    if not access_token or not author_urn:
        return {"channel": "LinkedIn", "status": "SKIPPED", "reason": "LINKEDIN_ACCESS_TOKEN or LINKEDIN_AUTHOR_URN missing"}
    
    if dry_run:
        return {"channel": "LinkedIn", "status": "DRY_RUN_PASS", "length": len(message), "author": author_urn}
    
    try:
        import requests
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code in [200, 201]:
            return {"channel": "LinkedIn", "status": "SUCCESS", "response_code": resp.status_code}
        return {"channel": "LinkedIn", "status": "FAILED", "code": resp.status_code, "error": resp.text}
    except Exception as e:
        return {"channel": "LinkedIn", "status": "ERROR", "error": str(e)}

def post_to_unified_api(message: str, dry_run: bool = False) -> Dict[str, Any]:
    unified_key = os.environ.get("UNIFIED_API_KEY") or os.environ.get("UPLOAD_POST_API_KEY")
    
    if not unified_key:
        return {"channel": "Unified API (Ayrshare/UploadPost)", "status": "SKIPPED", "reason": "UNIFIED_API_KEY missing"}
    
    if dry_run:
        return {"channel": "Unified API", "status": "DRY_RUN_PASS", "message_length": len(message)}
    
    try:
        import requests
        # Support Ayrshare endpoint
        resp = requests.post(
            "https://app.ayrshare.com/api/post",
            json={"post": message, "platforms": ["instagram", "facebook", "pinterest"]},
            headers={"Authorization": f"Bearer {unified_key}", "Content-Type": "application/json"},
            timeout=20
        )
        if resp.status_code == 200:
            return {"channel": "Unified API", "status": "SUCCESS", "response_code": 200}
        return {"channel": "Unified API", "status": "FAILED", "code": resp.status_code, "error": resp.text}
    except Exception as e:
        return {"channel": "Unified API", "status": "ERROR", "error": str(e)}

def post_to_pinterest(content: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    token = os.environ.get("PINTEREST_ACCESS_TOKEN")
    board_id = os.environ.get("PINTEREST_BOARD_ID")
    
    if not token or not board_id:
        return {"channel": "Pinterest", "status": "SKIPPED", "reason": "PINTEREST credentials missing"}
    
    if dry_run:
        return {
            "channel": "Pinterest",
            "status": "DRY_RUN_PASS",
            "board": board_id,
            "title": content.get("pin_title"),
            "keywords": content.get("auto_keywords", [])
        }
        
    try:
        import requests
        url = "https://api.pinterest.com/v5/pins"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        # Use dynamic auto-suggest optimized title, rich description, and direct claimed link
        pin_title = content.get("pin_title") or f"{content['exam']}: {content['topic']}"
        pin_desc = content.get("pin_description") or f"{content['hook']} {content['cta']} {content['url']}"
        pin_link = content.get("pin_link") or content["url"]
        
        payload = {
            "link": pin_link,
            "title": pin_title[:100],
            "description": pin_desc[:800],
            "board_id": board_id,
            "media_source": {
                "source_type": "image_url",
                "url": "https://raw.githubusercontent.com/eduprosuite-org/eduprosuite-pro-landing/main/pinterest_pin.png"
            }
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code in [200, 201]:
            return {"channel": "Pinterest", "status": "SUCCESS", "response_code": resp.status_code}
        return {"channel": "Pinterest", "status": "FAILED", "code": resp.status_code, "error": resp.text}
    except Exception as e:
        return {"channel": "Pinterest", "status": "ERROR", "error": str(e)}

def post_to_make_webhook(content: Dict[str, Any], formatted_msg: str, dry_run: bool = False) -> Dict[str, Any]:
    webhook_url = os.environ.get("MAKE_WEBHOOK_URL")
    
    if not webhook_url:
        return {"channel": "Make.com Webhook", "status": "SKIPPED", "reason": "MAKE_WEBHOOK_URL missing"}
    
    pin_title = content.get("pin_title") or f"{content['exam']}: {content['topic']}"
    pin_desc = content.get("pin_description") or f"{content['hook']} {content['cta']} {content['url']}"
    pin_link = content.get("pin_link") or content["url"]
    
    fb_msg = format_facebook_message(content)
    fb_cmt = format_facebook_comment(content)
    tw_msg = format_twitter_message(content)
    tw_rpl = format_twitter_reply(content)
    ig_cap = format_instagram_caption(content)
    
    payload = {
        "exam": content["exam"],
        "topic": content["topic"],
        "message": formatted_msg,
        "caption": formatted_msg,
        "facebook_message": fb_msg,
        "facebook_post": fb_msg,
        "facebook_comment": fb_cmt,
        "twitter_message": tw_msg,
        "twitter_post": tw_msg,
        "twitter_reply": tw_rpl,
        "instagram_caption": ig_cap,
        "hook": content["hook"],
        "body": content["body"],
        "url": pin_link,
        "link": pin_link,
        "pin_title": pin_title,
        "pin_description": pin_desc,
        "pinterest_keywords": content.get("pinterest_suggestions", []),
        "youtube_keywords": content.get("youtube_suggestions", []),
        "instagram_tags": content.get("instagram_tags", []),
        "auto_keywords": content.get("auto_keywords", []),
        "tags": content["tags"] + content.get("instagram_tags", []),
        "video_url": content.get("video_url") or f"{RAW_ASSETS}/ap_stats_book_look_inside_promo.mp4",
        "image_url": content.get("image_url") or f"{RAW_ASSETS}/ap_stats_official_book_pin.png",
        "facebook_image_url": content.get("facebook_image_url") or f"{RAW_ASSETS}/ap_stats_facebook_book_card.png",
        "board_id": os.environ.get("PINTEREST_BOARD_ID", "1111263345495432591"),
        "board": os.environ.get("PINTEREST_BOARD_ID", "1111263345495432591")
    }
    
    if dry_run:
        return {
            "channel": "Make.com Webhook",
            "status": "DRY_RUN_PASS",
            "payload_fields": len(payload),
            "pin_title": pin_title,
            "pinterest_keywords": content.get("pinterest_suggestions", []),
            "instagram_tags": content.get("instagram_tags", []),
            "auto_keywords": content.get("auto_keywords", [])
        }
        
    try:
        import requests
        resp = requests.post(webhook_url, json=payload, timeout=20)
        if resp.status_code in [200, 201, 204]:
            return {"channel": "Make.com Webhook", "status": "SUCCESS", "response_code": resp.status_code}
        return {"channel": "Make.com Webhook", "status": "FAILED", "code": resp.status_code, "error": resp.text}
    except Exception as e:
        return {"channel": "Make.com Webhook", "status": "ERROR", "error": str(e)}

def run_pipeline(dry_run: bool = False) -> int:
    # Unpack single master config if provided as 1 JSON secret
    master_json = os.environ.get("SOCIAL_MASTER_CONFIG")
    if master_json:
        try:
            cfg = json.loads(master_json)
            if "unified_api_key" in cfg and not os.environ.get("UNIFIED_API_KEY"):
                os.environ["UNIFIED_API_KEY"] = cfg["unified_api_key"]
            if "discord_webhook_url" in cfg and not os.environ.get("DISCORD_WEBHOOK_URL"):
                os.environ["DISCORD_WEBHOOK_URL"] = cfg["discord_webhook_url"]
            if "telegram_bot_token" in cfg and not os.environ.get("TELEGRAM_BOT_TOKEN"):
                os.environ["TELEGRAM_BOT_TOKEN"] = cfg["telegram_bot_token"]
            if "telegram_chat_id" in cfg and not os.environ.get("TELEGRAM_CHAT_ID"):
                os.environ["TELEGRAM_CHAT_ID"] = cfg["telegram_chat_id"]
            if "linkedin_access_token" in cfg and not os.environ.get("LINKEDIN_ACCESS_TOKEN"):
                os.environ["LINKEDIN_ACCESS_TOKEN"] = cfg["linkedin_access_token"]
            if "linkedin_author_urn" in cfg and not os.environ.get("LINKEDIN_AUTHOR_URN"):
                os.environ["LINKEDIN_AUTHOR_URN"] = cfg["linkedin_author_urn"]
            if "pinterest_access_token" in cfg and not os.environ.get("PINTEREST_ACCESS_TOKEN"):
                os.environ["PINTEREST_ACCESS_TOKEN"] = cfg["pinterest_access_token"]
            if "pinterest_board_id" in cfg and not os.environ.get("PINTEREST_BOARD_ID"):
                os.environ["PINTEREST_BOARD_ID"] = cfg["pinterest_board_id"]
            if "make_webhook_url" in cfg and not os.environ.get("MAKE_WEBHOOK_URL"):
                os.environ["MAKE_WEBHOOK_URL"] = cfg["make_webhook_url"]
        except Exception as e:
            logger.warning(f"Could not parse SOCIAL_MASTER_CONFIG: {e}")

    content = get_todays_content()
    formatted_msg = format_plain_message(content)
    
    logger.info("=" * 60)
    logger.info("EduProSuite Daily Social Auto-Post Engine")
    logger.info(f"Target Exam: {content['exam']} | Topic: {content['topic']}")
    logger.info(f"Execution Mode: {'DRY RUN (Simulation)' if dry_run else 'LIVE BROADCAST'}")
    logger.info("=" * 60)
    
    results = [
        post_to_make_webhook(content, formatted_msg, dry_run=dry_run),
        post_to_telegram(formatted_msg, dry_run=dry_run),
        post_to_discord(content, dry_run=dry_run),
        post_to_linkedin(formatted_msg, dry_run=dry_run),
        post_to_pinterest(content, dry_run=dry_run),
        post_to_unified_api(formatted_msg, dry_run=dry_run)
    ]
    
    print("\n" + "=" * 65)
    print(f"| {'CHANNEL':<25} | {'STATUS':<15} | {'DETAILS':<17} |")
    print("=" * 65)
    
    has_failure = False
    success_count = 0
    for r in results:
        status = r.get("status", "UNKNOWN")
        details = str(r.get("reason") or r.get("code") or r.get("response_code") or "Verified OK")[:17]
        print(f"| {r['channel']:<25} | {status:<15} | {details:<17} |")
        if status in ["SUCCESS", "DRY_RUN_PASS"]:
            success_count += 1
        elif status in ["FAILED", "ERROR"]:
            has_failure = True
            
    print("=" * 65)
    print(f"Total Channels Processed: {len(results)} (Successes: {success_count})")
    print(f"Destination Funnel URL: {content['url']}")
    print("=" * 65 + "\n")
    
    # Resilient pipeline: If at least one channel succeeded, allow downstream YouTube and syndication steps
    if success_count > 0:
        return 0
    return 1 if has_failure else 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EduProSuite Daily Social Auto-Poster")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without real HTTP requests")
    parser.add_argument("--live", action="store_true", help="Execute real live HTTP requests")
    args = parser.parse_args()
    
    # Default to dry-run if neither or dry-run is specified
    is_dry = not args.live or args.dry_run
    sys.exit(run_pipeline(dry_run=is_dry))
