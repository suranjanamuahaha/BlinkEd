import os
from diffusers import StableDiffusionXLPipeline
import torch
from PIL import Image


# ----------------------------
# LOAD SDXL TURBO MODEL
# ----------------------------
print("🔄 Loading SDXL Turbo model... (first time slow, then cached)")

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    variant="fp16"
)

# Determine device
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

print(f"✅ Using device: {device}")


# ----------------------------
# READ PROMPTS
# ----------------------------
def read_prompts(path):
    prompts = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    current = []
    for line in lines:
        if line.startswith("IMAGE"):
            if current:
                prompts.append(" ".join(current).strip())
                current = []
        else:
            if line.strip():
                current.append(line.strip())

    if current:
        prompts.append(" ".join(current).strip())

    return prompts


# ----------------------------
# GENERATE IMAGE LOCALLY
# ----------------------------
def generate_image(prompt: str):
    try:
        # SDXL Turbo uses only 1 step — super fast
        image = pipe(
            prompt,
            width=1024,
            height=576,
            num_inference_steps=1,
            guidance_scale=0.0
        ).images[0]

        return image

    except Exception as e:
        print("❌ Error generating image:", e)
        return None


# ----------------------------
# SAVE IMAGE
# ----------------------------
def save_image(image: Image.Image, path: str):
    image.save(path)


# ----------------------------
# MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(BASE_DIR, "output", "image_prompts.txt")
    frames_dir = os.path.join(BASE_DIR, "output", "frames")

    os.makedirs(frames_dir, exist_ok=True)

    print("📘 Reading prompts...")
    prompts = read_prompts(prompts_path)

    print(f"📌 Total prompts: {len(prompts)}")

    for i, prompt in enumerate(prompts, start=1):
        print(f"\n🎨 Generating image {i}/{len(prompts)}…")
        img = generate_image(prompt)

        if img:
            save_path = os.path.join(frames_dir, f"frame_{i:02d}.png")
            save_image(img, save_path)
            print(f"✔ Saved: {save_path}")
        else:
            print("⚠ Skipped due to error.")

    print("\n🎉 ALL DONE! Images saved!")
