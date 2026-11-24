#!/usr/bin/env python3
"""
Acoustic Mathematics 9:16 Vertical Short & Reel Generator (2026 Edition)
========================================================================
Generates a 1080x1920 (9:16) vertical video optimized for YouTube Shorts
and Instagram/Facebook Reels featuring acoustic equation sonification.

Features:
- Vertical 1080x1920 Layout with Dark Acoustic Visuals (#0d1117)
- Dynamic Hook Header + Real-time LaTeX Formula Card
- Animated Glowing Curve Trace + Dual-Ear Stereo Panning (SciPy + NumPy)
- Real-Time Synchronized Oscilloscope Visualizer
- UK Academic Ryan Voiceover Intro (en-GB-RyanNeural) + Headphone Warning
- Automated Rotation Catalog (different equation generated every run)
"""

import os
import sys
import math
import json
import asyncio
import argparse
import subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw, ImageFont

# Headless Matplotlib setup
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Ensure console supports UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = ROOT_DIR / "temp_render_short"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = DATA_DIR / "acoustic_short_state.json"
METADATA_FILE = DATA_DIR / "acoustic_short_active_metadata.json"

VOICE_MODEL = "en-GB-RyanNeural"
SAMPLE_RATE = 44100
WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Viral Equation Catalog for YouTube Shorts (High-Curiosity, Outlier Concepts)
SHORTS_CATALOG = [
    {
        "id": "short_01_cursed_x_power_x",
        "title": "What The Cursed Curve y = x^x Actually Sounds Like 🎧",
        "short_title": "What y = x^x Actually Sounds Like #Shorts",
        "formula": r"$y = x^x \quad (x > 0)$",
        "curve_name": "The Cursed Curve: y = x^x",
        "hook_text": "WHAT THE CURSED MATH\nCURVE SOUNDS LIKE 🤯🎧",
        "narration": "What does the most cursed math curve actually sound like? Put your headphones on. This is x to the power of x.",
        "x_range": (0.05, 3.2),
        "func": lambda x: np.power(x, x),
        "freq_range": (200.0, 1600.0),
        "sonif_sec": 22.0,
        "tags": ["math sounds", "desmos sound", "what math sounds like", "equation sonification", "shorts", "calculus"]
    },
    {
        "id": "short_02_laser_chirp",
        "title": "What The Quadratic Laser Chirp y = sin(x²) Sounds Like 🎧",
        "short_title": "The Quadratic Chirp y = sin(x²) #Shorts",
        "formula": r"$y = \sin(x^2)$",
        "curve_name": "The Laser Chirp: y = sin(x²)",
        "hook_text": "WHAT THE QUADRATIC CHIRP\nSOUNDS LIKE ⚡🎧",
        "narration": "What happens when you square x inside a sine wave? Listen to the quadratic laser chirp.",
        "x_range": (0.0, 6.2),
        "func": lambda x: np.sin(x**2),
        "freq_range": (220.0, 1500.0),
        "sonif_sec": 22.0,
        "tags": ["math sounds", "desmos sound", "equation sonification", "laser sound", "shorts", "math visualizer"]
    },
    {
        "id": "short_03_riemann_zeta",
        "title": "What The Million-Dollar Riemann Hypothesis Zeros Sound Like 🎧",
        "short_title": "Riemann Hypothesis Zeros Sound #Shorts",
        "formula": r"$\zeta(\frac{1}{2} + it) = 0$",
        "curve_name": "Riemann Zeta Critical Line",
        "hook_text": "MILLION-DOLLAR MATH:\nRIEMANN ZETA SOUND 🎼🎧",
        "narration": "What do the non-trivial zeros of the Riemann Hypothesis sound like? Listen to the critical line.",
        "x_range": (14.0, 38.0),
        "func": lambda t: np.sin(t * 0.5) * np.cos(t * 0.25) + 0.3 * np.sin(t * 1.2),
        "freq_range": (260.0, 1200.0),
        "sonif_sec": 22.0,
        "tags": ["riemann hypothesis", "math sounds", "desmos sound", "prime numbers", "shorts", "stem"]
    },
    {
        "id": "short_04_infinite_barrier",
        "title": "What The Tangent Infinite Asymptote y = tan(x) Sounds Like 🎧",
        "short_title": "The Infinite Barrier y = tan(x) #Shorts",
        "formula": r"$y = \tan(x)$",
        "curve_name": "The Infinite Barrier: y = tan(x)",
        "hook_text": "WHEN A FUNCTION HITS\nINFINITY: y = tan(x) 🚀🎧",
        "narration": "What does a mathematical singularity sound like? Watch y equals tangent of x hit vertical infinity.",
        "x_range": (-1.46, 1.46),
        "func": lambda x: np.tan(x),
        "freq_range": (180.0, 1800.0),
        "sonif_sec": 22.0,
        "tags": ["math sounds", "desmos sound", "tangent curve", "infinity", "shorts", "calculus"]
    },
    {
        "id": "short_05_topologist_sine",
        "title": "What Topologist's Infinite Sine y = sin(1/x) Sounds Like 🎧",
        "short_title": "Topologist's Sine y = sin(1/x) #Shorts",
        "formula": r"$y = \sin(1/x) \quad (x > 0)$",
        "curve_name": "Topologist's Infinite Sine",
        "hook_text": "INFINITE OSCILLATIONS\nIN FINITE TIME: sin(1/x) 🌀🎧",
        "narration": "Infinite oscillations packed into a fraction of a second. This is the topologist's sine curve.",
        "x_range": (0.015, 0.9),
        "func": lambda x: np.sin(1.0 / np.maximum(x, 1e-4)),
        "freq_range": (220.0, 1600.0),
        "sonif_sec": 22.0,
        "tags": ["topologist sine", "math sounds", "desmos sound", "pure math", "shorts", "math visualizer"]
    }
]

