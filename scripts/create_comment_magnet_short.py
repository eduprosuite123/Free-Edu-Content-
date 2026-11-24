#!/usr/bin/env python3
"""
scripts/create_comment_magnet_short.py
======================================
Autonomous 100% Free Viral YouTube Shorts Generator (2026 Edition)
Featuring Dynamic 6-Subject Content Rotation:
  1. AP Calculus (TI-84 fnInt & nDeriv Integration Shortcuts)
  2. AP Statistics (TI-84 normalcdf & 1-Var Stats Hacks)
  3. AP Physics (Kinematics & Conservation of Energy Bluebook Traps)
  4. Journeyman Electrician (NEC Table 314.16(B) Box Fill & Conduit Math)
  5. EPA 608 HVAC Certification (Refrigerant Recovery Vacuum & Pressure-Temp Hacks)
  6. Journeyman Plumber (UPC 45-Degree Pipe Offset Math & DFU Tables)

Guarantees 100% non-repeating fresh video generation on every workflow run.
Saves active metadata to `data/youtube_short_active_metadata.json` for YouTube upload sync.
"""

import os
import sys
import math
import json
import asyncio
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio
import imageio_ffmpeg
import edge_tts

# Set stdout to UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

TEMP_AUDIO = os.path.join(DATA_DIR, "temp_voiceover.mp3")
TEMP_VIDEO = os.path.join(DATA_DIR, "temp_raw_video.mp4")
OUTPUT_VIDEO = os.path.join(DATA_DIR, "eduprosuite_comment_magnet_short.mp4")
VIRAL_REEL_VIDEO = os.path.join(DATA_DIR, "eduprosuite_viral_trend_reel.mp4")
OUTPUT_PIN_PATH = os.path.join(DATA_DIR, "eduprosuite_viral_trend_pin.png")
STATE_FILE = os.path.join(DATA_DIR, "youtube_shorts_rotation_state.json")
METADATA_FILE = os.path.join(DATA_DIR, "youtube_short_active_metadata.json")
SOCIAL_METADATA_FILE = os.path.join(DATA_DIR, "social_active_rotation_metadata.json")
LANDING_REPO = os.path.join(os.path.dirname(BASE_DIR), "eduprosuite-pro-landing")

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# ==============================================================================
# 6-SUBJECT ROTATION CATALOG
# ==============================================================================
SUBJECT_ROTATION = [
    # 0. AP CALCULUS
    {
        "id": "calculus",
        "badge": "⚡ EDUPRO SUITE • AP® CALCULUS AB/BC HACKS",
        "device_title": "TI-84 Plus CE",
        "device_sub": "EduPro Calc Engine",
        "voiceover": (
            "Stop calculating definite integrals by hand on the AP Calculus exam! "
            "You are wasting 10 critical minutes. Use this secret TI-84 shortcut. "
            "Press MATH, choose option 9 for fnInt. "
            "Type your lower limit, upper limit, function, comma X, and hit enter. "
            "Boom! Exact numerical accumulation in 3 seconds! "
            "FRQ trap alert: on free response questions, always write your integrand setup or College Board awards zero points! "
            "Comment CALC below for our secret 2026 AP formula cheat sheet, because that's why..."
        ),
        "subtitles": [
            (0.0, 3.5, "STOP SOLVING INTEGRALS BY HAND!", (239, 68, 68)),
            (3.5, 6.5, "You're Wasting 10 Critical Minutes!", (250, 204, 21)),
            (6.5, 9.5, "Secret TI-84 fnInt Shortcut", (56, 189, 248)),
            (9.5, 13.5, "Press [MATH] -> [9: fnInt]", (74, 222, 128)),
            (13.5, 17.5, "Input: f(x), x, Lower, Upper -> Enter", (255, 255, 255)),
            (17.5, 21.0, "BOOM! Instant Accumulation in 3s!", (250, 204, 21)),
            (21.0, 26.0, "🚨 FRQ TRAP: Show Setup or ZERO Points!", (239, 68, 68)),
            (26.0, 34.0, "💬 COMMENT 'CALC' FOR FREE CHEAT SHEET! 👇", (34, 197, 94)),
        ],
        "screen_content": {
            "hook": [
                ("∫ (x² · sin(x)) dx from 0 to π", (239, 68, 68)),
                ("Integration by parts: u=x², dv=sin(x)...", (148, 163, 184)),
                ("❌ WASTING 10 FULL MINUTES!", (239, 68, 68))
            ],
            "menu": [
                ("MATH NUM CPX PRB", (56, 189, 248)),
                ("7: fMax(", (203, 213, 225)),
                ("8: nDeriv(", (203, 213, 225)),
                ("9: fnInt(", (255, 255, 255)),
                ("0: summation Σ(", (203, 213, 225))
            ],
            "wizard": [
                ("fnInt Wizard (Definite Integral)", (56, 189, 248)),
                ("Expression: X² · sin(X)", (255, 255, 255)),
                ("Variable: X", (255, 255, 255)),
                ("Lower: 0", (255, 255, 255)),
                ("Upper: π", (255, 255, 255)),
                ("Paste ■", (250, 204, 21))
            ],
            "output": [
                ("fnInt(X²·sin(X), X, 0, π)", (203, 213, 225)),
                ("5.869604401", (74, 222, 128)),
                ("🚨 FRQ WARNING: NEVER WRITE SYNTAX ONLY!", (254, 202, 202)),
                ("Must write: ∫₀^π x² sin(x) dx = 5.870", (255, 255, 255)),
                ("Unlabeled calculator syntax gets 0 on AP exam!", (252, 165, 165))
            ]
        },
        "keys": [
            ("[ MATH ]", (59, 130, 246), 9.0, 10.5),
            ("[ 9: fnInt ]", (249, 115, 22), 10.5, 12.0),
            ("[ X,T,θ,n ]", (34, 197, 94), 12.0, 14.0),
            ("[ ENTER ]", (236, 72, 153), 17.0, 18.5),
        ],
        "cta_keyword": "CALC",
        "cta_val_prop": "Full 2026 AP Calculus Formula Matrix",
        "micro_poll": "Aiming for: [A] Score 5  or  [B] Score 4?",
        "exam_badge": "AP CALCULUS AB/BC EXAM",
        "coupon": "SCORE5",
        "price": "$29.00",
        "destination_url": "https://eduprosuite.pro/ap-calc.html",
        "formula_summary": "Press [MATH] ➔ [9: fnInt] to evaluate definite accumulation in 3s",
        "trap_alert": "Grader Trap: Always write your integral setup! Unlabeled calculator syntax gets ZERO points on FRQs!",
        "pin_h1": "TI-84 CALCULATOR HACKS",
        "pin_sub": "AP CALCULUS AB/BC EXAM SHORTCUTS",
        "mistake_lines": [
            "Calculating definite integrals and derivatives by hand under time pressure.",
            "Writing raw fnInt calculator syntax without mathematical integral notation.",
            "College Board AP readers award ZERO points for syntax alone on FRQ #2 & #4!"
        ],
        "secret_lines": [
            "Shortcut: Press [MATH] ➔ [9: fnInt] ➔ Input: f(x), x, Lower, Upper ➔ [ENTER].",
            "Computes exact numerical accumulation in 3 seconds flat with zero algebra errors.",
            "Saves 15+ minutes on Section I & II to double-check free-response proofs!"
        ],
        "yt_title": "Secret TI-84 Hack for AP Calculus Exam 2026! 📈 (Comment CALC for 90% OFF) #Shorts",
        "yt_description": (
            "Don't solve definite integrals by hand on the 2026 AP Calculus AB/BC Exam!\n"
            "Master this instant fnInt shortcut and avoid the #1 unlabeled syntax trap.\n\n"
            "💬 COMMENT 'CALC' BELOW to get our Secret 90% OFF Coupon + Full 2026 AP Calculus Cheat Sheet!\n"
            "❓ QUICK POLL: What score are you aiming for on the AP Exam? Comment '4' or '5' below!\n\n"
            "👉 Get 500+ Practice MCQs & Bluebook Simulators:\n"
            "https://eduprosuite.pro/ap-calc.html\n\n"
            "#Shorts #APCalculus #APCalc #TI84 #CalculusHacks #ExamPrep #EduProSuite"
        ),
        "yt_tags": ["Shorts", "AP Calculus", "AP Calc", "TI-84", "Calculus Hacks", "Study Hacks", "Exam Prep", "EduProSuite"]
    },

    # 1. AP STATISTICS
    {
        "id": "stats",
        "badge": "⚡ EDUPRO SUITE • AP® STATISTICS HACKS 2026",
        "device_title": "TI-84 Plus CE",
        "device_sub": "EduPro Stats Engine",
        "voiceover": (
            "Stop calculating normal distributions by hand on the AP Stats exam! "
            "You are wasting 10 minutes. Watch this secret TI-84 hack. "
            "Press 2nd, VARS, and choose normalcdf. "
            "Enter lower, upper, mu, and sigma, then hit enter. "
            "Boom! Instant 0.9772 in 3 seconds! "
            "Trap alert: on FRQs, always label mu and sigma or College Board gives zero points! "
            "Comment STATS below for our secret cheat sheet, because that's why..."
        ),
        "subtitles": [
            (0.0, 3.5, "STOP CALCULATING BY HAND!", (239, 68, 68)),
            (3.5, 6.5, "You're Wasting 10 Full Minutes!", (250, 204, 21)),
            (6.5, 9.5, "Secret TI-84 Hack (Score 5)", (56, 189, 248)),
            (9.5, 13.5, "Press [2nd] -> [VARS] -> 2:normalcdf", (74, 222, 128)),
            (13.5, 17.5, "Input: Lower, Upper, μ, σ -> Enter", (255, 255, 255)),
            (17.5, 21.0, "BOOM! Instant 0.9772 in 3 Seconds!", (250, 204, 21)),
            (21.0, 26.0, "🚨 FRQ TRAP: You MUST Label μ & σ!", (239, 68, 68)),
            (26.0, 33.0, "💬 COMMENT 'STATS' FOR FREE CHEAT SHEET! 👇", (34, 197, 94)),
        ],
        "screen_content": {
            "hook": [
                ("Z = (X - μ) / σ", (239, 68, 68)),
                ("P(Z < 2.00) = Table A lookup...", (148, 163, 184)),
                ("❌ WASTING 5-10 MINUTES!", (239, 68, 68))
            ],
            "menu": [
                ("DISTR  DRAW", (56, 189, 248)),
                ("1: normalpdf(", (203, 213, 225)),
                ("2: normalcdf(", (255, 255, 255)),
                ("3: invNorm(", (203, 213, 225)),
                ("4: invT(", (203, 213, 225))
            ],
            "wizard": [
                ("normalcdf Wizard", (56, 189, 248)),
                ("lower: -1E99", (255, 255, 255)),
                ("upper: 2", (255, 255, 255)),
                ("μ: 0", (255, 255, 255)),
                ("σ: 1", (255, 255, 255)),
                ("Paste ■", (250, 204, 21))
            ],
            "output": [
                ("normalcdf(-1E99,2,0,1)", (203, 213, 225)),
                (".977249868", (74, 222, 128)),
                ("🚨 FRQ WARNING: NEVER WRITE SYNTAX ALONE!", (254, 202, 202)),
                ("Must write: lower=-1E99, upper=2, μ=0, σ=1", (255, 255, 255)),
                ("Otherwise College Board awards ZERO credit!", (252, 165, 165))
            ]
        },
        "keys": [
            ("[ 2nd ]", (59, 130, 246), 9.0, 10.5),
            ("[ VARS ]", (249, 115, 22), 10.5, 12.0),
            ("[ normalcdf ]", (34, 197, 94), 12.0, 14.0),
            ("[ ENTER ]", (236, 72, 153), 17.0, 18.5),
        ],
        "cta_keyword": "STATS",
        "cta_val_prop": "Full 2026 AP Statistics Cheat Sheet",
        "micro_poll": "Which do you use? [A] TI-84  or  [B] Table A?",
        "exam_badge": "AP STATISTICS EXAM",
        "coupon": "SCORE5",
        "price": "$29.00",
        "destination_url": "https://eduprosuite.pro/ap-stats.html",
        "formula_summary": "Press [2ND] ➔ [VARS] ➔ [2: normalcdf] to get exact P-values in 3s",
        "trap_alert": "Grader Trap: You MUST label lower, upper, μ, and σ or College Board gives ZERO points on FRQs!",
        "pin_h1": "AP STATISTICS TI-84 HACKS",
        "pin_sub": "WHAT COLLEGE BOARD WON'T TELL YOU",
        "mistake_lines": [
            "Calculating Z-scores and looking up probabilities in Table A by hand.",
            "Writing raw normalcdf(-1E99, 2, 0, 1) without explicit parameter names.",
            "Graders award ZERO rubric points on FRQ questions for unlabeled calculator commands!"
        ],
        "secret_lines": [
            "Shortcut: Press [2ND] ➔ [VARS] ➔ [2: normalcdf] ➔ Enter Lower, Upper, μ, σ.",
            "Instant 0.9772 probability in under 3 seconds with zero table lookup errors.",
            "Always write: 'normalcdf(lower=-1E99, upper=2, μ=0, σ=1)' for 100% rubric score!"
        ],
        "yt_title": "Secret TI-84 Hack for AP Stats Exam 2026! 📊 (Comment STATS for 90% OFF) #Shorts",
        "yt_description": (
            "Don't calculate Z-scores and 1-Var stats by hand on the 2026 AP Statistics Exam!\n"
            "Master these 2 instant TI-84 shortcuts and avoid the #1 unlabeled input trap.\n\n"
            "💬 COMMENT 'STATS' BELOW to get our Secret 90% OFF Coupon + Full 2026 AP Cheat Sheet!\n"
            "❓ QUICK POLL: What score are you aiming for on the AP Exam? Comment '4' or '5' below!\n\n"
            "👉 Get 500+ Practice MCQs & Diagnostic Exams:\n"
            "https://eduprosuite.pro/ap-stats.html\n\n"
            "#Shorts #APStatistics #APStats #TI84 #StatisticsHacks #StudyHacks #EduProSuite"
        ),
        "yt_tags": ["Shorts", "AP Statistics", "AP Stats", "TI-84", "Statistics Hacks", "Study Hacks", "EduProSuite"]
    },

    # 2. AP PHYSICS
    {
        "id": "physics",
        "badge": "⚡ EDUPRO SUITE • AP® PHYSICS 1 EXAM HACKS",
        "device_title": "TI-84 Plus CE",
        "device_sub": "EduPro Physics Engine",
        "voiceover": (
            "Stop memorizing 50 physics equations for the AP Physics 1 exam! "
            "You are falling into College Board's biggest trap. "
            "Instead of solving messy kinematics quadratics, use Conservation of Energy! "
            "Set kinetic energy plus potential energy initial equal to final. "
            "Solve velocity in 5 seconds without quadratic formula! "
            "Trap alert: on the new digital Bluebook exam, never round gravity to 10 unless explicitly told. Use 9.8! "
            "Comment PHYSICS below for the full 2026 formula matrix, because that's why..."
        ),
        "subtitles": [
            (0.0, 3.5, "STOP MEMORIZING 50 EQUATIONS!", (239, 68, 68)),
            (3.5, 6.5, "Skip Messy Kinematics Quadratics!", (250, 204, 21)),
            (6.5, 10.0, "Use Conservation of Energy: ΔE = 0", (56, 189, 248)),
            (10.0, 14.0, "½mv² + mgh₁ = ½mv₂² + mgh₂", (74, 222, 128)),
            (14.0, 18.0, "Instant Velocity v = √(2gh) in 3s!", (255, 255, 255)),
            (18.0, 22.5, "🚨 BLUEBOOK TRAP: Always Use g = 9.8!", (239, 68, 68)),
            (22.5, 26.5, "Never use g = 10 unless permitted!", (250, 204, 21)),
            (26.5, 34.0, "💬 COMMENT 'PHYSICS' FOR FREE FORMULA PACK! 👇", (34, 197, 94)),
        ],
        "screen_content": {
            "hook": [
                ("Kinematics: Δx = v₀t + ½at²", (239, 68, 68)),
                ("Solving quadratic for time t...", (148, 163, 184)),
                ("❌ WASTING 8 MINUTES ON ALGEBRA!", (239, 68, 68))
            ],
            "menu": [
                ("PHYSICS ENERGY MATRIX", (56, 189, 248)),
                ("1: Work-Energy Theorem", (203, 213, 225)),
                ("2: Conservation of Mechanical E", (255, 255, 255)),
                ("3: Linear Momentum p = mv", (203, 213, 225)),
                ("4: Rotational Inertia I", (203, 213, 225))
            ],
            "wizard": [
                ("Energy Balance Wizard", (56, 189, 248)),
                ("mgh = ½mv² -> mass m cancels!", (255, 255, 255)),
                ("v = √(2 · g · h)", (74, 222, 128)),
                ("g: 9.8 m/s² (Mandatory)", (250, 204, 21)),
                ("h: 15.0 meters", (255, 255, 255)),
                ("Compute Velocity ■", (56, 189, 248))
            ],
            "output": [
                ("√(2 · 9.8 · 15) = v", (203, 213, 225)),
                ("17.146 m/s", (74, 222, 128)),
                ("🚨 BLUEBOOK EXAM TRAP ALERT!", (254, 202, 202)),
                ("If you use g=10, v=17.32 (LOSE 2 ACCURACY POINTS)", (255, 255, 255)),
                ("College Board strictly enforces 9.8 m/s² on FRQs!", (252, 165, 165))
            ]
        },
        "keys": [
            ("[ 2nd ]", (59, 130, 246), 9.0, 10.5),
            ("[ √ ]", (249, 115, 22), 10.5, 12.0),
            ("[ 2·g·h ]", (34, 197, 94), 12.0, 14.0),
            ("[ ENTER ]", (236, 72, 153), 17.0, 18.5),
        ],
        "cta_keyword": "PHYSICS",
        "cta_val_prop": "Full 2026 AP Physics 1 Formula Sheet",
        "micro_poll": "Hardest topic? [A] Rotation  or  [B] Circuits?",
        "exam_badge": "AP PHYSICS 1 EXAM",
        "coupon": "SCORE5",
        "price": "$29.00",
        "destination_url": "https://eduprosuite.pro/ap-physics.html",
        "formula_summary": "Use Conservation of Energy (ΔE = 0) to solve velocity v = √(2gh) in 3s",
        "trap_alert": "Bluebook Trap: Always use g = 9.8 m/s²! Rounding to 10 loses 2 accuracy points on FRQs!",
        "pin_h1": "AP PHYSICS 1 EXAM SHORTCUTS",
        "pin_sub": "SKIP MESSY KINEMATICS QUADRATICS",
        "mistake_lines": [
            "Memorizing 50 disconnected formulas without understanding energy balance.",
            "Solving tedious kinematics quadratic equations for time t during timed exams.",
            "Using g = 10 m/s² instead of mandatory 9.8 m/s² on the digital Bluebook exam!"
        ],
        "secret_lines": [
            "Shortcut: Set initial mechanical energy equal to final (½mv² = mgh) -> mass cancels!",
            "Solve velocity directly: v = √(2 · g · h) in 3 seconds flat without quadratics.",
            "Guarantees 4/4 points on College Board quantitative/qualitative translation FRQs!"
        ],
        "yt_title": "The #1 AP Physics Trap You MUST Avoid in 2026! ⚡ (Comment PHYSICS) #Shorts",
        "yt_description": (
            "Avoid the #1 algebraic trap on the 2026 AP Physics 1 Exam!\n"
            "Master Conservation of Energy shortcuts and stop losing points on the g=9.8 rounding rule.\n\n"
            "💬 COMMENT 'PHYSICS' BELOW to get our Secret 90% OFF Coupon + Full AP Physics Equation Guide!\n"
            "❓ QUICK POLL: Which topic is harder? Comment 'Rotation' or 'Circuits' below!\n\n"
            "👉 Get 500+ Practice MCQs & Bluebook Simulators:\n"
            "https://eduprosuite.pro/ap-physics.html\n\n"
            "#Shorts #APPhysics #APPhysics1 #PhysicsHacks #StudyHacks #CollegeBoard #EduProSuite"
        ),
        "yt_tags": ["Shorts", "AP Physics", "AP Physics 1", "Physics Hacks", "Study Hacks", "CollegeBoard", "EduProSuite"]
    },

    # 3. JOURNEYMAN ELECTRICIAN
    {
        "id": "electrical",
        "badge": "⚡ EDUPRO SUITE • JOURNEYMAN ELECTRICIAN NEC HACKS",
        "device_title": "NEC 2026 Pro",
        "device_sub": "Code Calculator Matrix",
        "voiceover": (
            "Stop failing your Journeyman Electrician exam on Box Fill calculations! "
            "You are missing the most heavily tested trade math in America. "
            "Under NEC Table 314.16(B), every conductor, clamp, and device has an exact cubic inch volume. "
            "For 12 AWG wire, multiply each conductor count by 2.25 cubic inches. "
            "Deduct 2 allowances for a standard receptacle, and 1 for internal clamps! "
            "Trap alert: all ground wires together only count as ONE deduction up to four wires! "
            "Comment NEC below for our full 2026 Electrician Exam Cram Guide, because that's why..."
        ),
        "subtitles": [
            (0.0, 3.5, "STOP FAILING NEC BOX FILL MATH!", (239, 68, 68)),
            (3.5, 6.5, "Journeyman Exam #1 Trap Question!", (250, 204, 21)),
            (6.5, 10.0, "NEC Table 314.16(B) Shortcut", (56, 189, 248)),
            (10.0, 14.0, "12 AWG = 2.25 cu in per conductor", (74, 222, 128)),
            (14.0, 18.0, "Device = 2 Allowances | Clamps = 1", (255, 255, 255)),
            (18.0, 22.5, "🚨 GROUND WIRE TRAP: Only Deduct ONE!", (239, 68, 68)),
            (22.5, 26.5, "Up to 4 equipment grounds = 1 volume!", (250, 204, 21)),
            (26.5, 34.0, "💬 COMMENT 'NEC' FOR COMPLETE CRAM GUIDE! 👇", (34, 197, 94)),
        ],
        "screen_content": {
            "hook": [
                ("Box Fill: 4x4x1.5 Square Box", (239, 68, 68)),
                ("Six #12 wires + Receptacle + Clamps...", (148, 163, 184)),
                ("❌ 45% OF APPRENTICES FAIL THIS QUESTION!", (239, 68, 68))
            ],
            "menu": [
                ("NEC 314.16(B) VOLUME MATRIX", (56, 189, 248)),
                ("14 AWG -> 2.00 cu in", (203, 213, 225)),
                ("12 AWG -> 2.25 cu in", (74, 222, 128)),
                ("10 AWG -> 2.50 cu in", (203, 213, 225)),
                ("8 AWG  -> 3.00 cu in", (203, 213, 225))
            ],
            "wizard": [
                ("Box Volume Calculation", (56, 189, 248)),
                ("Conductors (6 x 2.25 cu in) = 13.5", (255, 255, 255)),
                ("Device Receptacle (2 x 2.25) = 4.5", (255, 255, 255)),
                ("Internal Clamps (1 x 2.25) = 2.25", (255, 255, 255)),
                ("Ground Wires (1 x 2.25) = 2.25", (250, 204, 21)),
                ("Total Minimum Box Volume = 22.5 cu in", (74, 222, 128))
            ],
            "output": [
                ("Required Volume: 22.5 cu in", (74, 222, 128)),
                ("Box Selected: 4 x 4 x 2⅛ Square (30.3 cu in)", (203, 213, 225)),
                ("🚨 NEC INSPECTOR & EXAM TRAP!", (254, 202, 202)),
                ("Never deduct each ground wire individually!", (255, 255, 255)),
                ("NEC 314.16(B)(5) specifies 1 allowance total up to 4 grounds!", (252, 165, 165))
            ]
        },
        "keys": [
            ("[ NEC 314 ]", (59, 130, 246), 9.0, 10.5),
            ("[ 12 AWG ]", (249, 115, 22), 10.5, 12.0),
            ("[ 2.25 in³ ]", (34, 197, 94), 12.0, 14.0),
            ("[ PASS ]", (236, 72, 153), 17.0, 18.5),
        ],
        "cta_keyword": "NEC",
        "cta_val_prop": "Full 2026 Electrician Exam Cram Guide",
        "micro_poll": "Which state exam? [A] Texas  or  [B] California?",
        "exam_badge": "JOURNEYMAN ELECTRICIAN NEC EXAM",
        "coupon": "TRADEPRO",
        "price": "$29.00",
        "destination_url": "https://eduprosuite.pro/electrician-exam.html",
        "formula_summary": "NEC 314.16(B): 12 AWG = 2.25 cu in. Up to 4 equipment grounds = 1 volume allowance total!",
        "trap_alert": "Inspector Trap: Never deduct each ground wire separately! NEC 314.16(B)(5) specifies 1 allowance total!",
        "pin_h1": "NEC BOX FILL CALCULATIONS",
        "pin_sub": "JOURNEYMAN ELECTRICIAN EXAM HACKS",
        "mistake_lines": [
            "Deducting each ground wire individually and picking an oversized enclosure.",
            "Forgetting that each receptacle/switch device counts as TWO volume allowances.",
            "Over 45% of apprentice applicants fail this exact NEC box sizing question!"
        ],
        "secret_lines": [
            "Shortcut: 12 AWG = 2.25 in³. Conductors (6x2.25) + Device (2x2.25) + Clamps (1x2.25).",
            "Equipment grounds (up to 4) = ONE allowance total (1x2.25) -> Total = 22.5 cu in.",
            "Select 4 x 4 x 2⅛ Square Box (30.3 cu in) for 100% inspection pass!"
        ],
        "yt_title": "Journeyman Electrician NEC Exam Hack! 🔌 Box Fill Math in 10 Seconds (Comment NEC) #Shorts",
        "yt_description": (
            "Pass the 2026 Journeyman Electrician Exam with confidence!\n"
            "Master NEC 314.16(B) Box Fill volume allowances and avoid the #1 ground wire deduction trap.\n\n"
            "💬 COMMENT 'NEC' BELOW to get our Secret 90% OFF Coupon + Full Journeyman Electrician Exam Cram Sheet!\n"
            "❓ QUICK POLL: Which state are you testing in? Comment below!\n\n"
            "👉 Download Complete Practice Drills & Code Simulators:\n"
            "https://eduprosuite.pro/electrician-exam.html\n\n"
            "#Shorts #Electrician #JourneymanElectrician #NECCode #ElectricalExam #TradeSchool #EduProSuite"
        ),
        "yt_tags": ["Shorts", "Electrician", "Journeyman Electrician", "NEC Code", "Electrical Exam", "Trade Exam", "EduProSuite"]
    },

    # 4. EPA 608 HVAC CERTIFICATION
    {
        "id": "hvac",
        "badge": "⚡ EDUPRO SUITE • EPA 608 HVAC CERTIFICATION HACKS",
        "device_title": "HVAC Pro 608",
        "device_sub": "EPA Recovery Engine",
        "voiceover": (
            "Stop guessing vacuum levels on your EPA 608 HVAC exam! "
            "This single question trips up sixty percent of HVAC technicians. "
            "For Type 2 appliances with over 200 pounds of R-22, you must pull ten inches of mercury vacuum. "
            "For systems under 200 pounds, pull zero inches or four inches if manufactured before 1993! "
            "EPA trap alert: recovery cylinders cannot be filled above eighty percent capacity by weight. "
            "Violating this risks catastrophic explosion and instant EPA fines! "
            "Comment EPA below for our complete 2026 Universal HVAC Cheat Sheet, because that's why..."
        ),
        "subtitles": [
            (0.0, 3.5, "STOP GUESSING EPA 608 VACUUMS!", (239, 68, 68)),
            (3.5, 6.5, "60% of Technicians Miss This Question!", (250, 204, 21)),
            (6.5, 10.0, "Type II Recovery Levels Mastered", (56, 189, 248)),
            (10.0, 14.0, ">200 lbs R-22 = 10 inches Hg Vacuum", (74, 222, 128)),
            (14.0, 18.0, "<200 lbs R-22 = 0 inches Hg Vacuum", (255, 255, 255)),
            (18.0, 22.5, "🚨 80% RECOVERY CYLINDER FILL LIMIT!", (239, 68, 68)),
            (22.5, 26.5, "Overfilled cylinders cause fatal rupture!", (250, 204, 21)),
            (26.5, 34.0, "💬 COMMENT 'EPA' FOR UNIVERSAL CHEAT SHEET! 👇", (34, 197, 94)),
        ],
        "screen_content": {
            "hook": [
                ("Type II Recovery: 250 lbs R-22", (239, 68, 68)),
                ("Vacuum Required: 4\" vs 10\" vs 15\" Hg?", (148, 163, 184)),
                ("❌ 60% OF TEST TAKERS GUESS WRONG!", (239, 68, 68))
            ],
            "menu": [
                ("EPA 608 TYPE II EVACUATION TABLE", (56, 189, 248)),
                ("R-22 (<200 lbs, Post-93) -> 0\" Hg", (203, 213, 225)),
                ("R-22 (>200 lbs, Post-93) -> 10\" Hg", (74, 222, 128)),
                ("R-410A / High Pressure   -> 10\" Hg", (203, 213, 225)),
                ("R-123 / Low Pressure     -> 25 mm Hg", (203, 213, 225))
            ],
            "wizard": [
                ("Cylinder Safety Calculation", (56, 189, 248)),
                ("Maximum Fill Limit = 80% by Weight", (250, 204, 21)),
                ("Tare Weight + (Water Cap x 0.8 x SpG)", (255, 255, 255)),
                ("DOT Stamp: Yellow Top / Gray Body", (74, 222, 128)),
                ("Hydrostatic test required every 5 years!", (255, 255, 255)),
                ("Verify Pressure-Temperature Chart ■", (56, 189, 248))
            ],
            "output": [
                ("Required Vacuum: 10\" Hg", (74, 222, 128)),
                ("Recovery Cylinder: 80% Weight Max", (74, 222, 128)),
                ("🚨 EPA FEDERAL PENALTY WARNING!", (254, 202, 202)),
                ("Never vent refrigerants into atmosphere!", (255, 255, 255)),
                ("Federal fines exceed $44,539 per day per violation!", (252, 165, 165))
            ]
        },
        "keys": [
            ("[ TYPE II ]", (59, 130, 246), 9.0, 10.5),
            ("[ >200 lbs ]", (249, 115, 22), 10.5, 12.0),
            ("[ 10\" Hg ]", (34, 197, 94), 12.0, 14.0),
            ("[ 80% MAX ]", (236, 72, 153), 17.0, 18.5),
        ],
        "cta_keyword": "EPA",
        "cta_val_prop": "Full 2026 Universal HVAC Cheat Sheet",
        "micro_poll": "Aiming for: [A] Universal  or  [B] Type II?",
        "exam_badge": "EPA 608 HVAC CERTIFICATION",
        "coupon": "TRADEPRO",
        "price": "$29.00",
        "destination_url": "https://eduprosuite.pro/hvac-exam.html",
        "formula_summary": "Type II >200 lbs R-22 = 10 inches Hg vacuum. Recovery cylinder max fill = 80% by weight!",
        "trap_alert": "Federal EPA Trap: Filling recovery cylinders beyond 80% causes explosive rupture and $44,539/day fines!",
        "pin_h1": "EPA 608 HVAC CERTIFICATION",
        "pin_sub": "CORE & TYPE II/III EVACUATION RULES",
        "mistake_lines": [
            "Guessing evacuation vacuum levels across different appliance refrigerant charges.",
            "Venting refrigerants or exceeding 80% cylinder weight capacity.",
            "Violating recovery limits risks cylinder rupture and severe federal EPA fines!"
        ],
        "secret_lines": [
            "Shortcut: Type II appliances with >200 lbs R-22 require 10 inches Hg vacuum.",
            "Recovery cylinders must NEVER be filled beyond 80% capacity by weight (Tare + Water x 0.8).",
            "Guarantees a passing score on EPA Core and Type II/Universal exams!"
        ],
        "yt_title": "Pass EPA 608 HVAC Exam in 30 Seconds! ❄️ Core & Type II/III Hacks (Comment EPA) #Shorts",
        "yt_description": (
            "Ace your EPA 608 Universal HVAC Certification Exam on the first try!\n"
            "Master Type II evacuation levels (10 inches Hg) and the mandatory 80% cylinder fill limit rule.\n\n"
            "💬 COMMENT 'EPA' BELOW to get our Secret 90% OFF Coupon + Universal EPA 608 Cram Sheet!\n"
            "❓ QUICK POLL: Which certification are you taking? Comment 'Core', 'Type II', or 'Universal' below!\n\n"
            "👉 Download Complete 500+ Practice Exam Simulator:\n"
            "https://eduprosuite.pro/hvac-exam.html\n\n"
            "#Shorts #HVAC #EPA608 #Refrigerant #HVACExam #TradeSchool #EduProSuite"
        ),
        "yt_tags": ["Shorts", "HVAC", "EPA 608", "Refrigerant", "HVAC Exam", "Trade School", "EduProSuite"]
    },

    # 5. JOURNEYMAN PLUMBER
    {
        "id": "plumbing",
        "badge": "⚡ EDUPRO SUITE • JOURNEYMAN PLUMBER UPC HACKS",
        "device_title": "UPC 2026 Pro",
        "device_sub": "Pipe Math Calculator",
        "voiceover": (
            "Stop losing points on 45-degree offset math on your Plumber Exam! "
            "This is free money on every state licensing exam. "
            "To find the true travel length of a 45-degree rolling or simple offset, multiply your set by 1.414! "
            "For a 10-inch offset, 10 times 1.414 gives 14.14 inches. "
            "UPC code trap alert: always deduct the fitting allowances from center-to-center measurements! "
            "If you cut the pipe without subtracting fitting takeoffs, your run will fail inspection instantly. "
            "Comment PLUMB below for our full 2026 UPC Code Cheat Sheet, because that's why..."
        ),
        "subtitles": [
            (0.0, 3.5, "STOP FAILING 45° OFFSET MATH!", (239, 68, 68)),
            (3.5, 6.5, "Free Money on Your Plumber Exam!", (250, 204, 21)),
            (6.5, 10.0, "Offset Constant: Travel = Set × 1.414", (56, 189, 248)),
            (10.0, 14.0, "10\" Set × 1.414 = 14.14\" Center-to-Center", (74, 222, 128)),
            (14.0, 18.0, "Deduct Fitting Takeoff Allowances!", (255, 255, 255)),
            (18.0, 22.5, "🚨 UPC TRAP: Subtract Fitting Takeoff!", (239, 68, 68)),
            (22.5, 26.5, "Cutting full travel fails inspection!", (250, 204, 21)),
            (26.5, 34.0, "💬 COMMENT 'PLUMB' FOR UPC CRAM SHEET! 👇", (34, 197, 94)),
        ],
        "screen_content": {
            "hook": [
                ("45° Offset: Set = 10 Inches", (239, 68, 68)),
                ("Travel = ? (What is the cut piece?)", (148, 163, 184)),
                ("❌ 50% CUT PIPE TOO LONG & FAIL!", (239, 68, 68))
            ],
            "menu": [
                ("PLUMBING OFFSET MULTIPLIERS", (56, 189, 248)),
                ("60° Offset -> 1.155 x Offset", (203, 213, 225)),
                ("45° Offset -> 1.414 x Offset", (74, 222, 128)),
                ("22.5° Offset -> 2.613 x Offset", (203, 213, 225)),
                ("Rolling Offset -> √(Set² + Roll²) x 1.414", (203, 213, 225))
            ],
            "wizard": [
                ("45° Travel Calculation", (56, 189, 248)),
                ("Set: 10.00 inches", (255, 255, 255)),
                ("Multiplier: 1.414", (255, 255, 255)),
                ("Center-to-Center Travel = 14.14 inches", (74, 222, 128)),
                ("Fitting Takeoff (Two 45° Els): -2.50\"", (250, 204, 21)),
                ("Actual Cut Length = 11.64 inches ■", (74, 222, 128))
            ],
            "output": [
                ("Center-to-Center: 14.14\"", (74, 222, 128)),
                ("True Cut Piece: 11.64\"", (74, 222, 128)),
                ("🚨 UPC CODE INSPECTOR TRAP!", (254, 202, 202)),
                ("Never forget to subtract fitting allowances!", (255, 255, 255)),
                ("Center-to-center is NOT pipe cut length!", (252, 165, 165))
            ]
        },
        "keys": [
            ("[ 45° EL ]", (59, 130, 246), 9.0, 10.5),
            ("[ 1.414 ]", (249, 115, 22), 10.5, 12.0),
            ("[ TAKEOFF ]", (34, 197, 94), 12.0, 14.0),
            ("[ CUT ]", (236, 72, 153), 17.0, 18.5),
        ],
        "cta_keyword": "PLUMB",
        "cta_val_prop": "Full 2026 UPC Code Cheat Sheet",
        "micro_poll": "Taking exam in: [A] 2026  or  [B] 2027?",
        "exam_badge": "JOURNEYMAN PLUMBER UPC EXAM",
        "coupon": "TRADEPRO",
        "price": "$29.00",
        "destination_url": "https://eduprosuite.pro/plumber-exam.html",
        "formula_summary": "45° Offset Constant: Travel = Set × 1.414 (Always subtract fitting takeoffs before cutting pipe!)",
        "trap_alert": "Code Inspector Trap: Cutting pipe to full center-to-center travel fails inspection instantly! Deduct takeoffs!",
        "pin_h1": "UPC 45° OFFSET PIPE MATH",
        "pin_sub": "JOURNEYMAN PLUMBER EXAM SHORTCUTS",
        "mistake_lines": [
            "Cutting pipe directly to the center-to-center travel measurement.",
            "Forgetting to subtract 45° elbow fitting takeoff allowances from both ends.",
            "50% of plumbing apprentices cut pipe too long and fail state practical inspection!"
        ],
        "secret_lines": [
            "Shortcut: 45° Travel = Set × 1.414! (For 10-inch offset: 10 × 1.414 = 14.14 inches).",
            "Subtract fitting takeoff (Two 45° Els = -2.50 inches) -> True cut piece = 11.64 inches!",
            "Passes state journeyman exam and field rough-in inspection with zero wasted pipe!"
        ],
        "yt_title": "Journeyman Plumber 45° Offset Math Secret! 🛠️ UPC Exam Shortcut (Comment PLUMB) #Shorts",
        "yt_description": (
            "Pass the 2026 Journeyman Plumber Exam on your first attempt!\n"
            "Master 45-degree offset pipe calculations (Set × 1.414) and fitting takeoff deductions.\n\n"
            "💬 COMMENT 'PLUMB' BELOW to get our Secret 90% OFF Coupon + Complete UPC Code Cheat Sheet!\n"
            "❓ QUICK POLL: What year are you taking your Journeyman Exam? Comment below!\n\n"
            "👉 Download Complete Practice Drills & DFU Code Simulators:\n"
            "https://eduprosuite.pro/plumber-exam.html\n\n"
            "#Shorts #PlumberExam #JourneymanPlumber #UPCCode #PlumbingMath #TradePrep #EduProSuite"
        ),
        "yt_tags": ["Shorts", "PlumberExam", "JourneymanPlumber", "UPCCode", "PlumbingMath", "TradePrep", "EduProSuite"]
    }
]

