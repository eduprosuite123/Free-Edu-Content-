#!/usr/bin/env python3
"""
Digital SAT Math Desmos Masterclass - Full-Length Headless Video Engine (2026 Edition)
=====================================================================================
Renders full-length publication-grade 1080p educational masterclass video featuring
all 10 Digital SAT Math Modules using:
- User-Approved Authentic Cloned Voiceover (via scripts/cloned_voice_engine.py)
- High-Contrast Cyber STEM Desmos Simulation Graphs (1920x1080 Full HD)
- Frame-accurate FFmpeg assembly with exact dynamic chapter timestamps
- Zero Local Load: 100% headless execution in GitHub Actions or cloud runner.
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
import numpy as np

# Ensure console supports UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
CURRICULUM_PATH = ROOT_DIR / "data" / "sat_desmos_masterclass_curriculum.json"
OUTPUT_DIR = ROOT_DIR / "output" / "sat_masterclass"
FINAL_VIDEO_PATH = ROOT_DIR / "output" / "sat_desmos_masterclass_30min.mp4"

# Color Palette (High-Contrast Cyber STEM Dark Theme)
BG_COLOR = (11, 15, 25)           # Deep Space Navy (#0B0F19)
CARD_BG = (22, 30, 46)            # Slate Card (#161E2E)
ACCENT_CYAN = (56, 189, 248)       # Electric Cyan (#38BDF8)
ACCENT_GREEN = (52, 211, 153)      # Emerald Success (#34D399)
ACCENT_GOLD = (251, 191, 36)       # Amber Gold (#FBBF24)
ACCENT_RED = (248, 113, 113)       # Coral Warning (#F87171)
TEXT_WHITE = (248, 250, 252)       # Clean White (#F8FAFC)
TEXT_MUTED = (148, 163, 184)       # Muted Slate (#94A3B8)
BORDER_COLOR = (51, 65, 85)        # Border (#334155)

def get_font(size=20, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def get_audio_duration(audio_file: Path) -> float:
    """Extract exact audio duration using ffprobe or fallback byte rate."""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        # Robust MP3 bitrate duration approximation (128 kbps ~ 16,000 bytes/sec)
        try:
            sz = os.path.getsize(str(audio_file))
            return max(round(sz / 16000.0, 1), 20.0)
        except Exception:
            return 60.0

def generate_voiceover(module: dict, output_audio: Path) -> Path:
    """Generate authentic user cloned voiceover using cloned_voice_engine."""
    m_id = module['module_id']
    title = module['title']
    problem = module['problem_statement']
    trap = module['algebra_trap']
    cheat_code = module['desmos_cheat_code']
    pro_tip = module['pro_tip']

    # Comprehensive educational script (approx 120-160 words per module)
    script = (
        f"Welcome to Module {m_id} of the Digital SAT Math Desmos Masterclass. {title}. "
        f"Let us examine this classic College Board problem: {problem}. "
        f"Here is why students lose precious time: {trap} "
        f"Now, let us deploy the Desmos ten second cheat code. Look at the Desmos interface on your right. "
        f"{cheat_code} "
        f"Notice how Desmos instantly pinpoints the key coordinates without factoring or algebraic expansion. "
        f"Keep this golden exam pro tip in mind for test day: {pro_tip} "
        f"Practice this technique, and let us move to the next high-yield module."
    )

    try:
        # Import local cloned voice engine
        from cloned_voice_engine import synthesize_user_cloned_voice
        print(f"  [+] Synthesizing authentic voiceover for Module {m_id} via cloned_voice_engine...")
        synthesize_user_cloned_voice(script, output_audio)
    except Exception as e:
        print(f"  [!] Primary cloned voice engine import error ({e}). Engaging direct Edge-TTS fallback...")
        import edge_tts
        async def _run_tts():
            comm = edge_tts.Communicate(script, "en-IN-PrabhatNeural", rate="-2%", pitch="+1Hz")
            await comm.save(str(output_audio))
        asyncio.run(_run_tts())

    return output_audio

def generate_desmos_graph(module: dict, output_path: Path):
    """Render high-resolution dark-mode simulated Desmos graph using Matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=100)
    fig.patch.set_facecolor('#0B101E')
    ax.set_facecolor('#131B2E')

    ax.grid(True, which='both', color='#24314E', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.axhline(0, color='#64748B', linewidth=1.2)
    ax.axvline(0, color='#64748B', linewidth=1.2)
    ax.tick_params(colors='#94A3B8', labelsize=11)
    for spine in ax.spines.values():
        spine.set_color('#334155')

    m_id = module['module_id']

    if m_id == 1:
        x = np.linspace(-2, 6, 200)
        y1 = (16 - 3*x)/2
        y2 = 5*x - 9
        ax.plot(x, y1, color='#38BDF8', linewidth=3, label='3x + 2y = 16')
        ax.plot(x, y2, color='#F43F5E', linewidth=3, label='5x - y = 9')
        ax.scatter([2], [5], color='#34D399', s=160, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate('(2, 5)\nIntersection', (2, 5), textcoords="offset points", xytext=(15, 10),
                    fontsize=12, fontweight='bold', color='#34D399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#34D399", lw=1.5))
        ax.set_xlim(-1, 5)
        ax.set_ylim(-2, 10)

    elif m_id == 2:
        t = np.linspace(-0.5, 5.5, 200)
        h = -16*t**2 + 64*t + 80
        ax.plot(t, h, color='#38BDF8', linewidth=3, label='y = -16x^2 + 64x + 80')
        ax.scatter([2], [144], color='#FBBF24', s=180, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate('Vertex: (2, 144)\nMax Height = 144 ft', (2, 144), textcoords="offset points", xytext=(-50, 15),
                    fontsize=12, fontweight='bold', color='#FBBF24',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#FBBF24", lw=1.5))
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(0, 160)

    elif m_id == 3:
        x_pts = np.array([1, 2, 3])
        y_pts = np.array([5, 11, 19])
        x = np.linspace(0, 4, 200)
        y = x**2 + 3*x + 1
        ax.plot(x, y, color='#A855F7', linewidth=3, label='y1 ~ ax1^2 + bx1 + c')
        ax.scatter(x_pts, y_pts, color='#34D399', s=150, zorder=5, edgecolors='white', linewidth=2)
        for xp, yp in zip(x_pts, y_pts):
            ax.annotate(f"({xp}, {yp})", (xp, yp), textcoords="offset points", xytext=(10, -5),
                        fontsize=11, color='#F8FAFC', fontweight='bold')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 25)

    elif m_id == 4:
        x = np.linspace(-2, 6, 200)
        y1 = (12 - 4*x)/6
        y2 = (7 - 2*x)/3
        ax.plot(x, y1, color='#38BDF8', linewidth=3, label='4x + 6y = 12')
        ax.plot(x, y2, color='#F59E0B', linewidth=3, linestyle='--', label='2x + ky = 7 (k=3)')
        ax.annotate('NO SOLUTION\n(Parallel Lines)', (1.5, 1.8),
                    fontsize=12, fontweight='bold', color='#F87171',
                    bbox=dict(boxstyle="round,pad=0.5", fc="#0F172A", ec="#F87171", lw=1.5))
        ax.set_xlim(-1, 5)
        ax.set_ylim(-2, 5)

    elif m_id == 5:
        theta = np.linspace(0, 2*np.pi, 200)
        xc = 3 + 7*np.cos(theta)
        yc = -4 + 7*np.sin(theta)
        ax.plot(xc, yc, color='#06B6D4', linewidth=3.5, label='x^2-6x+y^2+8y=24')
        ax.scatter([3], [-4], color='#FBBF24', s=140, zorder=5, edgecolors='white', linewidth=2)
        ax.plot([3, 10], [-4, -4], color='#34D399', linewidth=2.5, linestyle=':')
        ax.annotate('Center (3, -4)', (3, -4), textcoords="offset points", xytext=(-40, -20),
                    fontsize=11, fontweight='bold', color='#FBBF24')
        ax.annotate('Radius = 7', (6.5, -3.5), fontsize=12, fontweight='bold', color='#34D399')
        ax.set_aspect('equal')
        ax.set_xlim(-6, 12)
        ax.set_ylim(-13, 5)

    elif m_id == 6:
        x = np.linspace(-4, 6, 200)
        y = 2*x - 3
        y_bound = -x + 5
        ax.plot(x, y, color='#38BDF8', linewidth=3, label='y >= 2x - 3')
        ax.plot(x, y_bound, color='#F43F5E', linewidth=3, linestyle='--', label='y < -x + 5')
        ax.fill_between(x, y, y_bound, where=(y_bound > y), color='#38BDF8', alpha=0.25)
        ax.scatter([2], [2], color='#34D399', s=160, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate('Feasible (2, 2)', (2, 2), textcoords="offset points", xytext=(12, 12),
                    fontsize=12, fontweight='bold', color='#34D399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#34D399", lw=1.5))
        ax.set_xlim(-1, 5)
        ax.set_ylim(-3, 7)

    elif m_id == 7:
        x = np.linspace(0, 6, 200)
        y = 3*x**2 - 5*x + 4
        ax.plot(x, y, color='#38BDF8', linewidth=3, label='f(x) = 3x^2 - 5x + 4')
        ax.scatter([3, 5], [16, 54], color='#FBBF24', s=150, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate('f(3)=16', (3, 16), textcoords="offset points", xytext=(-35, 10), fontsize=11, fontweight='bold', color='#FBBF24')
        ax.annotate('f(5)=54', (5, 54), textcoords="offset points", xytext=(-35, 10), fontsize=11, fontweight='bold', color='#FBBF24')
        ax.annotate('f(5) - f(3) = 38', (4, 30), fontsize=12, fontweight='bold', color='#34D399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#34D399", lw=1.5))
        ax.set_xlim(1, 6)
        ax.set_ylim(0, 60)

    elif m_id == 8:
        t = np.linspace(0, 12, 200)
        p = 500 * (1.15)**(t/3)
        ax.plot(t, p, color='#34D399', linewidth=3, label='P(t) = 500(1.15)^(t/3)')
        ax.scatter([3, 6], [575, 661], color='#38BDF8', s=140, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate('t=3 -> 575', (3, 575), textcoords="offset points", xytext=(-20, 15), fontsize=11, fontweight='bold', color='#38BDF8')
        ax.annotate('t=6 -> 661', (6, 661), textcoords="offset points", xytext=(-20, 15), fontsize=11, fontweight='bold', color='#38BDF8')
        ax.set_xlim(0, 12)
        ax.set_ylim(400, 1000)

    elif m_id == 9:
        data = [14, 18, 22, 22, 25, 29, 31, 35, 42]
        ax.boxplot(data, vert=False, patch_artist=True,
                   boxprops=dict(facecolor='#38BDF8', color='white', linewidth=2),
                   medianprops=dict(color='#FBBF24', linewidth=3),
                   whiskerprops=dict(color='#94A3B8', linewidth=2),
                   capprops=dict(color='#94A3B8', linewidth=2))
        ax.set_yticks([])
        ax.set_xlabel('Values', color='#94A3B8', fontsize=12)
        ax.annotate('Median=25', (25, 1.15), fontsize=11, fontweight='bold', color='#FBBF24')
        ax.annotate('Q1=20', (20, 1.15), fontsize=11, fontweight='bold', color='#38BDF8')
        ax.annotate('Q3=33', (33, 1.15), fontsize=11, fontweight='bold', color='#38BDF8')
        ax.annotate('IQR = Q3 - Q1 = 13', (23, 0.75), fontsize=12, fontweight='bold', color='#34D399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#34D399", lw=1.5))
        ax.set_xlim(10, 45)

    else:
        # Module 10: Right Triangle Trig
        ax.plot([0, 12, 12, 0], [0, 0, 5, 0], color='#38BDF8', linewidth=3.5, label='Right Triangle (5-12-13)')
        ax.scatter([0, 12, 12], [0, 0, 5], color='#FBBF24', s=140, zorder=5)
        ax.annotate('Angle A', (1.5, 0.4), fontsize=11, fontweight='bold', color='#34D399')
        ax.annotate('Opposite = 5', (12.3, 2.5), fontsize=11, fontweight='bold', color='#F8FAFC')
        ax.annotate('Adjacent = 12', (5.5, -0.6), fontsize=11, fontweight='bold', color='#F8FAFC')
        ax.annotate('Hypotenuse = 13', (5, 3), fontsize=11, fontweight='bold', color='#38BDF8')
        ax.annotate('sin(A) = 5/13 = cos(90 - A)', (2, 4.5), fontsize=12, fontweight='bold', color='#34D399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#34D399", lw=1.5))
        ax.set_aspect('equal')
        ax.set_xlim(-1, 15)
        ax.set_ylim(-1, 6)

    ax.legend(loc='upper right', facecolor='#0B0F19', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=10)
    plt.tight_layout()
    plt.savefig(str(output_path), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

def create_masterclass_slide(module: dict, graph_img_path: Path, output_path: Path, current_timestamp: str):
    """Assemble 1920x1080 masterclass tutorial slide."""
    img = Image.new('RGB', (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_badge = get_font(16, bold=True)
    f_header = get_font(20, bold=True)
    f_body = get_font(18, bold=False)
    f_code = get_font(18, bold=True)

    # Top Header Bar
    draw.rectangle([(40, 25), (1880, 85)], fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((60, 42), "DIGITAL SAT MATH 2025/2026", fill=ACCENT_CYAN, font=f_badge)
    draw.text((380, 42), "|  OFFICIAL DESMOS CHEAT CODE MASTERCLASS  |", fill=TEXT_MUTED, font=f_badge)
    draw.text((880, 40), f"MODULE {module['module_id']}/10: {module['title'][:55]}", fill=TEXT_WHITE, font=f_header)
    draw.text((1680, 42), f"TIME: {current_timestamp}", fill=ACCENT_GOLD, font=f_badge)

    left_w = 840

    # 1. Question Box
    draw.rounded_rectangle([(40, 105), (40 + left_w, 320)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((65, 125), "COLLEGE BOARD OFFICIAL QUESTION ARCHETYPE", fill=ACCENT_GOLD, font=f_badge)
    
    stmt = module['problem_statement']
    words = stmt.split()
    lines = []
    cur_line = ""
    for w in words:
        if len(cur_line + " " + w) < 55:
            cur_line += " " + w
        else:
            lines.append(cur_line.strip())
            cur_line = w
    if cur_line:
        lines.append(cur_line.strip())
    
    y_q = 160
    for l in lines[:4]:
        draw.text((65, y_q), l, fill=TEXT_WHITE, font=f_header)
        y_q += 32

    # 2. Algebra Trap Box
    draw.rounded_rectangle([(40, 340), (40 + left_w, 510)], radius=12, fill=(35, 20, 25), outline=(120, 40, 50), width=1)
    draw.text((65, 360), "❌ THE SLOW ALGEBRA TRAP (Manual Method: 90 - 120s)", fill=ACCENT_RED, font=f_badge)
    trap = module['algebra_trap']
    t_lines = [trap[i:i+60] for i in range(0, min(len(trap), 180), 60)]
    y_t = 395
    for tl in t_lines[:3]:
        draw.text((65, y_t), tl, fill=(254, 202, 202), font=f_body)
        y_t += 28

    # 3. Desmos Cheat Code Box
    draw.rounded_rectangle([(40, 530), (40 + left_w, 790)], radius=12, fill=(18, 38, 32), outline=ACCENT_GREEN, width=2)
    draw.text((65, 550), "⚡ DESMOS 10-SECOND CHEAT CODE (Score 800 Fast)", fill=ACCENT_GREEN, font=f_badge)
    code_desc = module['desmos_cheat_code']
    c_lines = [code_desc[i:i+58] for i in range(0, min(len(code_desc), 240), 58)]
    y_c = 585
    for cl in c_lines[:4]:
        draw.text((65, y_c), cl, fill=TEXT_WHITE, font=f_body)
        y_c += 28

    draw.rounded_rectangle([(65, 710), (40 + left_w - 25, 770)], radius=8, fill=(10, 22, 18), outline=(34, 197, 94), width=1)
    eq_display = "  |  ".join(module['desmos_equations'])[:60]
    draw.text((80, 725), f"Desmos Input:  {eq_display}", fill=ACCENT_GREEN, font=f_code)

    # 4. Pro Tip Box
    draw.rounded_rectangle([(40, 810), (40 + left_w, 970)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((65, 830), "💡 EXAM PRO-TIP & COMMON TRAP AVOIDANCE", fill=ACCENT_CYAN, font=f_badge)
    ptip = module['pro_tip']
    p_lines = [ptip[i:i+60] for i in range(0, min(len(ptip), 180), 60)]
    y_p = 865
    for pl in p_lines[:3]:
        draw.text((65, y_p), pl, fill=TEXT_MUTED, font=f_body)
        y_p += 28

    # Right Panel: Desmos Window
    right_x = 910
    right_w = 970
    draw.rounded_rectangle([(right_x, 105), (right_x + right_w, 970)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.rectangle([(right_x, 105), (right_x + right_w, 155)], fill=(15, 23, 42))
    draw.text((right_x + 25, 122), "DESMOS GRAPHING CALCULATOR (OFFICIAL DIGITAL SAT)", fill=TEXT_WHITE, font=f_badge)
    draw.ellipse([(right_x + right_w - 70, 125), (right_x + right_w - 56, 139)], fill=(239, 68, 68))
    draw.ellipse([(right_x + right_w - 48, 125), (right_x + right_w - 34, 139)], fill=(234, 179, 8))
    draw.ellipse([(right_x + right_w - 26, 125), (right_x + right_w - 12, 139)], fill=(34, 197, 94))

    if graph_img_path.exists():
        graph = Image.open(graph_img_path).resize((right_w - 20, 790))
        img.paste(graph, (right_x + 10, 165))

    # Bottom Footer Bar
    draw.rectangle([(40, 995), (1880, 1055)], fill=CARD_BG, outline=BORDER_COLOR, width=1)
    progress_w = int((module['module_id'] / 10.0) * 800)
    draw.rectangle([(60, 1020), (60 + progress_w, 1030)], fill=ACCENT_CYAN)
    draw.rectangle([(60, 1020), (860, 1030)], outline=BORDER_COLOR, width=1)
    draw.text((880, 1015), f"Masterclass Progress: {module['module_id']*10}%", fill=TEXT_MUTED, font=f_badge)
    draw.text((1500, 1015), "EduProSuite SAT Prep Suite  •  eduprosuite.pro", fill=ACCENT_GOLD, font=f_badge)

    img.save(str(output_path), quality=95)

def format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def render_module_video(slide_path: Path, audio_path: Path, output_mp4: Path, duration: float):
    """Render single module video using high-performance FFmpeg still-image looping."""
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(slide_path),
        "-i", str(audio_path),
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-pix_fmt", "yuv420p",
        "-t", str(duration + 1.0), # Audio duration + 1s tail buffer
        "-shortest",
        str(output_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def concatenate_module_videos(module_video_paths: list, final_output: Path):
    """Concatenate all module videos into single full-length masterclass video using FFmpeg demuxer."""
    concat_list_path = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for vp in module_video_paths:
            f.write(f"file '{vp.resolve().as_posix()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(final_output)
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Final Full-Length Masterclass Concatenated: {final_output}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Full-Length SAT Desmos Masterclass Generator")
    parser.add_argument("--test-clip", action="store_true", help="Render Module 1 only for fast verification")
    parser.add_argument("--dry-run", action="store_true", help="Generate slides and voiceover only, without FFmpeg concat")
    parser.add_argument("--full", action="store_true", help="Compile full 10-module masterclass")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_VIDEO_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
        curriculum_data = json.load(f)

    modules = curriculum_data['modules']
    if args.test_clip:
        modules = modules[:1]
        print("[TEST MODE] Rendering Module 1 only...")

    cumulative_seconds = 0.0
    updated_modules = []
    module_video_paths = []

    print("=" * 65)
    print(f"DIGITAL SAT DESMOS MASTERCLASS ENGINE (10 Modules)")
    print("=" * 65)

    for mod in modules:
        m_id = mod['module_id']
        current_ts = format_timestamp(cumulative_seconds)
        mod['timestamp'] = current_ts

        print(f"\n[*] Processing Module {m_id}/10: {mod['title']}")
        print(f"    Timestamp: {current_ts}")

        graph_path = OUTPUT_DIR / f"graph_module_{m_id}.png"
        slide_path = OUTPUT_DIR / f"slide_module_{m_id}.png"
        audio_path = OUTPUT_DIR / f"audio_module_{m_id}.mp3"
        module_mp4 = OUTPUT_DIR / f"segment_module_{m_id}.mp4"

        # 1. Render Graphic & Slide
        generate_desmos_graph(mod, graph_path)
        create_masterclass_slide(mod, graph_path, slide_path, current_ts)

        # 2. Render Authentic Voiceover
        generate_voiceover(mod, audio_path)
        duration = get_audio_duration(audio_path)
        print(f"    Voiceover Duration: {duration:.2f} seconds")

        cumulative_seconds += duration + 1.0
        updated_modules.append(mod)

        # 3. Render Module Video Clip
        if not args.dry_run:
            print(f"    Rendering Segment MP4 (Duration: {duration + 1.0:.1f}s)...")
            render_module_video(slide_path, audio_path, module_mp4, duration)
            module_video_paths.append(module_mp4)

    # Update Curriculum with exact dynamic chapter timestamps
    curriculum_data['modules'] = updated_modules
    curriculum_data['total_duration_seconds'] = cumulative_seconds
    with open(CURRICULUM_PATH, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, indent=2)
    print(f"\n[+] Curriculum updated with exact dynamic timestamps. Total Duration: {format_timestamp(cumulative_seconds)} ({cumulative_seconds:.1f}s)")

    # 4. Concatenate Final Masterclass Video
    if not args.dry_run:
        target_video = OUTPUT_DIR / "test_module_1.mp4" if args.test_clip else FINAL_VIDEO_PATH
        if len(module_video_paths) == 1:
            import shutil
            shutil.copy2(module_video_paths[0], target_video)
        else:
            concatenate_module_videos(module_video_paths, target_video)

        final_size = target_video.stat().st_size / (1024 * 1024)
        print("=" * 65)
        print(f"🎉 MASTERCLASS VIDEO READY: {target_video} ({final_size:.2f} MB)")
        print(f"Total Video Runtime: {format_timestamp(cumulative_seconds)}")
        print("=" * 65)

if __name__ == "__main__":
    main()
