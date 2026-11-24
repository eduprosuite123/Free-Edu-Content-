#!/usr/bin/env python3
"""
Acoustic Mathematics & Equation Sonification Engine (2026 Edition)
=================================================================
Automated Headless 1080p Landscape (16:9) Video & Audio Generator
for YouTube Long-Form Content & Desmos Audio Trace Accessibility.

Engineered for 100% cloud execution on GitHub Actions (Ubuntu/Linux).
Zero local GUI dependency (Matplotlib Agg backend + SciPy + Edge-TTS + FFmpeg).
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

VOICE_MODEL = "en-GB-RyanNeural"  # Official UK Academic Tone

# 10 Iconic Equations Specification
EQUATIONS_SPEC = [
    {
        "id": "eq01_pure_sine",
        "title": "1. Pure Harmonic Oscillation: y = sin(x)",
        "formula": r"$y = \sin(x)$",
        "description": "The fundamental building block of all sound in the universe. In Desmos audio trace, this produces a pristine, continuous sinusoidal frequency at concert pitch A440.",
        "narration": "Equation one. The pure sine wave. In mathematical sonification, this is the foundational acoustic baseline. As x glides from left to right, the pitch traces a smooth, continuous sinusoidal tone.",
        "x_range": (-2 * np.pi, 2 * np.pi),
        "func": lambda x: np.sin(x),
        "base_freq": 440.0,
        "freq_range": (300.0, 580.0),
        "duration_sec": 12.0
    },
    {
        "id": "eq02_x_power_x",
        "title": "2. The Cursed Curve: y = x^x",
        "formula": r"$y = x^x \quad (x > 0)$",
        "description": "Known as the cursed Desmos equation. Near zero, the slope reverses, before rocketing into hyper-exponential growth, shooting audio into the ultrasonic register.",
        "narration": "Equation two. The infamous x to the power of x. Visually impaired mathematicians hear a distinct dip near one over e, followed by an aggressive exponential frequency climb into ultrasonic registers.",
        "x_range": (0.05, 3.2),
        "func": lambda x: np.power(x, x),
        "base_freq": 220.0,
        "freq_range": (180.0, 1600.0),
        "duration_sec": 14.0
    },
    {
        "id": "eq03_chirp_sine_sq",
        "title": "3. The Quadratic Chirp: y = sin(x^2)",
        "formula": r"$y = \sin(x^2)$",
        "description": "As x increases, the oscillation frequency accelerates quadratically. In radar and acoustics, this creates an ascending laser-like chirp.",
        "narration": "Equation three. Sine of x squared, known in audio engineering as the quadratic chirp. The zero crossings compress with extreme acceleration, producing an unmistakable ascending laser sweep.",
        "x_range": (0.0, 5.5),
        "func": lambda x: np.sin(x**2),
        "base_freq": 300.0,
        "freq_range": (200.0, 1400.0),
        "duration_sec": 14.0
    },
    {
        "id": "eq04_tan_asymptote",
        "title": "4. The Infinite Barrier: y = tan(x)",
        "formula": r"$y = \tan(x)$",
        "description": "The tangent function features vertical asymptotes at odd multiples of pi over two. The pitch shoots to infinity, followed by a sudden white-noise pop.",
        "narration": "Equation four. The tangent curve. As x approaches pi over two, the frequency races toward vertical infinity. In accessibility screen readers, the sudden discontinuity registers as a sharp acoustic break.",
        "x_range": (-1.45, 1.45),
        "func": lambda x: np.tan(x),
        "base_freq": 400.0,
        "freq_range": (150.0, 1800.0),
        "duration_sec": 14.0
    },
    {
        "id": "eq05_sinc_function",
        "title": "5. The Sinc Function: y = sin(x)/x",
        "formula": r"$y = \frac{\sin(x)}{x} \quad (\mathrm{sinc})$",
        "description": "The cardinal sine function is the bedrock of digital signal reconstruction and the Nyquist-Shannon sampling theorem. It produces a decaying acoustic reverberation.",
        "narration": "Equation five. The cardinal sinc function. Central to the Nyquist-Shannon sampling theorem, its audio trace forms a powerful central resonance flanked by dampening acoustic ripples.",
        "x_range": (-15.0, 15.0),
        "func": lambda x: np.where(np.abs(x) < 1e-9, 1.0, np.sin(x) / x),
        "base_freq": 440.0,
        "freq_range": (250.0, 880.0),
        "duration_sec": 14.0
    },
    {
        "id": "eq06_topologist_sine",
        "title": "6. The Topologist's Sine Curve: y = sin(1/x)",
        "formula": r"$y = \sin(1/x) \quad (x > 0)$",
        "description": "As x approaches zero, the oscillations become infinitely dense. It is connected but not path-connected, creating an acoustic swarm of micro-frequencies.",
        "narration": "Equation six. The topologist's sine curve. Near zero, the function undergoes infinite oscillations within a finite interval, creating an acoustic density wave that challenges continuous perception.",
        "x_range": (0.02, 1.0),
        "func": lambda x: np.sin(1.0 / np.maximum(x, 1e-4)),
        "base_freq": 400.0,
        "freq_range": (200.0, 1500.0),
        "duration_sec": 14.0
    },
    {
        "id": "eq07_riemann_zeta",
        "title": "7. Riemann Zeta Critical Zeros: Re(s) = 1/2",
        "formula": r"$\zeta(\frac{1}{2} + it) = 0$",
        "description": "The million-dollar Millennium Prize problem. The non-trivial zeros lie on the critical line at t = 14.13, 21.02, 25.01, creating harmonic quantum acoustic nodes.",
        "narration": "Equation seven. The non-trivial zeros of the Riemann Zeta function. The critical line zeroes at fourteen point one three and twenty-one point zero two generate profound harmonic resonance resembling quantum energy levels.",
        "x_range": (10.0, 32.0),
        "func": lambda t: np.sin(t * np.log(t / (2 * np.pi)) - t - np.pi / 8),
        "base_freq": 350.0,
        "freq_range": (180.0, 950.0),
        "duration_sec": 16.0
    },
    {
        "id": "eq08_tan_sin_cursed",
        "title": "8. The Razor Curve: y = tan(sin(x))",
        "formula": r"$y = \tan(\sin(x))$",
        "description": "A bounded periodic composite curve with flattened plateau peaks and lightning-fast vertical inflection slopes, creating punchy square-like overtones.",
        "narration": "Equation eight. Tangent of sine of x. This composite function creates sharp, trapezoidal transitions, producing an aggressive, buzzy square-wave overtone that sounds like an analog modular synthesizer.",
        "x_range": (-2 * np.pi, 2 * np.pi),
        "func": lambda x: np.tan(np.sin(x)),
        "base_freq": 380.0,
        "freq_range": (200.0, 900.0),
        "duration_sec": 14.0
    },
    {
        "id": "eq09_golden_spiral",
        "title": "9. The Golden Logarithmic Spiral: r = e^(0.15*theta)",
        "formula": r"$r(\theta) = e^{0.15 \theta}$",
        "description": "The self-similar spiral found in nautilus shells and spiral galaxies. In stereo space, it produces an expanding binaural acoustic rotation.",
        "narration": "Equation nine. The golden logarithmic spiral. Governed by Euler's constant and self-similarity, its acoustic mapping creates an expansive binaural stereo rotation through human hearing space.",
        "x_range": (0.0, 4 * np.pi),
        "func": lambda th: np.exp(0.15 * th) * np.cos(th),
        "base_freq": 300.0,
        "freq_range": (220.0, 1100.0),
        "duration_sec": 16.0
    },
    {
        "id": "eq10_fourier_square",
        "title": "10. The Fourier Synthesis: 7 Odd Harmonics",
        "formula": r"$\sum_{k=1}^7 \frac{\sin((2k-1)x)}{2k-1}$",
        "description": "Adding odd harmonics of sine waves progressively morphs a pure tone into a crisp acoustic square wave, showing the Gibbs phenomenon overshoot at the edges.",
        "narration": "Equation ten. Fourier square wave synthesis. As we accumulate odd harmonics, the acoustic tone hardens, demonstrating how calculus reconstructs the square waves of modern digital computers.",
        "x_range": (-np.pi, np.pi),
        "func": lambda x: sum(np.sin((2*k-1)*x) / (2*k-1) for k in range(1, 8)),
        "base_freq": 320.0,
        "freq_range": (180.0, 1200.0),
        "duration_sec": 16.0
    }
]

async def generate_speech_audio(text: str, output_path: Path):
    """Synthesizes high-fidelity academic voiceover using Edge-TTS."""
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE_MODEL, rate="-3%", pitch="-1Hz")
    await communicate.save(str(output_path))

def synthesize_equation_audio(spec: dict, wav_path: Path, sample_rate: int = 44100):
    """
    Synthesizes exact stereo sonification matching Desmos Audio Trace standards:
    - Time maps to x-axis
    - Frequency maps to y-value
    - Stereo pan sweeps Left to Right
    """
    duration = spec["duration_sec"]
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
    base_signal = 0.7 * np.sin(phase) + 0.2 * np.sin(2 * phase) + 0.1 * np.sin(3 * phase)
    
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

def render_equation_frames(spec: dict, frames_dir: Path, fps: int = 30):
    """Renders exact constant 1920x1080 frames with 3Blue1Brown/Desmos aesthetic."""
    frames_dir.mkdir(parents=True, exist_ok=True)
    duration = spec["duration_sec"]
    total_frames = int(duration * fps)
    
    x_min, x_max = spec["x_range"]
    x_curve = np.linspace(x_min, x_max, 1000)
    y_curve = spec["func"](x_curve)
    y_curve = np.nan_to_num(y_curve, nan=0.0)
    
    y_pad = 0.25 * (np.max(y_curve) - np.min(y_curve) + 1e-4)
    ylim = (np.min(y_curve) - y_pad, np.max(y_curve) + y_pad)
    
    # Color Palette: Deep Slate Theme
    BG_COLOR = "#0c1017"
    GRID_COLOR = "#1e293b"
    TEXT_COLOR = "#f8fafc"
    CURVE_COLOR = "#38bdf8"
    CURSOR_COLOR = "#f43f5e"
    SPECTRUM_COLOR = "#10b981"
    
    for i in range(total_frames):
        current_progress = i / max(total_frames - 1, 1)
        current_x = x_min + current_progress * (x_max - x_min)
        current_y = spec["func"](current_x)
        if not np.isfinite(current_y):
            current_y = 0.0
            
        # Fixed exact dimensions: 19.2 x 10.8 inches at 100 DPI = exactly 1920x1080
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
        fig.patch.set_facecolor(BG_COLOR)
        
        # Grid layout: Main Graph (top 75%), Audio Spectrum Scope (bottom 25%)
        gs = fig.add_gridspec(2, 1, height_ratios=[3.5, 1.0], hspace=0.28, left=0.08, right=0.95, top=0.92, bottom=0.08)
        
        # Main Math Graph Axis
        ax_main = fig.add_subplot(gs[0])
        ax_main.set_facecolor(BG_COLOR)
        ax_main.grid(True, color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.7)
        ax_main.axhline(0, color="#475569", linewidth=1.2, alpha=0.9)
        ax_main.axvline(0, color="#475569", linewidth=1.2, alpha=0.9)
        
        # Plot full trace faintly
        ax_main.plot(x_curve, y_curve, color="#334155", linewidth=2.0, alpha=0.6)
        
        # Plot active trace up to current cursor
        mask = x_curve <= current_x
        if np.any(mask):
            ax_main.plot(x_curve[mask], y_curve[mask], color=CURVE_COLOR, linewidth=3.5, alpha=0.95)
            
        # Draw Tracing Cursor Dot
        ax_main.scatter([current_x], [current_y], color=CURSOR_COLOR, s=180, zorder=5, edgecolors="#ffffff", linewidth=2.0)
        
        # Header Info
        ax_main.set_title(spec["title"], fontsize=18, fontweight="bold", color=TEXT_COLOR, pad=18)
        ax_main.text(0.02, 0.90, f"Formula: {spec['formula']}", transform=ax_main.transAxes, fontsize=14, color="#38bdf8", bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec="#38bdf8", lw=1.2))
        ax_main.text(0.02, 0.78, f"Stereo Pan: {int(current_progress * 100)}% (L -> R)", transform=ax_main.transAxes, fontsize=11, color="#94a3b8")
        
        ax_main.set_xlim(x_min, x_max)
        ax_main.set_ylim(ylim)
        ax_main.tick_params(colors="#64748b", labelsize=10)
        for spine in ax_main.spines.values():
            spine.set_color("#334155")
            
        # Oscilloscope Spectrum Scope Axis
        ax_scope = fig.add_subplot(gs[1])
        ax_scope.set_facecolor("#080c12")
        ax_scope.grid(True, color="#1e293b", linestyle=":", linewidth=0.6, alpha=0.6)
        
        # Real-time synthetic waveform oscilloscope
        t_scope = np.linspace(0, 0.05, 300)
        f_norm = spec["freq_range"][0] + current_progress * (spec["freq_range"][1] - spec["freq_range"][0])
        scope_wave = np.sin(2 * np.pi * f_norm * t_scope) * (0.8 + 0.2 * np.sin(current_x))
        ax_scope.plot(t_scope, scope_wave, color=SPECTRUM_COLOR, linewidth=2.0)
        ax_scope.set_ylim(-1.3, 1.3)
        ax_scope.set_title(f"Acoustic Waveform Tracing  |  Current Pitch: {int(f_norm)} Hz  |  Time: {current_progress * duration:.1f}s / {duration:.1f}s", fontsize=11, color="#94a3b8", pad=6)
        ax_scope.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
        for spine in ax_scope.spines.values():
            spine.set_color("#1e293b")
            
        frame_path = frames_dir / f"frame_{i:05d}.png"
        fig.savefig(frame_path, facecolor=BG_COLOR, dpi=100)
        plt.close(fig)

def build_single_equation_video(spec: dict, output_video: Path, fps: int = 24):
    """Renders visuals and muxes with synthesized speech and sonification audio."""
    eq_id = spec["id"]
    work_dir = TEMP_DIR / eq_id
    work_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = work_dir / "frames"
    
    speech_mp3 = work_dir / "speech.mp3"
    sonif_wav = work_dir / "sonification.wav"
    combined_audio = work_dir / "combined_audio.wav"
    
    print(f"\n[*] Processing: {spec['title']}")
    
    # 1. Synthesize Educational Voiceover
    print("  [1/4] Generating Academic Voiceover (Edge-TTS)...")
    asyncio.run(generate_speech_audio(spec["narration"], speech_mp3))
    
    # 2. Synthesize Precise Audio Trace Sonification
    print("  [2/4] Synthesizing Acoustic Sonification (SciPy)...")
    synthesize_equation_audio(spec, sonif_wav)
    
    # 3. Concatenate Speech + Sonification
    print("  [3/4] Muxing Speech & Acoustic Trace Audio (FFmpeg)...")
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(speech_mp3),
        "-i", str(sonif_wav),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
        "-map", "[outa]",
        str(combined_audio)
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 4. Render Visual Frames & Mux to Final MP4
    print("  [4/4] Rendering 1080p Graph Tracing Frames & Muxing Video...")
    render_equation_frames(spec, frames_dir, fps=fps)
    
    cmd_mux = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-i", str(combined_audio),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_video)
    ]
    mux_res = subprocess.run(cmd_mux, capture_output=True, text=True)
    if mux_res.returncode != 0:
        print(f"  [ERROR] FFmpeg Muxing failed:\n{mux_res.stderr}")
        sys.exit(1)
        
    print(f"  [SUCCESS] Rendered segment: {output_video.name}")

def main():
    parser = argparse.ArgumentParser(description="Acoustic Mathematics Video Master Engine")
    parser.add_argument("--mode", choices=["test", "full"], default="test", help="Test mode renders 2 equations (~2 min); Full mode renders all 10 equations (~10 min)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second (default: 24 for fast cloud render)")
    args = parser.parse_args()
    
    target_equations = EQUATIONS_SPEC[:2] if args.mode == "test" else EQUATIONS_SPEC
    segment_files = []
    
    print("=" * 80)
    print(f"ACOUSTIC MATHEMATICS 1080P MASTER VIDEO PIPELINE  |  Mode: {args.mode.upper()}")
    print(f"Target Equations: {len(target_equations)}  |  FPS: {args.fps}")
    print("=" * 80)
    
    for idx, spec in enumerate(target_equations, 1):
        seg_video = TEMP_DIR / f"segment_{idx:02d}_{spec['id']}.mp4"
        build_single_equation_video(spec, seg_video, fps=args.fps)
        segment_files.append(seg_video)
        
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
    
    file_size_mb = final_output.stat().st_size / (1024 * 1024)
    print("=" * 80)
    print(f"[+] MASTERCLASS VIDEO COMPLETE: {final_output.name}")
    print(f"[+] Path: {final_output.resolve()}")
    print(f"[+] Size: {file_size_mb:.2f} MB")
    print("=" * 80)

if __name__ == "__main__":
    main()