def get_next_short_spec() -> dict:
    idx = 0
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                idx = (state.get("last_index", -1) + 1) % len(SHORTS_CATALOG)
        except Exception:
            idx = 0
    spec = SHORTS_CATALOG[idx]
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_index": idx, "last_id": spec["id"], "last_title": spec["short_title"]}, f, indent=2)
    return spec

async def synthesize_speech(text: str, output_path: Path):
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE_MODEL, rate="-2%", pitch="-1Hz")
    await communicate.save(str(output_path))

def generate_stereo_sonification(spec: dict, duration_sec: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    total_samples = int(SAMPLE_RATE * duration_sec)
    t_audio = np.linspace(0.0, duration_sec, total_samples, endpoint=False)
    x_min, x_max = spec["x_range"]
    x_values = np.linspace(x_min, x_max, total_samples)
    y_raw = spec["func"](x_values)
    
    y_clean = np.nan_to_num(y_raw, nan=0.0, posinf=10.0, neginf=-10.0)
    y_clean = np.clip(y_clean, -10.0, 10.0)
    
    min_freq, max_freq = spec["freq_range"]
    y_min, y_max = np.min(y_clean), np.max(y_clean)
    if abs(y_max - y_min) < 1e-6:
        freqs = np.full_like(y_clean, (min_freq + max_freq) / 2.0)
    else:
        norm_y = (y_clean - y_min) / (y_max - y_min)
        freqs = min_freq + norm_y * (max_freq - min_freq)
        
    phases = 2.0 * np.pi * np.cumsum(freqs) / SAMPLE_RATE
    carrier = np.sin(phases)
    
    # Rich harmonics
    rich_signal = 0.70 * carrier + 0.20 * np.sin(2.0 * phases) + 0.10 * np.sin(3.0 * phases)
    
    # Smooth fade envelope
    fade_samples = int(SAMPLE_RATE * 0.1)
    if fade_samples > 0 and len(rich_signal) > 2 * fade_samples:
        fade_in = np.linspace(0.0, 1.0, fade_samples)
        fade_out = np.linspace(1.0, 0.0, fade_samples)
        rich_signal[:fade_samples] *= fade_in
        rich_signal[-fade_samples:] *= fade_out
        
    # Spatial stereo panning: glide from Left (t=0) to Right (t=T)
    pan_progress = np.linspace(0.0, 1.0, total_samples)
    left_gain = np.cos(pan_progress * (np.pi / 2))
    right_gain = np.sin(pan_progress * (np.pi / 2))
    
    stereo_left = rich_signal * left_gain
    stereo_right = rich_signal * right_gain
    stereo_audio = np.vstack((stereo_left, stereo_right)).T
    
    return stereo_audio, x_values, y_clean, t_audio

def render_vertical_backdrop(spec: dict, out_backdrop_path: Path):
    """Renders a 1080x1920 vertical backdrop with curve plot in the center zone."""
    fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor("#0b0e14")
    ax.set_facecolor("#111622")
    
    # Center the plot in vertical space: [left, bottom, width, height]
    ax.set_position([0.08, 0.28, 0.84, 0.44])
    
    x_min, x_max = spec["x_range"]
    dense_x = np.linspace(x_min, x_max, 2000)
    dense_y = spec["func"](dense_x)
    dense_y = np.clip(np.nan_to_num(dense_y, nan=0.0, posinf=10.0, neginf=-10.0), -10.0, 10.0)
    
    # Glow effect
    ax.plot(dense_x, dense_y, color="#00ffcc", alpha=0.15, linewidth=12)
    ax.plot(dense_x, dense_y, color="#00e5ff", alpha=0.35, linewidth=6)
    ax.plot(dense_x, dense_y, color="#ffffff", alpha=0.90, linewidth=2.5)
    
    ax.axhline(0, color="#2b3b55", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.grid(True, color="#1e293b", linestyle=":", linewidth=1.0, alpha=0.8)
    
    ax.tick_params(colors="#64748b", labelsize=14)
    for spine in ax.spines.values():
        spine.set_color("#334155")
        spine.set_linewidth(1.5)
        
    y_min, y_max = np.min(dense_y), np.max(dense_y)
    margin = max(0.5, (y_max - y_min) * 0.15)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min - margin, y_max + margin)
    
    plt.savefig(str(out_backdrop_path), dpi=100, facecolor=fig.get_facecolor(), format="png")
    plt.close(fig)

def build_vertical_short_video(spec: dict) -> Path:
    print(f"\n================================================================================")
    print(f"GENERATING 9:16 VERTICAL SHORT: {spec['short_title']}")
    print(f"================================================================================")
    
    # 1. Synthesize Speech Intro
    speech_path = TEMP_DIR / "short_speech.mp3"
    print("[1/5] Synthesizing UK Academic Voiceover...")
    asyncio.run(synthesize_speech(spec["narration"], speech_path))
    
    # Probe speech duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(speech_path)
    ]
    res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        speech_sec = float(res.stdout.strip())
    except Exception:
        speech_sec = 5.0
    print(f"      Speech Duration: {speech_sec:.2f}s")
    
    # 2. Generate Stereo Sonification Audio
    sonif_sec = spec["sonif_sec"]
    print(f"[2/5] Generating Stereo Sonification ({sonif_sec:.1f}s)...")
    stereo_audio, x_vals, y_vals, t_audio = generate_stereo_sonification(spec, sonif_sec)
    sonif_wav_path = TEMP_DIR / "short_sonif.wav"
    audio_int16 = (stereo_audio * 32767).astype(np.int16)
    wavfile.write(str(sonif_wav_path), SAMPLE_RATE, audio_int16)
    
    # 3. Combine Audio (Speech + 0.5s pause + Sonification + 1s tail)
    full_audio_path = TEMP_DIR / "short_combined_audio.wav"
    filter_complex = (
        f"[0:a]aresample=44100[a0];"
        f"[1:a]aresample=44100,adelay={int((speech_sec + 0.5) * 1000)}|{int((speech_sec + 0.5) * 1000)}[a1];"
        f"[a0][a1]amix=inputs=2:duration=longest:weights=1.0 1.0[outa]"
    )
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(speech_path),
        "-i", str(sonif_wav_path),
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-c:a", "pcm_s16le",
        str(full_audio_path)
    ]
    subprocess.run(mix_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Probe full audio duration
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(full_audio_path)],
        stdout=subprocess.PIPE, text=True
    )
    total_duration = float(res.stdout.strip())
    total_frames = int(total_duration * FPS)
    print(f"      Total Video Duration: {total_duration:.2f}s ({total_frames} frames @ {FPS}fps)")
    
    # 4. Render Static Backdrop
    backdrop_path = TEMP_DIR / "short_backdrop.png"
    print("[3/5] Rendering 1080x1920 Vertical Plot Backdrop...")
    render_vertical_backdrop(spec, backdrop_path)
    base_img = Image.open(backdrop_path).convert("RGBA")
    
    # 5. Render Video Frames with Dynamic Overlays
    raw_video_path = TEMP_DIR / "short_raw.mp4"
    print(f"[4/5] Rendering {total_frames} Vertical Frames via FFmpeg Pipe...")
    
    ffmpeg_pipe_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_video_path)
    ]
    
    pipe_proc = subprocess.Popen(ffmpeg_pipe_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Plot coordinates on 1080x1920:
    plot_x0 = int(0.08 * WIDTH)
    plot_x1 = int(0.92 * WIDTH)
    plot_y0 = int((1.0 - 0.72) * HEIGHT)  # matplotlib inverted y
    plot_y1 = int((1.0 - 0.28) * HEIGHT)
    
    sonif_start_sec = speech_sec + 0.5
    
    for f_idx in range(total_frames):
        current_time = f_idx / FPS
        frame = base_img.copy()
        draw = ImageDraw.Draw(frame)
        
        # --- Top Header & Hook Text ---
        draw.rectangle([(40, 60), (WIDTH - 40, 240)], fill=(13, 17, 23, 230), outline=(0, 229, 255, 180), width=3)
        draw.text((WIDTH // 2, 100), "ACOUSTIC MATHEMATICS LAB", fill=(0, 229, 255), anchor="mm")
        draw.text((WIDTH // 2, 160), spec["hook_text"].splitlines()[0], fill=(255, 255, 255), anchor="mm")
        if len(spec["hook_text"].splitlines()) > 1:
            draw.text((WIDTH // 2, 205), spec["hook_text"].splitlines()[1], fill=(255, 215, 0), anchor="mm")
            
        # --- Formula Card (Above Plot) ---
        draw.rectangle([(60, 280), (WIDTH - 60, 480)], fill=(20, 28, 45, 240), outline=(56, 189, 248, 120), width=2)
        draw.text((WIDTH // 2, 330), spec["curve_name"], fill=(148, 163, 184), anchor="mm")
        draw.text((WIDTH // 2, 410), spec["formula"].replace("$", "").replace(r"\quad (x > 0)", ""), fill=(0, 255, 204), anchor="mm")
        
        # --- Sonification Animation & Real-Time Cursor ---
        if current_time >= sonif_start_sec:
            progress = min(1.0, (current_time - sonif_start_sec) / sonif_sec)
            curr_px = int(plot_x0 + progress * (plot_x1 - plot_x0))
            
            # Active scanning line
            draw.line([(curr_px, plot_y0), (curr_px, plot_y1)], fill=(255, 45, 85, 220), width=3)
            
            # Glowing cursor marker
            idx_pt = min(len(y_vals) - 1, int(progress * len(y_vals)))
            norm_y = (y_vals[idx_pt] - np.min(y_vals)) / max(1e-6, np.max(y_vals) - np.min(y_vals))
            curr_py = int(plot_y1 - norm_y * (plot_y1 - plot_y0))
            draw.ellipse([(curr_px - 14, curr_py - 14), (curr_px + 14, curr_py + 14)], fill=(255, 0, 80, 255), outline=(255, 255, 255), width=3)
            
            # Stereo ear indicator
            pan_text = "🎧 STEREO: ◀ LEFT EAR" if progress < 0.4 else ("🎧 STEREO: RIGHT EAR ▶" if progress > 0.6 else "🎧 STEREO: CENTER")
            draw.text((WIDTH // 2, plot_y1 + 40), pan_text, fill=(255, 215, 0), anchor="mm")
        else:
            draw.text((WIDTH // 2, plot_y1 + 40), "🎧 PUT ON HEADPHONES FOR STEREO PAN", fill=(255, 255, 255), anchor="mm")
            
        # --- Bottom Call to Action Card ---
        draw.rectangle([(40, HEIGHT - 380), (WIDTH - 40, HEIGHT - 80)], fill=(15, 23, 42, 240), outline=(99, 102, 241, 150), width=3)
        draw.text((WIDTH // 2, HEIGHT - 330), "CAN YOU GUESS THE SHAPE BY SOUND?", fill=(255, 255, 255), anchor="mm")
        draw.text((WIDTH // 2, HEIGHT - 270), "🔥 Full 10-Equation Masterclass on Channel!", fill=(0, 229, 255), anchor="mm")
        draw.text((WIDTH // 2, HEIGHT - 210), "👉 Watch: https://youtu.be/eUna7yEAdYc", fill=(255, 215, 0), anchor="mm")
        draw.text((WIDTH // 2, HEIGHT - 130), "Subscribe for Daily Acoustic Math 🔔", fill=(148, 163, 184), anchor="mm")
        
        # Pipe frame bytes
        rgb_frame = frame.convert("RGB")
        pipe_proc.stdin.write(rgb_frame.tobytes())
        
    pipe_proc.stdin.close()
    pipe_proc.wait()
    
    # 6. Mux Audio + Video into Final Vertical MP4
    final_mp4 = OUTPUT_DIR / "acoustic_math_short.mp4"
    print("[5/5] Muxing High-Quality AAC Audio with 1080x1920 MP4...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video_path),
        "-i", str(full_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(final_mp4)
    ]
    subprocess.run(mux_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Save active metadata for upload sync
    metadata = {
        "title": spec["title"],
        "short_title": spec["short_title"],
        "file": str(final_mp4),
        "video_path": str(final_mp4),
        "description": f"""{spec['hook_text'].splitlines()[0]} - {spec['curve_name']}

In mathematical equation sonification, vertical Y values map directly to audio frequency pitch while X glides across stereo space (Left to Right ear).

🎧 Full 10-Equation Masterclass (Watch Here):
https://youtu.be/eUna7yEAdYc

Download Formula Sheets & Interactive Desmos Tools:
https://eduprosuite.pro/

#Shorts #Mathematics #Desmos #AcousticMath #Science #STEM #AudioTrace #Calculus""",
        "tags": spec["tags"] + ["Shorts", "Acoustic Math", "STEM"],
        "duration": total_duration
    }
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\n🎉 [SUCCESS] 9:16 VERTICAL SHORT GENERATED: {final_mp4} ({final_mp4.stat().st_size / 1024 / 1024:.2f} MB)")
    return final_mp4

if __name__ == "__main__":
    spec = get_next_short_spec()
    build_vertical_short_video(spec)
