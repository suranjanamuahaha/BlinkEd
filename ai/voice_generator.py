import os
import asyncio
import edge_tts

# ---------------------------------------------
# Load and clean narration text
# ---------------------------------------------
def load_paragraphs(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Remove unwanted symbols
    text = text.replace("*", "")

    # Split into paragraphs
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    return paragraphs


# ---------------------------------------------
# Generate narration using Edge-TTS
# ---------------------------------------------
async def generate_audio(paragraphs, output_dir="ai/output/audio"):
    os.makedirs(output_dir, exist_ok=True)

    VOICE = "en-US-AriaNeural"  # very natural female voice

    print(f"🎤 Using voice: {VOICE}")

    for i, para in enumerate(paragraphs, start=1):
        out_path = os.path.join(output_dir, f"audio_{i}.wav")
        print(f"🔊 Generating audio {i}/{len(paragraphs)}...")

        communicate = edge_tts.Communicate(para, VOICE)
        await communicate.save(out_path)

        print(f"✔ Saved: {out_path}")


# ---------------------------------------------
# MAIN
# ---------------------------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    text_path = os.path.join(BASE_DIR, "output", "explanation.txt")

    paragraphs = load_paragraphs(text_path)
    print(f"Found {len(paragraphs)} paragraphs.")

    asyncio.run(generate_audio(paragraphs))

    print("\n🎉 All audio files generated successfully!")