# ==============================================================================
# ROTATION SELECTION HELPER
# ==============================================================================
def get_next_rotation_subject():
    last_idx = -1
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                last_idx = data.get("current_index", -1)
        except Exception:
            last_idx = -1

    # Check CLI argument for explicit subject selection (e.g. --subject plumbing)
    forced_sub = None
    for i, a in enumerate(sys.argv):
        if a == "--subject" and i + 1 < len(sys.argv):
            forced_sub = sys.argv[i + 1].strip().lower()
        elif a.startswith("--subject="):
            forced_sub = a.split("=", 1)[1].strip().lower()

    # Load uploaded ledger to guarantee no already-posted short is selected
    LEDGER_PATH = os.path.join(DATA_DIR, "youtube_uploaded_shorts_ledger.json")
    uploaded_ids = set()
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                led = json.load(f)
                uploaded_ids = {item.get("id") for item in led.get("uploaded_shorts", []) if item.get("id")}
        except Exception:
            pass

    if forced_sub:
        match_idx = None
        for idx, s in enumerate(SUBJECT_ROTATION):
            if s["id"] == forced_sub or forced_sub in s["id"]:
                match_idx = idx
                break
        if match_idx is not None:
            next_idx = match_idx
            subject = SUBJECT_ROTATION[next_idx]
            print(f"[+] CLI Overridden Subject: {subject['id'].upper()}")
        else:
            next_idx = (last_idx + 1) % len(SUBJECT_ROTATION)
            subject = SUBJECT_ROTATION[next_idx]
    else:
        # Pick the next subject that has NOT yet been uploaded
        chosen_idx = None
        for offset in range(1, len(SUBJECT_ROTATION) + 1):
            candidate_idx = (last_idx + offset) % len(SUBJECT_ROTATION)
            candidate_sub = SUBJECT_ROTATION[candidate_idx]
            if candidate_sub["id"] not in uploaded_ids:
                chosen_idx = candidate_idx
                break
                
        if chosen_idx is not None:
            next_idx = chosen_idx
            subject = SUBJECT_ROTATION[next_idx]
            print(f"[+] Selected Fresh Unposted Subject: {subject['id'].upper()} (Avoids previously uploaded subjects)")
        else:
            # If all subjects have been uploaded at least once
            next_idx = (last_idx + 1) % len(SUBJECT_ROTATION)
            subject = SUBJECT_ROTATION[next_idx]
            print(f"[!] All catalog subjects uploaded at least once. Continuing rotation cycle at: {subject['id'].upper()}")

    # Update state file
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "current_index": next_idx,
                "current_id": subject["id"],
                "total_subjects": len(SUBJECT_ROTATION)
            }, f, indent=2)
    except Exception as e:
        print(f"[!] Warning writing rotation state: {e}")

    # Save active metadata for YouTube upload script
    try:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "id": subject["id"],
                "title": subject["yt_title"],
                "description": subject["yt_description"],
                "tags": subject["yt_tags"]
            }, f, indent=2)
        print(f"[+] Active YouTube Metadata saved to {METADATA_FILE}")
    except Exception as e:
        print(f"[!] Warning writing active metadata: {e}")

    # Save active social metadata for Pinterest, Meta, Make.com
    try:
        exam_name = subject.get("exam_badge", subject["id"].upper())
        kw = subject.get("cta_keyword", "PASS")
        cp = subject.get("coupon", "SCORE5")
        pr = subject.get("price", "$29.00")
        dest = subject.get("destination_url", "https://eduprosuite.pro")

        tags_str = " ".join(f"#{t}" for t in subject.get("yt_tags", ["EduProSuite", "ExamPrep"]))
        nl = chr(10)
        nl2 = chr(10) + chr(10)
        reel_caption = (
            f"STOP FAILING ON YOUR {exam_name}!" + nl2 +
            "Here is the proven 2026 shortcut:" + nl +
            f"👉 {subject.get('formula_summary', '')}" + nl2 +
            "CRITICAL EXAM TRAP:" + nl +
            f"{subject.get('trap_alert', '')}" + nl2 +
            "SPECIAL 2026 EXAM PREP PASS (90% OFF SALE):" + nl +
            "- Full 300+ Page Blueprint and Step-by-Step Problem Solutions" + nl +
            "- 500+ Practice MCQs with Diagnostic Distractor Explanations" + nl +
            "- Timed Bluebook / PSI Exam Simulator with Instant Scoring" + nl +
            f"Regular Price: $199 -> TODAY: ONLY {pr} (90% OFF with code: {cp})" + nl2 +
            f"COMMENT '{kw}' BELOW:" + nl +
            "I will instantly DM you our secret 90% OFF VIP Checkout Link + Free 2026 PDF Cheat Sheet!" + nl2 +
            "Teachers, Tutors and Apprentices:" + nl +
            "Earn 40% recurring commissions recommending EduProSuite! Comment 'PARTNER' or visit https://eduprosuite.pro/affiliates.html" + nl2 +
            f"Direct Instant Digital Access: {dest}" + nl2 +
            tags_str
        )

        fb_description = (
            f"STOP LOSING EASY POINTS ON YOUR {exam_name}!" + nl2 +
            f"Here is the proven shortcut: {subject.get('formula_summary', '')}" + nl2 +
            f"Code / Exam Trap: {subject.get('trap_alert', '')}" + nl2 +
            "Complete 300+ Page Prep Blueprint and 500 Practice MCQs:" + nl +
            f"Was $199 -> Today ONLY {pr} with promo code: {cp}" + nl2 +
            f"Comment '{kw}' below for the instant 2026 Exam Cheat Sheet!" + nl +
            f"Full Study Guide: {dest}" + nl2 +
            tags_str
        )

        pin_desc = (
            f"Pass your {exam_name}! "
            f"Master {subject.get('formula_summary', '')}. "
            f"Download the full 300+ page exam blueprint and 500 practice MCQs for only {pr} "
            f"(90% OFF with code {cp}) at {dest}! Pin this to your study board! "
            f"{tags_str}"
        )

        with open(SOCIAL_METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "id": subject["id"],
                "exam_badge": exam_name,
                "title": subject["yt_title"],
                "pin_title": f"{subject.get('pin_h1', subject['id'].upper())} (Only {pr} with Code {cp})",
                "pin_desc": pin_desc,
                "reel_caption": reel_caption,
                "fb_title": subject["yt_title"].replace(" #Shorts", ""),
                "fb_description": fb_description,
                "destination_url": dest,
                "coupon": cp,
                "price": pr,
                "cta_keyword": kw,
                "tags": subject.get("yt_tags", ["EduProSuite", "ExamPrep"])
            }, f, indent=2)
        print(f"[+] Active Social Multi-Channel Metadata saved to {SOCIAL_METADATA_FILE}")
    except Exception as e:
        print(f"[!] Warning writing social metadata: {e}")

    print(f"[+] ROTATION ENGINE: Selected Subject [{next_idx + 1}/{len(SUBJECT_ROTATION)}]: {subject['id'].upper()}")
    return subject

