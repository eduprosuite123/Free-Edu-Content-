#!/usr/bin/env python3
"""
EduProSuite SOTA Zero-Shot User Cloned Voice Engine (2026 Edition)
==================================================================
Features:
- Primary Engine: F5-TTS (E2-F5 Flow-Matching Zero-Shot Voice Cloner)
- Reference Speaker: User's authentic recorded voice (data/user_raw_sample.wav)
- Accent: Authentic User Pitch & Timbre with USA/Global STEM English inflection
- Resilience Gate: Auto-fallback to Studio-Equalized Neural Voice if cloud space is queued/busy
- Zero-Lag / Zero-Crash: Fully compatible with GitHub Actions Ubuntu runners and local systems
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"

REF_AUDIO_PATH = DATA_DIR / "user_raw_sample.wav"
REF_TRANSCRIPT = "An equation which is in the form a x squared plus b x plus c equals zero is called quadratic equation"

FALLBACK_VOICE = "en-IN-PrabhatNeural"
FALLBACK_RATE = "-3%"
FALLBACK_PITCH = "+1Hz"

STUDIO_FILTER = (
    "equalizer=f=250:width_type=o:w=1.2:g=1.5,"
    "equalizer=f=2800:width_type=o:w=1.0:g=1.5,"
    "acompressor=threshold=-16dB:ratio=2.5:attack=15:release=120,"
    "loudnorm=I=-16:TP=-1.0:LRA=9"
)

def get_ffmpeg_bin() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def _apply_studio_mastering(input_audio: Path, output_audio: Path):
    ff = get_ffmpeg_bin()
    cmd = [
        ff, "-y", "-i", str(input_audio),
        "-af", STUDIO_FILTER,
        "-ar", "44100",
        str(output_audio)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        import shutil
        print(f"[!] Warning: FFmpeg studio mastering failed ({e}), using raw voice file directly.")
        shutil.copy2(input_audio, output_audio)

def synthesize_user_cloned_voice(text: str, output_path: str | Path) -> Path:
    """
    Synthesizes speech using the user's authentic F5-TTS cloned voice (USA/Global Accent).
    Falls back gracefully to Edge-TTS if remote GPU is busy or network fails.
    """
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Attempt Primary Engine: F5-TTS Zero-Shot Clone
    if REF_AUDIO_PATH.exists():
        try:
            print("[+] Synthesizing 100% authentic USA-accented user voice with F5-TTS...")
            from gradio_client import Client, handle_file
            
            hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
            client = Client("mrfakename/E2-F5-TTS", hf_token=hf_token) if hf_token else Client("mrfakename/E2-F5-TTS")
            result_wav = client.predict(
                ref_audio=handle_file(str(REF_AUDIO_PATH)),
                ref_text=REF_TRANSCRIPT,
                gen_text=text,
                remove_silence=False,
                api_name="/predict"
            )
            
            _apply_studio_mastering(Path(result_wav), out_file)
            print(f"[SUCCESS] Authentic user cloned voice synthesized: {out_file} ({out_file.stat().st_size} bytes)")
            return out_file
        except Exception as e:
            print(f"[WARN] F5-TTS remote synthesis encountered ({e}). Engaging high-grade Studio fallback...")
    else:
        print(f"[WARN] Reference audio {REF_AUDIO_PATH} not found. Using fallback engine...")

    # 2. Resilient Fallback Engine: Tuned Edge-TTS with Studio HD EQ
    import edge_tts
    async def _run_fallback():
        raw_path = out_file.with_suffix(".fallback.mp3")
        comm = edge_tts.Communicate(text, FALLBACK_VOICE, rate=FALLBACK_RATE, pitch=FALLBACK_PITCH)
        await comm.save(str(raw_path))
        _apply_studio_mastering(raw_path, out_file)
        if raw_path.exists():
            raw_path.unlink()
            
    asyncio.run(_run_fallback())
    print(f"[SUCCESS] Fallback studio voice synthesized: {out_file} ({out_file.stat().st_size} bytes)")
    return out_file

async def synthesize_user_cloned_voice_async(text: str, output_path: str | Path) -> Path:
    return synthesize_user_cloned_voice(text, output_path)

if __name__ == "__main__":
    test_out = OUTPUT_DIR / "test_cloned_engine_sample.mp3"
    synthesize_user_cloned_voice(
        "Welcome to EduProSuite higher mathematics. Today we master advanced 3D calculus.",
        test_out
    )
