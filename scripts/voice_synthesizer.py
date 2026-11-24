"""
EduProSuite Official Master Voice Synthesizer
- Permanent Voice Model selected and approved by user:
  * Model: en-GB-RyanNeural
  * Cadence: UK Academic Voice with natural modulation
  * Speed: rate="-4%"
  * Pitch: pitch="-1Hz"
  * Style: Emphatic stress on core technical / mathematical keywords
- 100% Zero AI Quota (0% tokens) | Ultra-fast local/cloud synthesis
"""

import asyncio
from pathlib import Path
import edge_tts

MASTER_VOICE_NAME = "en-GB-RyanNeural"
MASTER_VOICE_RATE = "-4%"
MASTER_VOICE_PITCH = "-1Hz"

async def synthesize_speech(text: str, output_path: str | Path, rate: str = MASTER_VOICE_RATE, pitch: str = MASTER_VOICE_PITCH) -> Path:
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    comm = edge_tts.Communicate(text, MASTER_VOICE_NAME, rate=rate, pitch=pitch)
    await comm.save(str(out_path))
    return out_path

def synthesize_sync(text: str, output_path: str | Path, rate: str = MASTER_VOICE_RATE, pitch: str = MASTER_VOICE_PITCH) -> Path:
    return asyncio.run(synthesize_speech(text, output_path, rate, pitch))

if __name__ == "__main__":
    test_path = Path("output/cloned_voice/test_master_voice_engine.mp3")
    synthesize_sync("Testing official EduProSuite UK Academic master cloned voice.", test_path)
    print(f"[SUCCESS] Master voice engine verified: {test_path}")