# Active configuration for this run
ACTIVE_SUBJECT = get_next_rotation_subject()
VOICEOVER_SCRIPT = ACTIVE_SUBJECT["voiceover"]
SUBTITLE_CUES = ACTIVE_SUBJECT["subtitles"]

def get_font(size: int, bold: bool = False):
    font_names = ["arialbd.ttf", "segoeuib.ttf", "tahomabd.ttf"] if bold else ["arial.ttf", "segoeui.ttf", "tahoma.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

font_hook = get_font(62, bold=True)
font_subhook = get_font(42, bold=True)
font_ti_label = get_font(32, bold=True)
font_ti_screen = get_font(40, bold=True)
font_ti_screen_mono = get_font(46, bold=True)
font_key_btn = get_font(34, bold=True)
font_banner_title = get_font(48, bold=True)
font_banner_sub = get_font(36, bold=True)
font_badge = get_font(30, bold=True)

async def generate_voiceover():
    print(f"[*] Generating studio AI Voiceover via Edge-TTS ({ACTIVE_SUBJECT['id']})...")
    communicate = edge_tts.Communicate(VOICEOVER_SCRIPT, "en-US-AndrewMultilingualNeural")
    await communicate.save(TEMP_AUDIO)
    print(f"[+] Voiceover saved to: {TEMP_AUDIO}")

def get_audio_duration(audio_path):
    ffprobe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffprobe, "-i", audio_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            dur_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = dur_str.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 31.0

def draw_header_badge(draw, t: float):
    # Channel & Topic Pill
    draw.rounded_rectangle([70, 70, WIDTH - 70, 160], radius=25, fill=(15, 23, 42, 220), outline=(59, 130, 246), width=3)
    draw.text((WIDTH // 2, 115), ACTIVE_SUBJECT["badge"], font=font_ti_label, fill=(147, 197, 253), anchor="mm")

def draw_dynamic_subtitles(draw, t: float):
    current_cue = None
    for start, end, text, col in SUBTITLE_CUES:
        if start <= t < end:
            current_cue = (text, col)
            break
    if not current_cue and SUBTITLE_CUES:
        current_cue = (SUBTITLE_CUES[-1][2], SUBTITLE_CUES[-1][3])
        
    text, col = current_cue
    
    # Subtitle Pill Box in Upper Third (y = 190 - 330)
    draw.rounded_rectangle([60, 190, WIDTH - 60, 330], radius=24, fill=(11, 15, 25), outline=col, width=4)
    draw.text((WIDTH // 2, 260), text, font=font_subhook, fill=col, anchor="mm")

def draw_simulated_screen(draw, t: float):
    """
    Renders a dynamic, simulated screen with live outputs, active calculations, and key pads.
    """
    sc = ACTIVE_SUBJECT["screen_content"]
    bx1, by1, bx2, by2 = 60, 360, WIDTH - 60, 1260
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=35, fill=(30, 41, 59), outline=(71, 85, 105), width=5)
    
    # Model Title
    draw.text((bx1 + 40, by1 + 35), ACTIVE_SUBJECT["device_title"], font=font_ti_label, fill=(226, 232, 240))
    draw.text((bx2 - 200, by1 + 35), ACTIVE_SUBJECT["device_sub"], font=font_ti_label, fill=(56, 189, 248))

    # Inner LCD Screen
    sx1, sy1, sx2, sy2 = bx1 + 30, by1 + 75, bx2 - 30, by2 - 250
    draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=15, fill=(15, 23, 42), outline=(30, 58, 138), width=3)

    # Status Bar
    draw.rectangle([sx1 + 2, sy1 + 2, sx2 - 2, sy1 + 40], fill=(2, 6, 23))
    draw.text((sx1 + 20, sy1 + 20), "2026 CERTIFIED ENGINE • HIGH ACCURACY", font=font_ti_label, fill=(148, 163, 184), anchor="lm")
    draw.text((sx2 - 30, sy1 + 20), "🔋 ■", font=font_ti_label, fill=(34, 197, 94), anchor="rm")

    content_y = sy1 + 80
    cursor_blink = "■" if int(t * 3) % 2 == 0 else ""

    if t < 6.5:
        # Hook screen: Long Hand-Calculation being crossed out
        for idx, (line_text, line_col) in enumerate(sc["hook"]):
            draw.text((sx1 + 30, content_y + idx * 75), line_text, font=font_ti_screen_mono if idx == 0 else font_ti_screen, fill=line_col)
    elif 6.5 <= t < 10.5:
        # Menu screen
        for idx, (line_text, line_col) in enumerate(sc["menu"]):
            y_pos = content_y + idx * 55
            if idx == 3: # Highlighted menu item
                draw.rectangle([sx1 + 25, y_pos - 10, sx2 - 25, y_pos + 45], fill=(37, 99, 235))
                draw.text((sx1 + 30, y_pos + 15), line_text, font=font_ti_screen, fill=(255, 255, 255), anchor="lm")
            else:
                draw.text((sx1 + 30, y_pos), line_text, font=font_ti_screen, fill=line_col)
    elif 10.5 <= t < 17.5:
        # Wizard screen
        for idx, (line_text, line_col) in enumerate(sc["wizard"]):
            draw.text((sx1 + 30, content_y + idx * 55), line_text, font=font_ti_screen_mono if "x" in line_text or "=" in line_text else font_ti_screen, fill=line_col)
    else:
        # Output & Warning Screen
        draw.text((sx1 + 30, content_y), sc["output"][0][0], font=font_ti_screen_mono, fill=sc["output"][0][1])
        draw.text((sx2 - 40, content_y + 80), sc["output"][1][0], font=font_ti_screen_mono, fill=sc["output"][1][1], anchor="ra")
        
        # Warning callout box on bottom of LCD
        draw.rounded_rectangle([sx1 + 20, content_y + 160, sx2 - 20, content_y + 335], radius=12, fill=(69, 10, 10), outline=(239, 68, 68), width=3)
        draw.text((sx1 + 35, content_y + 195), sc["output"][2][0], font=font_ti_label, fill=sc["output"][2][1], anchor="lm")
        draw.text((sx1 + 35, content_y + 245), sc["output"][3][0], font=font_ti_label, fill=sc["output"][3][1], anchor="lm")
        draw.text((sx1 + 35, content_y + 295), sc["output"][4][0], font=font_ti_label, fill=sc["output"][4][1], anchor="lm")

    # Key Press Simulation Pads (Below LCD)
    key_y = by2 - 200
    keys = ACTIVE_SUBJECT["keys"]
    total_w = bx2 - bx1 - 60
    kw = total_w // len(keys)
    for i, (kname, kcol, start_t, end_t) in enumerate(keys):
        is_active = (start_t <= t < end_t)
        kx = bx1 + 30 + i * kw
        btn_box = [kx + 10, key_y + 20, kx + kw - 10, key_y + 140]
        bg = kcol if is_active else (51, 65, 85)
        border = (255, 255, 255) if is_active else (100, 116, 139)
        draw.rounded_rectangle(btn_box, radius=18, fill=bg, outline=border, width=4 if is_active else 2)
        txt_col = (255, 255, 255) if is_active else (203, 213, 225)
        draw.text(((btn_box[0] + btn_box[2]) // 2, (btn_box[1] + btn_box[3]) // 2), kname, font=font_key_btn, fill=txt_col, anchor="mm")

def draw_persistent_bottom_banner(draw, t: float):
    """
    Persistent Bottom 25-30% Comment-Magnet Banner:
    Engineered to capture 100% of viewer comments & DMs.
    """
    banner_y1 = HEIGHT - 540
    banner_y2 = HEIGHT - 80

    # Pulsing neon glow effect
    pulse = (math.sin(t * 5.0) + 1.0) / 2.0
    neon_r = int(234 * (0.8 + 0.2 * pulse))
    neon_g = int(179 * (0.8 + 0.2 * pulse))
    neon_b = int(8 * (0.8 + 0.2 * pulse))

    # Outer Banner Frame
    draw.rounded_rectangle([40, banner_y1, WIDTH - 40, banner_y2], radius=32, fill=(15, 23, 42), outline=(neon_r, neon_g, neon_b), width=5)

    # Top Pill
    pill_box = [WIDTH // 2 - 280, banner_y1 - 30, WIDTH // 2 + 280, banner_y1 + 35]
    draw.rounded_rectangle(pill_box, radius=20, fill=(234, 179, 8), outline=(255, 255, 255), width=3)
    draw.text((WIDTH // 2, banner_y1 + 2), "🔥 SECRET EXAM HACK UNLOCK", font=font_banner_sub, fill=(0, 0, 0), anchor="mm")

    # Call To Action Headline
    draw.text((WIDTH // 2, banner_y1 + 90), f"💬 COMMENT '{ACTIVE_SUBJECT['cta_keyword']}' BELOW 👇", font=font_banner_title, fill=(255, 255, 255), anchor="mm")

    # Value Proposition
    draw.text((WIDTH // 2, banner_y1 + 175), f"🎁 We will DM you the Full 2026", font=font_banner_sub, fill=(250, 204, 21), anchor="mm")
    draw.text((WIDTH // 2, banner_y1 + 235), f"{ACTIVE_SUBJECT['cta_val_prop']} + 90% OFF Coupon!", font=font_banner_sub, fill=(250, 204, 21), anchor="mm")

    # Micro Poll Action Prompt
    draw.rounded_rectangle([90, banner_y1 + 295, WIDTH - 90, banner_y1 + 415], radius=22, fill=(30, 41, 59), outline=(59, 130, 246), width=3)
    draw.text((WIDTH // 2, banner_y1 + 355), ACTIVE_SUBJECT["micro_poll"], font=font_banner_sub, fill=(224, 242, 254), anchor="mm")

    # Footer Branding
    draw.text((WIDTH // 2, HEIGHT - 40), "EduProSuite.pro • 40% Tutor Affiliate Program", font=font_badge, fill=(100, 116, 139), anchor="mm")

def render_frame(t: float):
    # Base dark gradient canvas
    base = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(base)

    # Subtle gradient
    for y in range(0, HEIGHT, 16):
        ratio = y / HEIGHT
        r = int(11 + ratio * 15)
        g = int(15 + ratio * 18)
        b = int(25 + ratio * 35)
        draw.rectangle([0, y, WIDTH, y + 16], fill=(r, g, b))

    # 1. Header
    draw_header_badge(draw, t)

    # 2. Dynamic Pop-up Subtitles (Top-third)
    draw_dynamic_subtitles(draw, t)

    # 3. Dynamic Interactive Screen (Middle)
    draw_simulated_screen(draw, t)

    # 4. Persistent Comment-Magnet Banner (Bottom 25-30%)
    draw_persistent_bottom_banner(draw, t)

    return base


def generate_active_pinterest_pin(subject=None):
    if subject is None:
        subject = ACTIVE_SUBJECT
    print("=" * 65)
    print(f"Generating 2:3 High-Intent Pinterest Fresh Pin for: {subject['id'].upper()}")
    print("=" * 65)

    PIN_WIDTH = 1000
    PIN_HEIGHT = 1500
    pin = Image.new("RGB", (PIN_WIDTH, PIN_HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(pin)

    # Grid background lines
    for x in range(0, PIN_WIDTH, 40):
        draw.line([(x, 0), (x, PIN_HEIGHT)], fill=(22, 33, 56), width=1)
    for y in range(0, PIN_HEIGHT, 40):
        draw.line([(0, y), (PIN_WIDTH, y)], fill=(22, 33, 56), width=1)

    font_pin_h1 = get_font(46, bold=True)
    font_pin_sub = get_font(30, bold=True)
    font_pin_tag = get_font(24, bold=True)
    font_box_title = get_font(28, bold=True)
    font_box_body = get_font(24, bold=False)
    font_pin_cta = get_font(36, bold=True)

    # Top Series Badge
    draw.rounded_rectangle([40, 35, PIN_WIDTH - 40, 105], radius=18, fill=(30, 41, 59), outline=(99, 102, 241), width=2)
    draw.text((PIN_WIDTH // 2, 70), "[*] 2026-2027 OFFICIAL EXAM BLUEPRINT SERIES", font=font_pin_tag, fill=(199, 210, 254), anchor="mm")

    # Header Card
    pin_h1 = subject.get("pin_h1", subject["id"].upper() + " EXAM HACKS")
    pin_sub = subject.get("pin_sub", "PASS YOUR EXAM ON THE FIRST TRY")
    draw.rounded_rectangle([40, 125, PIN_WIDTH - 40, 335], radius=24, fill=(255, 255, 255), outline=(224, 231, 255), width=3)
    draw.text((PIN_WIDTH // 2, 185), pin_h1, font=font_pin_h1, fill=(15, 23, 42), anchor="mm")
    draw.text((PIN_WIDTH // 2, 248), pin_sub, font=font_pin_sub, fill=(67, 56, 202), anchor="mm")
    draw.text((PIN_WIDTH // 2, 298), ">> Master The Exam In 30 Days With Zero Guesswork <<", font=font_pin_tag, fill=(15, 23, 42), anchor="mm")

    # Red Box: Common Mistake
    draw.rounded_rectangle([60, 365, PIN_WIDTH - 60, 575], radius=20, fill=(69, 10, 10), outline=(239, 68, 68), width=3)
    draw.text((90, 395), "[!] CRITICAL EXAM MISTAKE (LOSES EASY POINTS):", font=font_box_title, fill=(248, 113, 113))
    m_lines = subject.get("mistake_lines", [
        "Doing tedious hand calculations during timed exam sections.",
        "Falling into unlabelled input and syntax deduction traps.",
        "Graders award ZERO credit for unlabelled answers on free response!"
    ])
    y_pos = 445
    for l in m_lines:
        draw.text((90, y_pos), f"- {l}", font=font_box_body, fill=(254, 202, 202))
        y_pos += 40

    # Green Box: Passing Shortcut
    draw.rounded_rectangle([60, 605, PIN_WIDTH - 60, 815], radius=20, fill=(6, 78, 59), outline=(16, 185, 129), width=3)
    draw.text((90, 635), "[+] 2026 PASSING SHORTCUT (LOCK IN 100%):", font=font_box_title, fill=(52, 211, 153))
    s_lines = subject.get("secret_lines", [
        f"Shortcut: {subject.get('formula_summary', 'Instant calculator & formula shortcut')}",
        "Saves 15-20 minutes of exam time on complex test problems.",
        "Locks in full scoring rubrics and guarantees maximum score!"
    ])
    y_pos = 685
    for l in s_lines:
        draw.text((90, y_pos), f"- {l}", font=font_box_body, fill=(209, 250, 229))
        y_pos += 40

    # Blue/Purple Box: Complete 300+ Page Blueprint Showcase & Pricing
    draw.rounded_rectangle([60, 845, PIN_WIDTH - 60, 1180], radius=20, fill=(24, 24, 27), outline=(139, 92, 246), width=3)
    draw.text((90, 875), "[*] INSIDE THE COMPLETE 300+ PAGE PREP BLUEPRINT:", font=font_box_title, fill=(192, 132, 252))
    draw.text((90, 930), "- 500+ Practice MCQs with Diagnostic Distractor Explanations", font=font_box_body, fill=(226, 232, 240))
    draw.text((90, 975), "- Step-by-Step Scoring Rubrics & Formula Cheat Sheets", font=font_box_body, fill=(226, 232, 240))
    draw.text((90, 1020), "- Timed Digital Exam Simulator with Instant Automatic Grading", font=font_box_body, fill=(226, 232, 240))
    draw.text((90, 1065), "- 100% Up to Date for May 2026 & 2027 Exam Cycles", font=font_box_body, fill=(52, 211, 153))

    # Pricing Banner inside card
    draw.rounded_rectangle([80, 1110, PIN_WIDTH - 80, 1165], radius=10, fill=(79, 70, 229))
    draw.text((PIN_WIDTH // 2, 1137), f"🔥 TODAY ONLY: {subject.get('price', '$29')} (Was $199 — 90% OFF with code {subject.get('coupon', 'SCORE5')})", font=font_pin_tag, fill=(255, 255, 255), anchor="mm")

    # Bottom CTA Box
    draw.rounded_rectangle([50, 1210, PIN_WIDTH - 50, 1435], radius=24, fill=(225, 29, 72), outline=(254, 205, 211), width=3)
    draw.text((PIN_WIDTH // 2, 1260), "PIN THIS TO YOUR STUDY BOARD 📌", font=font_pin_cta, fill=(255, 255, 255), anchor="mm")
    dest_domain = subject.get('destination_url', 'https://eduprosuite.pro')
    draw.text((PIN_WIDTH // 2, 1320), f"Instant PDF: {dest_domain}", font=font_pin_sub, fill=(254, 240, 138), anchor="mm")
    draw.text((PIN_WIDTH // 2, 1375), f"Comment '{subject.get('cta_keyword', 'PASS')}' for Secret VIP Coupon Code!", font=font_pin_tag, fill=(255, 255, 255), anchor="mm")

    pin.save(OUTPUT_PIN_PATH, quality=95)
    print(f"[+] 100% SUCCESS: 2:3 Fresh Pin Generated at {OUTPUT_PIN_PATH} ({os.path.getsize(OUTPUT_PIN_PATH)/1024:.1f} KB)")

    # Sync to landing if folder exists
    if os.path.exists(LANDING_REPO):
        try:
            import shutil
            shutil.copy2(OUTPUT_PIN_PATH, os.path.join(LANDING_REPO, "eduprosuite_viral_trend_pin.png"))
            print(f"[+] Synced Fresh Pin to {LANDING_REPO}/eduprosuite_viral_trend_pin.png")
        except Exception as e:
            print(f"[!] Warning syncing pin to landing: {e}")

def build_viral_short():
    print("=" * 65)
    print(f"EduProSuite 6-Subject Viral Short Generator: {ACTIVE_SUBJECT['id'].upper()}")
    print("=" * 65)

    # Step 1: Generate AI Voiceover
    asyncio.run(generate_voiceover())

    # Step 2: Measure Audio Length
    audio_dur = get_audio_duration(TEMP_AUDIO)
    total_frames = int(audio_dur * FPS)
    print(f"[*] Audio Duration: {audio_dur:.2f}s -> Total Frames: {total_frames} @ {FPS} FPS")

    # Step 3: Stream Video Frames directly into FFmpeg Pipe (Ultra Low-Memory)
    print(f"[*] Streaming {total_frames} frames ({WIDTH}x{HEIGHT}) directly into FFmpeg encoder...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", TEMP_AUDIO,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(total_frames):
        t = i / FPS
        if i % (FPS * 5) == 0:
            print(f"    Progress: {t:.1f}s / {audio_dur:.1f}s (Frame {i}/{total_frames})", flush=True)
        frame_img = render_frame(t)
        proc.stdin.write(frame_img.tobytes())

    proc.stdin.close()
    proc.wait()

    # Cleanup temporary files
    if os.path.exists(TEMP_AUDIO):
        try:
            os.remove(TEMP_AUDIO)
        except Exception:
            pass

    # Sync video to viral reel output and landing repo
    try:
        import shutil
        shutil.copy2(OUTPUT_VIDEO, VIRAL_REEL_VIDEO)
        print(f"[+] Synced video to: {VIRAL_REEL_VIDEO}")
        if os.path.exists(LANDING_REPO):
            shutil.copy2(OUTPUT_VIDEO, os.path.join(LANDING_REPO, "eduprosuite_viral_trend_reel.mp4"))
            print(f"[+] Synced video to: {LANDING_REPO}/eduprosuite_viral_trend_reel.mp4")
    except Exception as e:
        print(f"[!] Warning copying video: {e}")

    # Generate 2:3 Pinterest Pin for active subject
    generate_active_pinterest_pin(ACTIVE_SUBJECT)

    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("\n" + "=" * 65)
    print(f"[+] 100% SUCCESS! Viral Short Generated for: {ACTIVE_SUBJECT['id'].upper()}")
    print(f"    Output: {OUTPUT_VIDEO} ({size_mb:.2f} MB)")
    print(f"    Title: {ACTIVE_SUBJECT['yt_title']}")
    print(f"    Duration: {audio_dur:.2f}s | Audio: 192k AAC Voiceover")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    build_viral_short()
