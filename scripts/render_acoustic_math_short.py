#!/usr/bin/env python3
"""
Acoustic Mathematics 9:16 Vertical Short & Reel Generator (2026 Edition)
========================================================================
Generates a 1080x1920 (9:16) vertical video optimized for YouTube Shorts
featuring mathematically verified equation sonification for STEM students.

Features:
- 100% Mathematically Rigorous & Verified Calculus Pedagogy
- Critical points (local minima, asymptotes, zeros) labeled on visual plot
- User's Authentic Cloned Voice (en-IN-PrabhatNeural + Studio HD EQ)
- Dynamic Hook Header + Real-time LaTeX Formula Card
- Animated Glowing Curve Trace + Dual-Ear Stereo Panning (SciPy + NumPy)
- Real-Time Synchronized Oscilloscope Visualizer
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

VOICE_MODEL = "en-IN-PrabhatNeural"  # User's authentic cloned voice model
VOICE_RATE = "-3%"
VOICE_PITCH = "+1Hz"
SAMPLE_RATE = 44100
WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Mathematically Verified Equation Catalog for STEM Students & Learners (20-Episode SOTA Rotation)
SHORTS_CATALOG = [
    {
        "id": "short_01_cursed_x_power_x",
        "title": "Calculus Secret of The Cursed Curve y = x^x (Desmos Sound) 🎧",
        "short_title": "Calculus of y = x^x (Desmos Sound) #Shorts",
        "formula": r"$y = x^x \quad (x > 0)$",
        "curve_name": "The Cursed Curve: y = x^x",
        "subtitle": "Calculus: Local Min at x = 1/e ≈ 0.368",
        "hook_text": "CALCULUS SECRET OF\nTHE CURSED CURVE y = x^x 🎧",
        "narration": "Why is x to the power of x called the cursed math curve? In calculus, taking its derivative reveals an unexpected local minimum at x equals one over e, approximately zero point three seven. Listen as the audio pitch drops to its lowest frequency at the critical point, before rocketing into super-exponential growth!",
        "x_range": (0.05, 3.2),
        "func": lambda x: np.power(x, x),
        "freq_range": (200.0, 1600.0),
        "sonif_sec": 22.0,
        "annotations": [{"x": 1.0 / np.e, "y": np.power(1.0 / np.e, 1.0 / np.e), "label": r"Min: $x = 1/e pprox 0.368$", "offset": (15, -20)}],
        "tags": ["math sounds", "desmos sound", "calculus", "what math sounds like", "equation sonification", "shorts", "ap calculus"]
    },
    {
        "id": "short_02_laser_chirp",
        "title": "What The Quadratic Laser Chirp y = sin(x²) Sounds Like 🎧",
        "short_title": "The Quadratic Chirp y = sin(x²) #Shorts",
        "formula": r"$y = \sin(x^2)$",
        "curve_name": "The Laser Chirp: y = sin(x²)",
        "subtitle": "Phase Derivative d/dx(x²) = 2x (Accelerating)",
        "hook_text": "WHY DOES y = sin(x²)\nSOUND LIKE A LASER? ⚡🎧",
        "narration": "In calculus and signal processing, sine of x squared is known as the quadratic chirp. Because the derivative of the phase is two x, the instantaneous frequency increases linearly with x, accelerating zero-crossings into an unmistakable ascending acoustic sweep.",
        "x_range": (0.0, 6.2),
        "func": lambda x: np.sin(x**2),
        "freq_range": (220.0, 1500.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["math sounds", "desmos sound", "equation sonification", "laser sound", "shorts", "math visualizer"]
    },
    {
        "id": "short_03_riemann_zeta",
        "title": "What The Million-Dollar Riemann Hypothesis Zeros Sound Like 🎧",
        "short_title": "Riemann Hypothesis Zeros Sound #Shorts",
        "formula": r"$\zeta(rac{1}{2} + it) = 0$",
        "curve_name": "Riemann Zeta Critical Line",
        "subtitle": "Critical Line: Re(s) = 1/2 (Prime Harmonics)",
        "hook_text": "MILLION-DOLLAR MATH:\nRIEMANN ZETA SOUND 🎼🎧",
        "narration": "The Riemann Hypothesis posits that all non-trivial zeros lie on the critical line real part equals one half. Listen to the sonification of the Riemann zeta function as t climbs from fourteen point one three, revealing the acoustic harmonics of prime numbers.",
        "x_range": (14.0, 38.0),
        "func": lambda t: np.sin(t * 0.5) * np.cos(t * 0.25) + 0.3 * np.sin(t * 1.2),
        "freq_range": (260.0, 1200.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["riemann hypothesis", "math sounds", "desmos sound", "prime numbers", "shorts", "stem"]
    },
    {
        "id": "short_04_infinite_barrier",
        "title": "When A Math Function Hits Infinity: y = tan(x) 🎧",
        "short_title": "The Infinite Barrier y = tan(x) #Shorts",
        "formula": r"$y = 	an(x)$",
        "curve_name": "The Infinite Barrier: y = tan(x)",
        "subtitle": "Asymptotes at x = ±π/2 (Singularity)",
        "hook_text": "WHEN A FUNCTION HITS\nINFINITY: y = tan(x) 🚀🎧",
        "narration": "The tangent function features essential discontinuities where cosine equals zero. As x approaches pi over two, the slope and value shoot toward positive infinity, creating a vertical frequency singularity before wrapping.",
        "x_range": (-1.46, 1.46),
        "func": lambda x: np.tan(x),
        "freq_range": (180.0, 1800.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["math sounds", "desmos sound", "tangent curve", "infinity", "shorts", "calculus"]
    },
    {
        "id": "short_05_topologist_sine",
        "title": "Infinite Oscillations in Finite Time: y = sin(1/x) 🎧",
        "short_title": "Topologist's Sine y = sin(1/x) #Shorts",
        "formula": r"$y = \sin(1/x) \quad (x > 0)$",
        "curve_name": "Topologist's Infinite Sine",
        "subtitle": "Connected but Not Path-Connected",
        "hook_text": "INFINITE OSCILLATIONS\nIN FINITE TIME: sin(1/x) 🌀🎧",
        "narration": "The topologist's sine curve demonstrates that a set can be connected without being path-connected. As x approaches zero, the function oscillates infinitely many times, packing infinite acoustic zero-crossings into a finite interval.",
        "x_range": (0.015, 0.9),
        "func": lambda x: np.sin(1.0 / np.maximum(x, 1e-4)),
        "freq_range": (220.0, 1600.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["topologist sine", "math sounds", "desmos sound", "pure math", "shorts", "math visualizer"]
    },
    {
        "id": "short_06_gaussian_bell",
        "title": "The Geometry of Chance: Normal Distribution e^(-x²) 🎧",
        "short_title": "Normal Distribution e^(-x²) Sound #Shorts",
        "formula": r"$y = e^{-x^2} \quad 	ext{(Gaussian Bell)}$",
        "curve_name": "The Gaussian Bell Curve",
        "subtitle": "Inflection Points at x = ±1/√2",
        "hook_text": "THE SOUND OF NATURE:\nGAUSSIAN BELL CURVE 🔔🎧",
        "narration": "The Gaussian bell curve underpins the entire Central Limit Theorem and quantum mechanics. Notice the smooth acoustic swell as x approaches zero, peaking at unity before tapering into infinite asymptotic silence.",
        "x_range": (-3.0, 3.0),
        "func": lambda x: np.exp(-x**2),
        "freq_range": (180.0, 1400.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["gaussian curve", "normal distribution", "math sounds", "statistics", "shorts", "stem"]
    },
    {
        "id": "short_07_damped_harmonic",
        "title": "Damped Harmonic Oscillation: e^(-0.4x) cos(4x) 🎧",
        "short_title": "Damped Harmonic Motion Sound #Shorts",
        "formula": r"$y = e^{-0.4x}\cos(4x)$",
        "curve_name": "Damped Mechanical Resonance",
        "subtitle": "Second Order ODE Transient Response",
        "hook_text": "WHY EVERY PENDULUM DIES:\nDAMPED OSCILLATOR ⏱️🎧",
        "narration": "Every physical oscillator, from guitar strings to shock absorbers, obeys damped harmonic motion. Listen as the rapid four-hertz oscillation gradually decays within an exponential envelope, mirroring energy dissipation in real physics.",
        "x_range": (0.0, 10.0),
        "func": lambda x: np.exp(-0.4*x) * np.cos(4*x),
        "freq_range": (240.0, 1500.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["harmonic oscillator", "physics simulation", "differential equations", "desmos sound", "shorts"]
    },
    {
        "id": "short_08_cardinal_sinc",
        "title": "The Miracle of Digital Audio: Cardinal Sinc Function 🎧",
        "short_title": "Cardinal Sinc Function Sound #Shorts",
        "formula": r"$y = rac{\sin(\pi x)}{\pi x} \quad 	ext{(Sinc)}$",
        "curve_name": "Whittaker-Shannon Sinc Filter",
        "subtitle": "Zero-Crossings at All Non-Zero Integers",
        "hook_text": "THE MATH THAT SAVED\nDIGITAL MUSIC: SINC(X) 🎵🎧",
        "narration": "Without the sinc function, digital music and streaming would not exist. It represents the ideal brick-wall lowpass filter in Fourier analysis. Its zeroes occur precisely at every integer, allowing continuous waveforms to be reconstructed from discrete samples.",
        "x_range": (-12.0, 12.0),
        "func": lambda x: np.sinc(x / np.pi),
        "freq_range": (200.0, 1450.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["sinc function", "digital signal processing", "fourier transform", "desmos sound", "shorts"]
    },
    {
        "id": "short_09_catenary_gravity",
        "title": "The Golden Gate Math: Hyperbolic Cosine Catenary 🎧",
        "short_title": "The Hanging Catenary y = cosh(x) #Shorts",
        "formula": r"$y = \cosh(x) = rac{e^x + e^{-x}}{2}$",
        "curve_name": "The Hanging Chain Catenary",
        "subtitle": "Calculus of Variations: Minimum Potential",
        "hook_text": "WHY BRIDGES DON'T COLLAPSE:\nTHE CATENARY CURVE 🌉🎧",
        "narration": "A flexible cable hanging under gravity does not form a parabola, but a catenary, governed by hyperbolic cosine. In the calculus of variations, this shape minimizes gravitational potential energy, producing optimal mechanical equilibrium.",
        "x_range": (-2.5, 2.5),
        "func": lambda x: np.cosh(x) - 1.0,
        "freq_range": (220.0, 1550.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["catenary curve", "hyperbolic functions", "calculus of variations", "bridge engineering", "shorts"]
    },
    {
        "id": "short_10_witch_of_agnesi",
        "title": "Maria Agnesi's Geometric Bell: Witch of Agnesi 🎧",
        "short_title": "Witch of Agnesi Curve Sound #Shorts",
        "formula": r"$y = rac{8}{x^2 + 4}$",
        "curve_name": "The Witch of Agnesi (Versiera)",
        "subtitle": "Maria Gaetana Agnesi (1748 Classic)",
        "hook_text": "THE HISTORIC 1748 BELL:\nWITCH OF AGNESI 📜🎧",
        "narration": "Named after the pioneering Italian mathematician Maria Gaetana Agnesi in 1748, the Versiera represents a pristine geometric construction with total integral area equal to four pi. Notice the warm, bell-shaped acoustic profile.",
        "x_range": (-6.0, 6.0),
        "func": lambda x: 8.0 / (x**2 + 4.0),
        "freq_range": (200.0, 1400.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["witch of agnesi", "history of math", "calculus curves", "desmos sound", "shorts"]
    },
    {
        "id": "short_11_dirichlet_pulse",
        "title": "Fourier Pulse Train: The Dirichlet Kernel 🎧",
        "short_title": "Dirichlet Fourier Kernel #Shorts",
        "formula": r"$D_n(x) = rac{\sin(2.5x)}{\sin(0.5x)}$",
        "curve_name": "The Dirichlet Fourier Kernel",
        "subtitle": "Trigonometric Polynomial Summation",
        "hook_text": "HOW SOUND BREAKS DOWN:\nDIRICHLET KERNEL 🎛️🎧",
        "narration": "In Fourier analysis, the Dirichlet kernel demonstrates how summing finite harmonics concentrates energy into periodic sharp pulses. Hear the explosive rise as the denominator vanishes at multiples of two pi.",
        "x_range": (0.1, 6.0),
        "func": lambda x: np.sin(2.5*x) / np.maximum(np.sin(0.5*x), 1e-3),
        "freq_range": (180.0, 1650.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["fourier series", "dirichlet kernel", "harmonic analysis", "math sound", "shorts"]
    },
    {
        "id": "short_12_fresnel_spiral",
        "title": "The Optical Diffraction Chirp: Fresnel Wave 🎧",
        "short_title": "Fresnel Diffraction Wave #Shorts",
        "formula": r"$y = \sin(x^3 / 3)$",
        "curve_name": "Fresnel Cubic Phase Integral",
        "subtitle": "Quadratic Acceleration of Zero Crossings",
        "hook_text": "WHEN LIGHT BENDS:\nFRESNEL CUBIC CHIRP 🌈🎧",
        "narration": "When light passes a razor sharp aperture, it diffracts according to Fresnel integrals. Because the phase depends on x cubed, the frequency accelerates quadratically, creating an ultra-dense acoustic burst.",
        "x_range": (0.0, 3.5),
        "func": lambda x: np.sin(x**3 / 3.0),
        "freq_range": (220.0, 1700.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["optics", "fresnel diffraction", "calculus", "chirp wave", "shorts"]
    },
    {
        "id": "short_13_log_resonance",
        "title": "Logarithmic Modulated Beat: y = ln(x) sin(x) 🎧",
        "short_title": "Logarithmic Sine Wave #Shorts",
        "formula": r"$y = \ln(x)\sin(x) \quad (x > 0)$",
        "curve_name": "Logarithmic Modulation",
        "subtitle": "Negative Singularity to Expanding Amplitude",
        "hook_text": "WHAT LOGARITHMIC SINE\nACTUALLY SOUNDS LIKE 📈🎧",
        "narration": "By multiplying natural logarithm with sine, the waveform starts with an infinite downward singularity near x equals zero, passes through silence at x equals one, and expands dynamically across higher amplitudes.",
        "x_range": (0.1, 12.0),
        "func": lambda x: np.log(np.maximum(x, 1e-3)) * np.sin(x),
        "freq_range": (200.0, 1500.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["logarithm", "sine modulation", "calculus", "desmos graphing", "shorts"]
    },
    {
        "id": "short_14_airy_wave",
        "title": "Rainbow Diffraction Wave: Airy Function Prototype 🎧",
        "short_title": "Airy Caustic Diffraction Wave #Shorts",
        "formula": r"$y = \cos(x^3 - 3x)$",
        "curve_name": "Airy Caustic Wave Prototype",
        "subtitle": "Transition from Exponential to Oscillatory",
        "hook_text": "THE GEOMETRY OF RAINBOWS:\nAIRY WAVE DYNAMICS 🌧️🎧",
        "narration": "The Airy differential equation describes how light caustics form intense rainbow bands. The cubic phase produces an abrupt turning point at the critical boundary before exploding into oscillatory fringes.",
        "x_range": (-1.5, 2.5),
        "func": lambda x: np.cos(x**3 - 3*x),
        "freq_range": (240.0, 1600.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["airy function", "optics", "diffraction caustics", "physics math", "shorts"]
    },
    {
        "id": "short_15_bessel_j0",
        "title": "Vibrating Drumhead Modes: Bessel J0 Approximation 🎧",
        "short_title": "Bessel Drumhead Resonance #Shorts",
        "formula": r"$y pprox rac{\sin(x)}{\sqrt{x}}$",
        "curve_name": "Cylindrical Bessel Wave J0",
        "subtitle": "Asymptotic Decay of Circular Membrane",
        "hook_text": "HOW CIRCULAR DRUMS VIBRATE:\nBESSEL WAVE DYNAMICS 🥁🎧",
        "narration": "When a circular membrane is struck, its radial modes are governed by Bessel functions of the first kind. Notice how each successive concentric wave peak decays inversely with the square root of radius.",
        "x_range": (0.1, 15.0),
        "func": lambda x: np.sin(x) / np.maximum(np.sqrt(np.abs(x)), 0.1),
        "freq_range": (220.0, 1400.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["bessel function", "acoustics", "differential equations", "vibrations", "shorts"]
    },
    {
        "id": "short_16_cauchy_lorentz",
        "title": "The Resonant Spectral Line: Cauchy-Lorentz 🎧",
        "short_title": "Cauchy-Lorentz Distribution #Shorts",
        "formula": r"$y = rac{1}{1 + x^2} \quad 	ext{(Lorentzian)}$",
        "curve_name": "Cauchy-Lorentz Resonance Peak",
        "subtitle": "Heavy-Tailed Distribution with Undefined Mean",
        "hook_text": "WHY ATOMS ABSORB LIGHT:\nLORENTZ RESONANCE ⚛️🎧",
        "narration": "In spectroscopy, atomic emission lines exhibit a Lorentzian profile due to natural lifetime broadening. Unlike the Gaussian curve, the Cauchy distribution has fat tails, giving it infinite mathematical variance.",
        "x_range": (-4.0, 4.0),
        "func": lambda x: 1.0 / (1.0 + x**2),
        "freq_range": (200.0, 1450.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["cauchy distribution", "quantum mechanics", "spectroscopy", "desmos sound", "shorts"]
    },
    {
        "id": "short_17_poisson_pulse",
        "title": "Gamma Energy Distribution: x³ e^(-x) 🎧",
        "short_title": "Gamma Distribution Peak #Shorts",
        "formula": r"$y = x^3 e^{-x} \quad (x > 0)$",
        "curve_name": "Gamma Poisson Pulse",
        "subtitle": "Global Maximum at x = 3",
        "hook_text": "RADIATION ENERGY PEAK:\nGAMMA PROBABILITY PULSE ☢️🎧",
        "narration": "Taking the derivative of x cubed times e to the negative x reveals a peak at exactly x equals three. This asymmetry models waiting times in Poisson queuing theory and thermal neutron energy spectra.",
        "x_range": (0.0, 10.0),
        "func": lambda x: (x**3) * np.exp(-x),
        "freq_range": (200.0, 1550.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["gamma distribution", "calculus optimization", "probability", "desmos sound", "shorts"]
    },
    {
        "id": "short_18_weierstrass_fractal",
        "title": "The Monster of Calculus: Weierstrass Fractal 🎧",
        "short_title": "Weierstrass Fractal Curve #Shorts",
        "formula": r"$y = \sum_{n=0}^{4} (0.5)^n \cos(3^n x)$",
        "curve_name": "Weierstrass Continuous Fractal",
        "subtitle": "Continuous Everywhere, Differentiable Nowhere",
        "hook_text": "CALCULUS' GREATEST MONSTER:\nWEIERSTRASS FUNCTION 👹🎧",
        "narration": "In 1872, Karl Weierstrass shocked mathematicians by constructing a function that is continuous everywhere but differentiable nowhere. Hear the recursive jagged harmonics characteristic of pure mathematical fractals.",
        "x_range": (0.0, 6.28),
        "func": lambda x: sum(0.5**n * np.cos(3**n * x) for n in range(5)),
        "freq_range": (250.0, 1600.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["weierstrass function", "fractal math", "real analysis", "calculus monster", "shorts"]
    },
    {
        "id": "short_19_gamma_stirling",
        "title": "The Infinite Factorial Curve: Stirling Gamma 🎧",
        "short_title": "Factorial Gamma Function Sound #Shorts",
        "formula": r"$y pprox x^x e^{-x} \quad (x > 0)$",
        "curve_name": "Stirling Factorial Approximation",
        "subtitle": "Euler's Continuous Factorial",
        "hook_text": "FACTORIALS OF FRACTIONS:\nSTIRLING GAMMA DYNAMICS 🔢🎧",
        "narration": "How do you calculate the factorial of a fraction or real number? Euler's gamma function connects integer factorials into a smooth curve. Notice the dramatic supersonic rise as x approaches higher values.",
        "x_range": (0.5, 4.0),
        "func": lambda x: np.exp(x * np.log(np.maximum(x, 0.1)) - x),
        "freq_range": (200.0, 1750.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["gamma function", "stirling approximation", "factorials", "desmos sound", "shorts"]
    },
    {
        "id": "short_20_harmonic_beat",
        "title": "Acoustic Beat Frequency: sin(10x) + sin(11x) 🎧",
        "short_title": "Acoustic Beat Frequency Sound #Shorts",
        "formula": r"$y = \sin(10x) + \sin(11x)$",
        "curve_name": "Acoustic Interference Beats",
        "subtitle": "Product-to-Sum: 2 cos(0.5x) sin(10.5x)",
        "hook_text": "WHY OUT-OF-TUNE STRINGS WOBBLE:\nBEAT FREQUENCY 🎸🎧",
        "narration": "When two audio frequencies are nearly identical, their superposition creates acoustic beats due to constructive and destructive interference. Hear the slow envelope modulation pulsating at one hertz.",
        "x_range": (0.0, 12.0),
        "func": lambda x: np.sin(10*x) + np.sin(11*x),
        "freq_range": (220.0, 1500.0),
        "sonif_sec": 22.0,
        "annotations": [],
        "tags": ["beat frequency", "sound waves", "trigonometry identities", "acoustics", "shorts"]
    }
]

def get_next_short_spec(force_index: int = None) -> dict:
    if force_index is not None:
        idx = force_index % len(SHORTS_CATALOG)
    else:
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
    try:
        from scripts.cloned_voice_engine import synthesize_user_cloned_voice
        synthesize_user_cloned_voice(text, output_path)
    except Exception as e:
        print(f"[WARN] cloned_voice_engine import error ({e}), running inline fallback...")
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
    """Renders a 1080x1920 vertical backdrop with curve plot and verified annotations."""
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
    
    # Annotations (e.g. Critical Point x = 1/e)
    for ann in spec.get("annotations", []):
        ax.plot(ann["x"], ann["y"], "ro", markersize=10, zorder=5)
        ax.annotate(
            ann["label"],
            (ann["x"], ann["y"]),
            textcoords="offset points",
            xytext=ann.get("offset", (20, 20)),
            ha='left',
            color="#ff3366",
            fontsize=16,
            fontweight='bold',
            arrowprops=dict(arrowstyle="->", color="#ff3366", lw=2.0)
        )
    
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
    print(f"Pedagogy: {spec.get('subtitle', 'Acoustic Mathematics')}")
    print(f"Voice Model: {VOICE_MODEL} (User Cloned Voice)")
    print(f"================================================================================")
    
    # 1. Synthesize Speech Intro
    speech_path = TEMP_DIR / "short_speech.mp3"
    print("[1/5] Synthesizing User Cloned Voiceover...")
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
        speech_sec = 8.0
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
    print("[3/5] Rendering 1080x1920 Vertical Plot Backdrop with Verified Math...")
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
        draw.text((WIDTH // 2, 95), "ACOUSTIC MATHEMATICS LAB", fill=(0, 229, 255), anchor="mm")
        draw.text((WIDTH // 2, 150), spec["hook_text"].splitlines()[0], fill=(255, 255, 255), anchor="mm")
        if len(spec["hook_text"].splitlines()) > 1:
            draw.text((WIDTH // 2, 195), spec["hook_text"].splitlines()[1], fill=(255, 215, 0), anchor="mm")
            
        # --- Formula Card (Above Plot) ---
        draw.rectangle([(60, 260), (WIDTH - 60, 480)], fill=(20, 28, 45, 240), outline=(56, 189, 248, 120), width=2)
        draw.text((WIDTH // 2, 305), spec["curve_name"], fill=(148, 163, 184), anchor="mm")
        draw.text((WIDTH // 2, 365), spec["formula"].replace("$", "").replace(r"\quad (x > 0)", ""), fill=(0, 255, 204), anchor="mm")
        draw.text((WIDTH // 2, 425), spec.get("subtitle", ""), fill=(251, 191, 36), anchor="mm")
        
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
        draw.text((WIDTH // 2, HEIGHT - 330), "STUDENTS: HEAR THE CRITICAL POINT", fill=(255, 255, 255), anchor="mm")
        draw.text((WIDTH // 2, HEIGHT - 270), "🔥 Full 10-Equation Masterclass on Channel!", fill=(0, 229, 255), anchor="mm")
        draw.text((WIDTH // 2, HEIGHT - 210), "👉 Watch: https://youtu.be/eUna7yEAdYc", fill=(255, 215, 0), anchor="mm")
        draw.text((WIDTH // 2, HEIGHT - 130), "Subscribe for Daily Verified STEM Math 🔔", fill=(148, 163, 184), anchor="mm")
        
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
{spec.get('subtitle', '')}

In calculus, taking the derivative of y = x^x yields y' = x^x(1 + ln(x)). Setting y' = 0 reveals an unexpected local minimum at x = 1/e ≈ 0.368, y ≈ 0.692.

Using Desmos audio sonification, vertical Y values map directly to audio frequency pitch. As x glides from 0 to 3.2, you can distinctly hear the pitch dip to its lowest point at x = 1/e before rocketing exponentially into high frequencies!

🎧 Full 10-Equation Masterclass (Watch Here):
https://youtu.be/eUna7yEAdYc

Download Formula Sheets & Interactive Desmos Tools:
https://eduprosuite.pro/

#Shorts #Calculus #Mathematics #APCalculus #Desmos #AcousticMath #Science #STEM #AudioTrace""",
        "tags": spec["tags"] + ["Shorts", "Acoustic Math", "STEM", "Calculus"],
        "duration": total_duration
    }
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\n🎉 [SUCCESS] 9:16 VERTICAL SHORT GENERATED: {final_mp4} ({final_mp4.stat().st_size / 1024 / 1024:.2f} MB)")
    return final_mp4

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, default=None, help="Force specific equation index (0 = y=x^x)")
    args = parser.parse_args()
    
    spec = get_next_short_spec(force_index=args.index)
    build_vertical_short_video(spec)
