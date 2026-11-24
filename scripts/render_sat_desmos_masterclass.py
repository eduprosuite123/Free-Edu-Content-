#!/usr/bin/env python3
"""
Digital SAT Math Desmos 30-Minute Masterclass - Headless Video Engine
Generates 1080p full HD tutorial slides, Desmos simulation graphs, audio, and MP4 video.
Designed for 100% automated execution in GitHub Actions or headless cloud environments.
"""

import os
import sys
import json
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

CURRICULUM_PATH = os.path.join("data", "sat_desmos_masterclass_curriculum.json")
OUTPUT_DIR = os.path.join("output", "sat_masterclass")
FINAL_VIDEO_PATH = os.path.join("output", "sat_desmos_masterclass_30min.mp4")

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
    """Fallback font loader for Windows & Linux headless."""
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

def generate_desmos_graph(module, output_path):
    """Render high-resolution dark-mode simulated Desmos graph using Matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=100)
    fig.patch.set_facecolor('#0B101E')
    ax.set_facecolor('#131B2E')

    # Grid styling
    ax.grid(True, which='both', color='#24314E', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.axhline(0, color='#64748B', linewidth=1.2)
    ax.axvline(0, color='#64748B', linewidth=1.2)
    ax.tick_params(colors='#94A3B8', labelsize=11)
    for spine in ax.spines.values():
        spine.set_color('#334155')

    m_id = module['module_id']

    if m_id == 1:
        # 3x + 2y = 16 -> y = (16 - 3x)/2
        # 5x - y = 9  -> y = 5x - 9
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
        # h(t) = -16t^2 + 64t + 80
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
        # Regression y = x^2 + 3x + 1
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
        # Parallel lines 4x + 6y = 12 & 2x + 3y = 7
        x = np.linspace(-2, 6, 200)
        y1 = (12 - 4*x)/6
        y2 = (7 - 2*x)/3
        ax.plot(x, y1, color='#38BDF8', linewidth=3, label='4x + 6y = 12')
        ax.plot(x, y2, color='#F59E0B', linewidth=3, linestyle='--', label='2x + ky = 7 (k=3)')
        ax.annotate('NO SOLUTION\n(Slopes Equal, Parallel)', (1.5, 1.8),
                    fontsize=12, fontweight='bold', color='#F87171',
                    bbox=dict(boxstyle="round,pad=0.5", fc="#0F172A", ec="#F87171", lw=1.5))
        ax.set_xlim(-1, 5)
        ax.set_ylim(-2, 5)

    elif m_id == 5:
        # Circle (x-3)^2 + (y+4)^2 = 49 (r=7, center=(3, -4))
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

    else:
        # Default high-impact graph
        x = np.linspace(-4, 6, 200)
        y = 2*x - 3
        y_bound = -x + 5
        ax.plot(x, y, color='#38BDF8', linewidth=3, label='y >= 2x - 3')
        ax.plot(x, y_bound, color='#F43F5E', linewidth=3, linestyle='--', label='y < -x + 5')
        ax.fill_between(x, y, y_bound, where=(y_bound > y), color='#38BDF8', alpha=0.25)
        ax.scatter([2], [2], color='#34D399', s=160, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate('Feasible Point (2, 2)', (2, 2), textcoords="offset points", xytext=(12, 12),
                    fontsize=12, fontweight='bold', color='#34D399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#34D399", lw=1.5))
        ax.set_xlim(-1, 5)
        ax.set_ylim(-3, 7)

    ax.legend(loc='upper right', facecolor='#0B0F19', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

def create_masterclass_slide(module, graph_img_path, output_path):
    """Assemble 1920x1080 masterclass tutorial slide."""
    img = Image.new('RGB', (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    f_badge = get_font(16, bold=True)
    f_title = get_font(28, bold=True)
    f_header = get_font(20, bold=True)
    f_body = get_font(18, bold=False)
    f_code = get_font(18, bold=True)

    # Top Header Bar
    draw.rectangle([(40, 25), (1880, 85)], fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((60, 42), "DIGITAL SAT MATH 2025/2026", fill=ACCENT_CYAN, font=f_badge)
    draw.text((380, 42), "|  OFFICIAL DESMOS CHEAT CODE MASTERCLASS  |", fill=TEXT_MUTED, font=f_badge)
    draw.text((880, 40), f"MODULE {module['module_id']}/10: {module['title'][:55]}", fill=TEXT_WHITE, font=f_header)
    draw.text((1680, 42), f"TIME: {module['timestamp']}", fill=ACCENT_GOLD, font=f_badge)

    # LEFT PANEL: Question & Cheat Codes (X: 40 -> 880, Y: 105 -> 1010)
    left_w = 840

    # 1. Official SAT Question Box
    draw.rounded_rectangle([(40, 105), (40 + left_w, 320)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((65, 125), "COLLEGE BOARD OFFICIAL QUESTION ARITYPE", fill=ACCENT_GOLD, font=f_badge)
    
    # Wrap text for question statement
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

    # 2. The Algebra Trap Box (Warning)
    draw.rounded_rectangle([(40, 340), (40 + left_w, 510)], radius=12, fill=(35, 20, 25), outline=(120, 40, 50), width=1)
    draw.text((65, 360), "❌ THE SLOW ALGEBRA TRAP (Manual Method: 90 - 120s)", fill=ACCENT_RED, font=f_badge)
    
    trap = module['algebra_trap']
    t_lines = [trap[i:i+60] for i in range(0, min(len(trap), 180), 60)]
    y_t = 395
    for tl in t_lines[:3]:
        draw.text((65, y_t), tl, fill=(254, 202, 202), font=f_body)
        y_t += 28

    # 3. Desmos 10-Second Cheat Code Box (Hero Success)
    draw.rounded_rectangle([(40, 530), (40 + left_w, 790)], radius=12, fill=(18, 38, 32), outline=ACCENT_GREEN, width=2)
    draw.text((65, 550), "⚡ DESMOS 10-SECOND CHEAT CODE (Score 800 Fast)", fill=ACCENT_GREEN, font=f_badge)
    
    code_desc = module['desmos_cheat_code']
    c_lines = [code_desc[i:i+58] for i in range(0, min(len(code_desc), 240), 58)]
    y_c = 585
    for cl in c_lines[:4]:
        draw.text((65, y_c), cl, fill=TEXT_WHITE, font=f_body)
        y_c += 28

    # Desmos Input Commands Pill
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

    # RIGHT PANEL: Simulated Desmos Interactive Window (X: 910 -> 1880, Y: 105 -> 970)
    right_x = 910
    right_w = 970
    draw.rounded_rectangle([(right_x, 105), (right_x + right_w, 970)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)

    # Desmos Window Header
    draw.rectangle([(right_x, 105), (right_x + right_w, 155)], fill=(15, 23, 42))
    draw.text((right_x + 25, 122), "DESMOS GRAPHING CALCULATOR (OFFICIAL SAT SUITE)", fill=TEXT_WHITE, font=f_badge)
    # Window controls (colored dots)
    draw.ellipse([(right_x + right_w - 70, 125), (right_x + right_w - 56, 139)], fill=(239, 68, 68))
    draw.ellipse([(right_x + right_w - 48, 125), (right_x + right_w - 34, 139)], fill=(234, 179, 8))
    draw.ellipse([(right_x + right_w - 26, 125), (right_x + right_w - 12, 139)], fill=(34, 197, 94))

    # Paste the Matplotlib Graph into the Desmos Window
    if os.path.exists(graph_img_path):
        graph = Image.open(graph_img_path).resize((right_w - 20, 790))
        img.paste(graph, (right_x + 10, 165))

    # Bottom Footer Bar
    draw.rectangle([(40, 995), (1880, 1055)], fill=CARD_BG, outline=BORDER_COLOR, width=1)
    progress_w = int((module['module_id'] / 10.0) * 800)
    draw.rectangle([(60, 1020), (60 + progress_w, 1030)], fill=ACCENT_CYAN)
    draw.rectangle([(60, 1020), (860, 1030)], outline=BORDER_COLOR, width=1)
    draw.text((880, 1015), f"Masterclass Progress: {module['module_id']*10}%", fill=TEXT_MUTED, font=f_badge)
    draw.text((1500, 1015), "EduProSuite SAT Prep Suite  •  eduprosuite.pro", fill=ACCENT_GOLD, font=f_badge)

    img.save(output_path, quality=95)

def render_audio_speech(module, output_audio_path):
    """Generate audio voiceover for the module. Uses gTTS if available, or generates wave chime."""
    text = (
        f"Module {module['module_id']}. {module['title']}. "
        f"Here is the problem: {module['problem_statement']}. "
        f"The slow algebra way takes over a minute. But with Desmos: {module['desmos_cheat_code']}. "
        f"Remember this pro tip: {module['pro_tip']}"
    )
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='com')
        tts.save(output_audio_path)
        return True
    except Exception as e:
        print(f"gTTS not available or error: {e}. Generating clean tone audio.")
        # Fallback: Generate clean WAV tone with scipy / wave
        import wave, struct
        sample_rate = 44100
        duration = 5.0 # 5 seconds audio placeholder
        n_samples = int(sample_rate * duration)
        with wave.open(output_audio_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            for i in range(n_samples):
                val = int(1000 * np.sin(2 * np.pi * 440 * (i / sample_rate)))
                data = struct.pack('<h', val)
                wav_file.writeframes(data)
        return True

def compile_video(slide_paths, audio_paths, output_mp4, test_mode=False):
    """Compile slides and audio into MP4 video using MoviePy or FFmpeg."""
    print(f"Compiling {len(slide_paths)} slides into {output_mp4}...")
    try:
        from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        clips = []
        for s_path, a_path in zip(slide_paths, audio_paths):
            duration = 10 if test_mode else 30
            if os.path.exists(a_path) and a_path.endswith('.mp3'):
                try:
                    a_clip = AudioFileClip(a_path)
                    duration = max(a_clip.duration + 2.0, duration)
                    clip = ImageClip(s_path).set_duration(duration).set_audio(a_clip)
                except Exception:
                    clip = ImageClip(s_path).set_duration(duration)
            else:
                clip = ImageClip(s_path).set_duration(duration)
            clips.append(clip)

        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(
            output_mp4,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=2
        )
        print(f"SUCCESS: Video successfully written to {output_mp4}")
        return True
    except Exception as e:
        print(f"Moviepy error: {e}. Attempting FFmpeg CLI fallback...")
        # Direct FFmpeg fallback if installed
        try:
            import subprocess
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", slide_paths[0],
                "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", output_mp4
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as ffe:
            print(f"FFmpeg CLI fallback also failed: {ffe}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Digital SAT Math Desmos Masterclass Generator")
    parser.add_argument("--test-clip", action="store_true", help="Generate single test module clip (fast QA)")
    parser.add_argument("--dry-run", action="store_true", help="Generate slides and graphs only, without compiling MP4")
    parser.add_argument("--full", action="store_true", help="Compile full 10-module masterclass")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(FINAL_VIDEO_PATH), exist_ok=True)

    with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    modules = data['modules']
    if args.test_clip:
        modules = modules[:1]
        print(f"TEST MODE: Processing Module 1 only for rapid verification...")

    slide_paths = []
    audio_paths = []

    for mod in modules:
        m_id = mod['module_id']
        print(f"Generating Module {m_id}: {mod['title']}...")
        graph_path = os.path.join(OUTPUT_DIR, f"graph_module_{m_id}.png")
        slide_path = os.path.join(OUTPUT_DIR, f"slide_module_{m_id}.png")
        audio_path = os.path.join(OUTPUT_DIR, f"audio_module_{m_id}.wav")

        generate_desmos_graph(mod, graph_path)
        create_masterclass_slide(mod, graph_path, slide_path)
        render_audio_speech(mod, audio_path)

        slide_paths.append(slide_path)
        audio_paths.append(audio_path)

    print(f"All {len(slide_paths)} module slides generated successfully in {OUTPUT_DIR}.")

    if not args.dry_run:
        target_out = os.path.join(OUTPUT_DIR, "test_module_1.mp4") if args.test_clip else FINAL_VIDEO_PATH
        compile_video(slide_paths, audio_paths, target_out, test_mode=args.test_clip)

if __name__ == "__main__":
    main()
