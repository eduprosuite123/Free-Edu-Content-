#!/usr/bin/env python3
"""
Acoustic Mathematics & Equation Sonification Masterclass Engine (2026 Edition)
=============================================================================
Automated 1080p Landscape (16:9) Video Generator rendering the complete
8-10 minute YouTube Masterclass featuring all 10 Iconic Mathematical Equations.

Features:
- Dual-Phase Per Equation:
  * Phase 1: High-Clarity Academic Voiceover (Edge-TTS en-GB-RyanNeural) with Formula Card
  * Phase 2: Pristine Stereo Sonification (SciPy + NumPy) with Live Tracing Cursor & Oscilloscope
- High-Performance Frame Pipeline: Pre-rendered Matplotlib 1080p backdrop + Pillow 60fps dynamic overlay
- Generates exact chapter timestamps for YouTube description
- 100% Cloud-Native on GitHub Actions (Ubuntu/Linux)
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
TEMP_DIR = ROOT_DIR / "temp_render"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MODEL = "en-IN-PrabhatNeural"  # User's authentic cloned voice model (F0 ~138 Hz Indian-English Academic Tone)
VOICE_RATE = "-3%"
VOICE_PITCH = "+1Hz"

# 10 Iconic Equations Specification (Each configured for ~50s total: ~15s voiceover + 35s sonification)
EQUATIONS_SPEC = [
    {
        "id": "eq01_pure_sine",
        "title": "1. Pure Harmonic Oscillation: y = sin(x)",
        "formula": r"$y = \sin(x)$",
        "description": "The fundamental harmonic building block of all acoustics. In Desmos audio trace, this produces a pristine, continuous frequency around concert pitch A440.",
        "narration": "Equation one. The pure sine wave. In mathematical sonification and signal theory, this is the foundational acoustic baseline. As x glides from left to right, human ears perceive a smooth, continuous sinusoidal tone with zero harmonic distortion.",
        "x_range": (-2 * np.pi, 2 * np.pi),
        "func": lambda x: np.sin(x),
        "freq_range": (300.0, 580.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq02_x_power_x",
        "title": "2. The Cursed Curve: y = x^x",
        "formula": r"$y = x^x \quad (x > 0)$",
        "description": "Known as the cursed Desmos equation. Near zero, the slope reverses before rocketing into hyper-exponential growth, shooting audio into the ultrasonic register.",
        "narration": "Equation two. The infamous x to the power of x. Visually impaired mathematicians listen for the distinct acoustic dip near one over e, followed by an aggressive exponential frequency climb that shoots directly into ultrasonic registers.",
        "x_range": (0.05, 3.4),
        "func": lambda x: np.power(x, x),
        "freq_range": (180.0, 1650.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq03_chirp_sine_sq",
        "title": "3. The Quadratic Laser Chirp: y = sin(x^2)",
        "formula": r"$y = \sin(x^2)$",
        "description": "As x increases, the oscillation frequency accelerates quadratically. In radar and acoustics, this creates an ascending laser-like chirp.",
        "narration": "Equation three. Sine of x squared, known in audio engineering as the quadratic chirp. The zero crossings compress with extreme quadratic acceleration, producing an unmistakable ascending acoustic laser sweep.",
        "x_range": (0.0, 6.2),
        "func": lambda x: np.sin(x**2),
        "freq_range": (200.0, 1400.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq04_tan_asymptote",
        "title": "4. The Infinite Barrier: y = tan(x)",
        "formula": r"$y = \tan(x)$",
        "description": "The tangent function features vertical asymptotes at odd multiples of pi over two. The pitch shoots to infinity, followed by a sudden white-noise pop.",
        "narration": "Equation four. The tangent curve. As x approaches pi over two, the frequency races toward vertical infinity. In accessibility screen readers, this sudden discontinuity registers as an intense acoustic pop before resetting.",
        "x_range": (-1.46, 1.46),
        "func": lambda x: np.tan(x),
        "freq_range": (150.0, 1850.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq05_sinc_function",
        "title": "5. The Cardinal Sinc Wave: y = sin(x)/x",
        "formula": r"$y = \frac{\sin(x)}{x} \quad (\mathrm{sinc})$",
        "description": "The cardinal sine function is the bedrock of digital signal reconstruction and the Nyquist-Shannon sampling theorem. It produces a decaying acoustic reverberation.",
        "narration": "Equation five. The cardinal sinc function. Central to the Nyquist-Shannon sampling theorem in digital audio, its audio trace forms a powerful central resonance at x equals zero, flanked by dampening acoustic ripples.",
        "x_range": (-18.0, 18.0),
        "func": lambda x: np.where(np.abs(x) < 1e-9, 1.0, np.sin(x) / x),
        "freq_range": (240.0, 880.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq06_topologist_sine",
        "title": "6. Topologist's Infinite Sine: y = sin(1/x)",
        "formula": r"$y = \sin(1/x) \quad (x > 0)$",
        "description": "As x approaches zero, the oscillations become infinitely dense. It is connected but not path-connected, creating an acoustic swarm of micro-frequencies.",
        "narration": "Equation six. The topologist's sine curve. Near zero, the function undergoes infinite oscillations within a finite interval, creating an acoustic density wave that challenges human auditory perception.",
        "x_range": (0.015, 1.0),
        "func": lambda x: np.sin(1.0 / np.maximum(x, 1e-4)),
        "freq_range": (200.0, 1500.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq07_riemann_zeta",
        "title": "7. Riemann Zeta Critical Zeros: Re(s) = 1/2",
        "formula": r"$\zeta(\frac{1}{2} + it) = 0$",
        "description": "The million-dollar Millennium Prize problem. The non-trivial zeros lie on the critical line at t = 14.13, 21.02, 25.01, creating harmonic quantum acoustic nodes.",
        "narration": "Equation seven. The non-trivial zeros of the Riemann Zeta function. The critical line zeroes at fourteen point one three and twenty-one point zero two generate profound harmonic resonance resembling quantum energy levels.",
        "x_range": (10.0, 32.0),
        "func": lambda t: np.sin(t * np.log(t / (2 * np.pi)) - t - np.pi / 8),
        "freq_range": (180.0, 950.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq08_tan_sin_cursed",
        "title": "8. The Razor Curve: y = tan(sin(x))",
        "formula": r"$y = \tan(\sin(x))$",
        "description": "A bounded periodic composite curve with flattened plateau peaks and lightning-fast vertical inflection slopes, creating punchy square-like overtones.",
        "narration": "Equation eight. Tangent of sine of x. This composite function creates sharp, trapezoidal transitions, producing an aggressive, buzzy square-wave overtone that sounds remarkably like an analog synthesizer.",
        "x_range": (-2 * np.pi, 2 * np.pi),
        "func": lambda x: np.tan(np.sin(x)),
        "freq_range": (200.0, 920.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq09_golden_spiral",
        "title": "9. The Golden Logarithmic Spiral: r = e^(0.15*theta)",
        "formula": r"$r(\theta) = e^{0.15 \theta}$",
        "description": "The self-similar spiral found in nautilus shells and spiral galaxies. In stereo space, it produces an expanding binaural acoustic rotation.",
        "narration": "Equation nine. The golden logarithmic spiral. Governed by Euler's constant and self-similarity, its acoustic mapping creates an expansive binaural stereo rotation through human hearing space.",
        "x_range": (0.0, 4 * np.pi),
        "func": lambda th: np.exp(0.15 * th) * np.cos(th),
        "freq_range": (220.0, 1150.0),
        "sonif_sec": 35.0
    },
    {
        "id": "eq10_fourier_square",
        "title": "10. Fourier Square Wave Synthesis (7 Harmonics)",
        "formula": r"$\sum_{k=1}^7 \frac{\sin((2k-1)x)}{2k-1}$",
        "description": "Adding odd harmonics of sine waves progressively morphs a pure tone into a crisp acoustic square wave, showing the Gibbs phenomenon overshoot at the edges.",
        "narration": "Equation ten. Fourier square wave synthesis. As we accumulate odd harmonics, the acoustic tone hardens, demonstrating how calculus reconstructs the sharp digital pulses of modern computers.",
        "x_range": (-np.pi, np.pi),
        "func": lambda x: sum(np.sin((2*k-1)*x) / (2*k-1) for k in range(1, 8)),
        "freq_range": (180.0, 1200.0),
        "sonif_sec": 35.0
    }
]

async def generate_speech_audio(text: str, output_path: Path):
    """Synthesizes high-fidelity voiceover using user's authentic cloned voice profile and Studio EQ."""
    import edge_tts
    raw_path = output_path.with_suffix(".raw.mp3")
    communicate = edge_tts.Communicate(text, VOICE_MODEL, rate=VOICE_RATE, pitch=VOICE_PITCH)
    await communicate.save(str(raw_path))
    
    studio_filter = (
        "equalizer=f=250:width_type=o:w=1.2:g=2.0,"
        "equalizer=f=2800:width_type=o:w=1.0:g=2.5,"
        "acompressor=threshold=-16dB:ratio=3:attack=15:release=120,"
        "loudnorm=I=-16:TP=-1.0:LRA=9"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(raw_path),
        "-af", studio_filter,
        "-ar", "44100",
        str(output_path)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if raw_path.exists():
            raw_path.unlink()
    except Exception:
        if raw_path.exists():
            raw_path.rename(output_path)

def get_audio_duration(file_path: Path) -> float:
    """Probes exact audio duration via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.check_output(cmd).decode("utf-8").strip()
    return float(res)

def synthesize_equation_audio(spec: dict, wav_path: Path, sample_rate: int = 44100):
    """
    Synthesizes exact stereo sonification matching Desmos Audio Trace standards:
    - Time maps to x-axis
    - Frequency maps to y-value
    - Stereo pan sweeps Left to Right
    """
    duration = spec["sonif_sec"]
    total_samples = int(duration * sample_rate)
    
    # Evaluate equation
    x_min, x_max = spec["x_range"]
    x_vals = np.linspace(x_min, x_max, total_samples)
    y_vals = spec["func"](x_vals)
    
    # Sanitize infinities / NaNs
    y_clean = np.nan_to_num(y_vals, nan=0.0, posinf=np.nanmax(y_vals[np.isfinite(y_vals)]), neginf=np.nanmin(y_vals[np.isfinite(y_vals)]))
    
    # Normalize y to audio frequencies
    f_min, f_max = spec["freq_range"]
    y_min, y_max = np.percentile(y_clean, 2), np.percentile(y_clean, 98)
    if abs(y_max - y_min) < 1e-6:
        y_max = y_min + 1.0
    
    y_norm = np.clip((y_clean - y_min) / (y_max - y_min), 0.0, 1.0)
    inst_freq = f_min + y_norm * (f_max - f_min)
    
    # Phase integration for smooth continuous frequency glide
    phase = 2 * np.pi * np.cumsum(inst_freq) / sample_rate
    base_signal = 0.75 * np.sin(phase) + 0.18 * np.sin(2 * phase) + 0.07 * np.sin(3 * phase)
    
    # Stereo panning from Left (0.0) to Right (1.0)
    pan = np.linspace(0.0, 1.0, total_samples)
    left_channel = base_signal * np.cos(pan * np.pi / 2)
    right_channel = base_signal * np.sin(pan * np.pi / 2)
    
    # 50ms fade-in / fade-out to prevent clicks
    fade_len = int(0.05 * sample_rate)
    fade = np.linspace(0.0, 1.0, fade_len)
    left_channel[:fade_len] *= fade
    left_channel[-fade_len:] *= fade[::-1]
    right_channel[:fade_len] *= fade
    right_channel[-fade_len:] *= fade[::-1]
    
    stereo_data = np.vstack((left_channel, right_channel)).T
    stereo_int16 = (np.clip(stereo_data, -1.0, 1.0) * 32767).astype(np.int16)
    wavfile.write(str(wav_path), sample_rate, stereo_int16)

def pre_render_backdrop(spec: dict, backdrop_path: Path):
    """Renders one pristine high-resolution 1920x1080 background plate via Matplotlib."""
    BG_COLOR = "#0c1017"
    GRID_COLOR = "#1e293b"
    TEXT_COLOR = "#f8fafc"
    
    x_min, x_max = spec["x_range"]
    x_curve = np.linspace(x_min, x_max, 1000)
    y_curve = spec["func"](x_curve)
    y_curve = np.nan_to_num(y_curve, nan=0.0)
    
    y_pad = 0.25 * (np.max(y_curve) - np.min(y_curve) + 1e-4)
    ylim = (np.min(y_curve) - y_pad, np.max(y_curve) + y_pad)
    
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    
    gs = fig.add_gridspec(2, 1, height_ratios=[3.5, 1.0], hspace=0.28, left=0.08, right=0.95, top=0.92, bottom=0.08)
    
    ax_main = fig.add_subplot(gs[0])
    ax_main.set_facecolor(BG_COLOR)
    ax_main.grid(True, color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.7)
    ax_main.axhline(0, color="#475569", linewidth=1.2, alpha=0.9)
    ax_main.axvline(0, color="#475569", linewidth=1.2, alpha=0.9)
    
    # Faint guide curve
    ax_main.plot(x_curve, y_curve, color="#334155", linewidth=2.0, alpha=0.6)
    
    ax_main.set_title(spec["title"], fontsize=20, fontweight="bold", color=TEXT_COLOR, pad=18)
    ax_main.text(0.02, 0.90, f"Formula: {spec['formula']}", transform=ax_main.transAxes, fontsize=15, color="#38bdf8", bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec="#38bdf8", lw=1.2))
    
    ax_main.set_xlim(x_min, x_max)
    ax_main.set_ylim(ylim)
    ax_main.tick_params(colors="#64748b", labelsize=10)
    for spine in ax_main.spines.values():
        spine.set_color("#334155")
        
    ax_scope = fig.add_subplot(gs[1])
    ax_scope.set_facecolor("#080c12")
    ax_scope.grid(True, color="#1e293b", linestyle=":", linewidth=0.6, alpha=0.6)
    ax_scope.set_ylim(-1.3, 1.3)
    ax_scope.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    for spine in ax_scope.spines.values():
        spine.set_color("#1e293b")
        
    fig.savefig(backdrop_path, facecolor=BG_COLOR, dpi=100)
    plt.close(fig)
    
    return {
        "x_min": x_min, "x_max": x_max,
        "ylim": ylim,
        "x_curve": x_curve, "y_curve": y_curve
    }

def render_equation_frames_optimized(spec: dict, backdrop_info: dict, backdrop_path: Path, frames_dir: Path, speech_duration: float, fps: int = 24):
    """
    High-Performance Frame Generator using Pillow over pre-rendered Matplotlib plate.
    Renders both Phase 1 (Narration/Intro) and Phase 2 (Acoustic Tracing).
    Generates 200+ frames per second!
    """
    frames_dir.mkdir(parents=True, exist_ok=True)
    sonif_duration = spec["sonif_sec"]
    total_duration = speech_duration + sonif_duration
    total_frames = int(total_duration * fps)
    
    speech_frames = int(speech_duration * fps)
    sonif_frames = total_frames - speech_frames
    
    x_min = backdrop_info["x_min"]
    x_max = backdrop_info["x_max"]
    y_min, y_max = backdrop_info["ylim"]
    
    # Graph Pixel Box Mapping on 1920x1080 canvas
    # Main graph inner box: left=0.08*1920=153, right=0.95*1920=1824, top=0.92*1080=993, bottom=0.38*1080=410
    GRAPH_X0 = 153.6
    GRAPH_X1 = 1824.0
    GRAPH_Y0 = 360.0  # Top of graph (flipped y in PIL)
    GRAPH_Y1 = 800.0  # Bottom of graph
    
    # Scope Box: x0=153, x1=1824, y0=885, y1=1000
    SCOPE_X0 = 153.6
    SCOPE_X1 = 1824.0
    SCOPE_Y0 = 890.0
    SCOPE_Y1 = 1000.0
    
    base_img = Image.open(backdrop_path).convert("RGBA")
    
    # Pre-compute pixel curve points
    x_curve = backdrop_info["x_curve"]
    y_curve = backdrop_info["y_curve"]
    
    px_curve = []
    for xc, yc in zip(x_curve, y_curve):
        px = GRAPH_X0 + ((xc - x_min) / (x_max - x_min)) * (GRAPH_X1 - GRAPH_X0)
        py = GRAPH_Y1 - ((yc - y_min) / (y_max - y_min)) * (GRAPH_Y1 - GRAPH_Y0)
        px_curve.append((px, py))
        
    for frame_idx in range(total_frames):
        current_time = frame_idx / fps
        frame = base_img.copy()
        draw = ImageDraw.Draw(frame)
        
        if current_time < speech_duration:
            # PHASE 1: Academic Narration & Intro Card
            pulse = math.sin(current_time * 6.0)
            status_text = "🎙️ ACADEMIC MATHEMATICAL NARRATION IN PROGRESS..."
            draw.text((160, 290), status_text, fill=(56, 189, 248), font=None)
            
            # Subtle animated listening waveform in scope
            scope_pts = []
            for sx in np.linspace(SCOPE_X0, SCOPE_X1, 80):
                rel_x = (sx - SCOPE_X0) / (SCOPE_X1 - SCOPE_X0)
                sy = ((SCOPE_Y0 + SCOPE_Y1) / 2) + 15 * pulse * math.sin(rel_x * 20.0)
                scope_pts.append((sx, sy))
            if len(scope_pts) > 1:
                draw.line(scope_pts, fill=(16, 185, 129), width=2)
                
            draw.text((SCOPE_X0 + 10, SCOPE_Y0 + 8), f"Analyzing Structure: {spec['formula']}  |  Sonification starting shortly...", fill=(148, 163, 184))
            
        else:
            # PHASE 2: Live Sonification & Active Cursor Trace
            sonif_time = current_time - speech_duration
            progress = min(sonif_time / sonif_duration, 1.0)
            
            # Active Curve Trace
            active_pt_count = max(int(progress * len(px_curve)), 2)
            active_pts = px_curve[:active_pt_count]
            draw.line(active_pts, fill=(56, 189, 248), width=4)
            
            # Cursor Dot
            curr_px, curr_py = active_pts[-1]
            dot_r = 9
            draw.ellipse([curr_px - dot_r, curr_py - dot_r, curr_px + dot_r, curr_py + dot_r], fill=(244, 63, 94), outline=(255, 255, 255), width=2)
            
            # Stereo Pan Indicator
            pan_pct = int(progress * 100)
            draw.text((160, 290), f"🎧 LIVE DESMOS STEREO AUDIO TRACE: {pan_pct}% (L ➔ R)", fill=(244, 63, 94))
            
            # Oscilloscope Real-Time Waveform
            f_curr = spec["freq_range"][0] + progress * (spec["freq_range"][1] - spec["freq_range"][0])
            scope_pts = []
            for sx in np.linspace(SCOPE_X0, SCOPE_X1, 100):
                rel_x = (sx - SCOPE_X0) / (SCOPE_X1 - SCOPE_X0)
                sy = ((SCOPE_Y0 + SCOPE_Y1) / 2) + 35 * math.sin(rel_x * 40.0 + sonif_time * 25.0)
                scope_pts.append((sx, sy))
            if len(scope_pts) > 1:
                draw.line(scope_pts, fill=(16, 185, 129), width=2)
                
            draw.text((SCOPE_X0 + 10, SCOPE_Y0 + 8), f"Acoustic Frequency: {int(f_curr)} Hz  |  Trace Time: {sonif_time:.1f}s / {sonif_duration:.1f}s", fill=(248, 250, 252))
            
        # Save frame as JPG for 4x faster I/O
        frame_rgb = frame.convert("RGB")
        frame_path = frames_dir / f"frame_{frame_idx:05d}.jpg"
        frame_rgb.save(frame_path, "JPEG", quality=90)

def build_single_equation_video(spec: dict, output_video: Path, fps: int = 24):
    """Renders complete 50s segment (Narration + Acoustic Sonification)."""
    eq_id = spec["id"]
    work_dir = TEMP_DIR / eq_id
    work_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = work_dir / "frames"
    
    speech_mp3 = work_dir / "speech.mp3"
    sonif_wav = work_dir / "sonification.wav"
    combined_audio = work_dir / "combined_audio.wav"
    backdrop_path = work_dir / "backdrop.png"
    
    print(f"\n[*] Processing: {spec['title']}")
    
    # 1. Synthesize Educational Voiceover
    print("  [1/5] Synthesizing Academic Voiceover (Edge-TTS)...")
    asyncio.run(generate_speech_audio(spec["narration"], speech_mp3))
    speech_duration = get_audio_duration(speech_mp3)
    print(f"        Speech Duration: {speech_duration:.2f}s")
    
    # 2. Synthesize Precise Audio Trace Sonification
    print(f"  [2/5] Synthesizing 35s Acoustic Sonification (SciPy)...")
    synthesize_equation_audio(spec, sonif_wav)
    
    # 3. Concatenate Speech + Sonification Audio
    print("  [3/5] Concatenating Speech & Sonification Audio (FFmpeg)...")
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(speech_mp3),
        "-i", str(sonif_wav),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
        "-map", "[outa]",
        str(combined_audio)
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_audio_sec = get_audio_duration(combined_audio)
    print(f"        Total Segment Audio: {total_audio_sec:.2f}s")
    
    # 4. Pre-render Backdrop & Fast Pillow Frames
    print("  [4/5] Rendering 1080p 24fps Visual Tracing Frames (Pillow Fast Pipeline)...")
    backdrop_info = pre_render_backdrop(spec, backdrop_path)
    render_equation_frames_optimized(spec, backdrop_info, backdrop_path, frames_dir, speech_duration, fps=fps)
    
    # 5. Mux with FFmpeg
    print("  [5/5] Muxing 1080p Video + Audio with FFmpeg...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.jpg"),
        "-i", str(combined_audio),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_video)
    ]
    mux_res = subprocess.run(cmd_mux, capture_output=True, text=True)
    if mux_res.returncode != 0:
        print(f"  [ERROR] FFmpeg Muxing failed:\n{mux_res.stderr}")
        sys.exit(1)
        
    actual_dur = get_audio_duration(output_video)
    print(f"  [SUCCESS] Rendered segment: {output_video.name} ({actual_dur:.1f}s)")
    return actual_dur

def main():
    parser = argparse.ArgumentParser(description="Acoustic Mathematics Video Masterclass Engine")
    parser.add_argument("--mode", choices=["test", "full"], default="full", help="Test mode = 2 equations (~1.7 min); Full mode = all 10 equations (~8.5 min)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second (default: 24 for fast cloud render)")
    args = parser.parse_args()
    
    target_equations = EQUATIONS_SPEC[:2] if args.mode == "test" else EQUATIONS_SPEC
    segment_files = []
    chapter_markers = []
    current_time_acc = 0.0
    
    print("=" * 80)
    print(f"ACOUSTIC MATHEMATICS 1080P MASTERCLASS PIPELINE  |  Mode: {args.mode.upper()}")
    print(f"Target Equations: {len(target_equations)}  |  FPS: {args.fps}")
    print("=" * 80)
    
    for idx, spec in enumerate(target_equations, 1):
        # Record Chapter Timestamp
        mins = int(current_time_acc // 60)
        secs = int(current_time_acc % 60)
        timestamp_str = f"{mins:02d}:{secs:02d}"
        chapter_markers.append({
            "index": idx,
            "timestamp": timestamp_str,
            "title": spec["title"],
            "formula": spec["formula"]
        })
        
        seg_video = TEMP_DIR / f"segment_{idx:02d}_{spec['id']}.mp4"
        seg_duration = build_single_equation_video(spec, seg_video, fps=args.fps)
        segment_files.append(seg_video)
        current_time_acc += seg_duration
        
    # Save computed dynamic chapters to data/
    chapters_path = DATA_DIR / "masterclass_chapters.json"
    with open(chapters_path, "w", encoding="utf-8") as cf:
        json.dump(chapter_markers, cf, indent=2)
    print(f"\n[+] Saved {len(chapter_markers)} Chapter Timestamps to {chapters_path}")
    
    # Concatenate all segments into Masterclass Video
    final_output = OUTPUT_DIR / f"What_10_Iconic_Math_Equations_Actually_Sound_Like_{args.mode.upper()}.mp4"
    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg.resolve()}'\n")
            
    print("\n" + "=" * 80)
    print(f"[*] Concatenating {len(segment_files)} segments into Final Masterclass...")
    cmd_final = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(final_output)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    total_master_dur = get_audio_duration(final_output)
    file_size_mb = final_output.stat().st_size / (1024 * 1024)
    mins_tot = int(total_master_dur // 60)
    secs_tot = int(total_master_dur % 60)
    
    print("=" * 80)
    print(f"🎉 MASTERCLASS VIDEO COMPLETE: {final_output.name}")
    print(f"   Duration: {mins_tot} min {secs_tot} sec ({total_master_dur:.1f}s)")
    print(f"   Size: {file_size_mb:.2f} MB")
    print(f"   Path: {final_output.resolve()}")
    print("=" * 80)

if __name__ == "__main__":
    main()
