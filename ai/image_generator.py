import os
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

IMAGE_MODEL = "gemini-2.0-flash"   # Best for image generation


# ----------------------------
# READ IMAGE PROMPTS
# ----------------------------
def read_prompts(path: str):
    prompts = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    current = []
    for line in lines:
        if line.startswith("IMAGE"):
            if current:
                prompts.append("\n".join(current).strip())
                current = []
        else:
            if line.strip():
                current.append(line.strip())

    if current:
        prompts.append("\n".join(current).strip())

    return prompts


# ----------------------------
# GENERATE IMAGE SAFELY
# ----------------------------
def generate_image(prompt: str):
    model = genai.GenerativeModel(IMAGE_MODEL)

    try:
        response = model.generate_image(
            prompt=prompt,
            size="1024x1024"   # best size for slideshows
        )

        # Return raw image bytes
        return response.images[0]  # flash returns array
    except Exception as e:
        print("Error generating image:", e)
        return None


# ----------------------------
# SAVE IMAGE BYTES
# ----------------------------
def save_image(image_bytes, path: str):
    with open(path, "wb") as f:
        f.write(image_bytes)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(BASE_DIR, "output", "image_prompts.txt")
    frames_dir = os.path.join(BASE_DIR, "output", "frames")

    os.makedirs(frames_dir, exist_ok=True)

    print("Reading prompts...")
    prompts = read_prompts(prompts_path)

    print(f"Total prompts: {len(prompts)}")

    for i, prompt in enumerate(prompts, start=1):
        print(f"\nGenerating image {i}/{len(prompts)}...")
        img_bytes = generate_image(prompt)

        if img_bytes:
            filename = f"frame_{i:02d}.png"
            save_path = os.path.join(frames_dir, filename)
            save_image(img_bytes, save_path)
            print(f"Saved: {save_path}")
        else:
            print("Skipped due to error.")

    print("\nAll done! Images saved in:")
    print(frames_dir)
