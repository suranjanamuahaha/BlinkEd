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
# SPLIT INTO CHUNKS (PARAGRAPHS)
# ----------------------------
def chunk_text(text: str):
    """
    Split narration into chunks based on paragraph breaks (blank lines or newlines).
    Each paragraph will be turned into ONE image prompt.
    """
    raw_chunks = re.split(r'\n\s*\n', text.strip())
    chunks = [c.strip() for c in raw_chunks if c.strip()]
    return chunks


# ----------------------------
# GENERATE EDUCATIONAL IMAGE PROMPT
# ----------------------------
def generate_image_prompt(narration_chunk: str) -> str:
    """
    Convert narration chunk into a clean educational image prompt.
    Includes robust fallback extraction (never crashes).
    """
    model = genai.GenerativeModel(TEXT_MODEL)

    prompt = f"""
Convert the narration into a clear 1-line educational image prompt, possibly under 70 tokens.

Rules:
- The illustration must be in landscape orientation (wide, horizontal).
- The visual style must match the narration content closely and be a bit realistic and engaging.
- Try to make it casual and natural and a little text-book style.
- This is something to explain the topic to STUDENTS.
- Don't use multiple scenes or diagrams.
- DONT USE ANY TEXT IN THE IMAGE.
- Try to make the lines smooth, straight, and professional.
- Avoid hyperrealism; keep it cartoonish, fun, and very clear.
- You can use text ONLY if it is clear and readable.
- Keep everything simple and easy to understand.
- Do NOT create complex flowcharts or hard diagrams.

Narration:
"{narration_chunk}"
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.4, "max_output_tokens": 1024}
        )

        # 1. Try response.text
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # 2. Extract manually
        extracted = ""
        if hasattr(response, "candidates"):
            for cand in response.candidates:
                if hasattr(cand, "content") and cand.content:
                    for part in cand.content.parts:
                        if hasattr(part, "text") and part.text:
                            extracted += part.text

        if extracted.strip():
            return extracted.strip()

        # 3. Fallback
        return "Simple educational diagram explaining the concept."

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

    print("Splitting into paragraph-based chunks...")
    chunks = chunk_text(narration)

    print(f"Total image chunks: {len(chunks)}\n")

    prompts = []
    for i, ch in enumerate(chunks, start=1):
        print(f"Generating image prompt {i}/{len(chunks)}...")
        prompts.append(generate_image_prompt(ch))

    save_prompts(prompts, output_path)

    print(f"\nDone! Image prompts saved at:\n{output_path}")
