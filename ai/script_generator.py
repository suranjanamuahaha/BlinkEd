import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# ----------------------------
# INIT
# ----------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

TEXT_MODEL = "gemini-flash-latest"


# ----------------------------
# READ NARRATION
# ----------------------------
def read_explanation(path: str) -> str:
    """Read the previously generated explanation."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


# ----------------------------
# SPLIT INTO CHUNKS
# ----------------------------
def chunk_text(text: str, max_sentences=3):
    """Break narration into short visual chunks for image prompting."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []

    current = []
    for s in sentences:
        current.append(s)
        if len(current) >= max_sentences:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


# ----------------------------
# SAFE GEMINI IMAGE PROMPT GENERATION
# ----------------------------
def generate_image_prompt(narration_chunk: str) -> str:
    """
    Convert narration chunk into an image prompt.
    Includes robust fallback extraction (never crashes).
    """
    model = genai.GenerativeModel(TEXT_MODEL)

    prompt = f"""
Convert the following narration into a vivid, detailed image prompt.

Rules:
- No text overlays
- No narration style, only visual description
- Cinematic, realistic, descriptive
- One single clear scene
- Do NOT mention the narration text
- Focus on visuals only

Narration:
"{narration_chunk}"
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7, "max_output_tokens": 1024}
        )

        # --------------- SAFE EXTRACTION ---------------
        # 1. Try response.text
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # 2. Fallback: extract manually
        extracted = ""
        if hasattr(response, "candidates"):
            for cand in response.candidates:
                if hasattr(cand, "content") and cand.content:
                    for part in cand.content.parts:
                        if hasattr(part, "text") and part.text:
                            extracted += part.text

        if extracted.strip():
            return extracted.strip()

        # 3. Final fallback
        return "A detailed cinematic scene representing the narration."

    except Exception as e:
        return f"Error generating prompt: {e}"


# ----------------------------
# SAVE PROMPTS
# ----------------------------
def save_prompts(prompts, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for i, p in enumerate(prompts, start=1):
            f.write(f"IMAGE {i}:\n{p}\n\n")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(BASE_DIR, "output", "explanation.txt")
    output_path = os.path.join(BASE_DIR, "output", "image_prompts.txt")

    print("Reading narration text...")
    narration = read_explanation(input_path)

    print("Splitting into visual chunks...")
    chunks = chunk_text(narration, max_sentences=3)

    print(f"Total image chunks: {len(chunks)}\n")

    prompts = []
    for i, ch in enumerate(chunks, start=1):
        print(f"Generating image prompt {i}/{len(chunks)}...")
        prompt_text = generate_image_prompt(ch)
        prompts.append(prompt_text)

    save_prompts(prompts, output_path)

    print(f"\nDone! Image prompts saved at:\n{output_path}")
