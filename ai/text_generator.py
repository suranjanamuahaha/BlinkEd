import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

TEXT_MODEL = "gemini-flash-latest"


def generate_explanation(topic: str):
    model = genai.GenerativeModel(TEXT_MODEL)

    prompt = f"""Explain the following topic in a simple and clear way.
Write 250 to 320 words.
Use short sentences.
Beginner friendly.
Topic: {topic}"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 1024
            }
        )
        # print("DEBUG:", response)


        # BEST way to extract text safely
        text = response.text  # ← Works in Flash
        if text:
            return text.strip()

        # If .text fails, fallback:
        all_text = ""
        for cand in response.candidates:
            for part in cand.content.parts:
                if hasattr(part, "text"):
                    all_text += part.text

        return all_text.strip() if all_text else "No text returned."

    except Exception as e:
        return f"Error generating content: {e}"
    

def save_explanation(text: str, output_path: str):
    """Save explanation text to a file."""
    directory = os.path.dirname(output_path)
    if directory != "":
        os.makedirs(directory, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    topic = "How does a machine work?"
    result = generate_explanation(topic)

    print("Generated Explanation:\n")
    print(result)

    save_path = "output/explanation.txt"
    save_explanation(result, save_path)

    print(f"\nSaved to: {save_path}")