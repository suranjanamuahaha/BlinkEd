import os
from moviepy.editor import *

def create_video():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "output", "frames")
    audio_dir = os.path.join(BASE_DIR, "output", "audio")
    output_path = os.path.join(BASE_DIR, "output", "video", "final_video.mp4")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load assets
    image_files = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png")])
    audio_files = sorted([os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".wav")])

    print(f"🔍 Found {len(image_files)} images.")
    print(f"🔍 Found {len(audio_files)} audio clips.")

    clips = []

    for i, (img, aud) in enumerate(zip(image_files, audio_files)):
        print(f"🎨 Processing slide {i+1}...")

        try:
            audio_clip = AudioFileClip(aud)
            audio_duration = audio_clip.duration
        except Exception as e:
            print(f"❌ ERROR reading audio {aud}: {e}")
            continue

        if audio_duration is None or audio_duration <= 0:
            print(f"⚠ Skipping invalid audio (duration={audio_duration}) → {aud}")
            continue

        try:
            image_clip = (
                ImageClip(img)
                .resize(width=1280)
                .set_duration(audio_duration)
                .set_audio(AudioFileClip(aud))
            )
            clips.append(image_clip)

        except Exception as e:
            print(f"❌ ERROR creating clip for {img}: {e}")
            continue

    if not clips:
        print("❌ No valid clips generated. Cannot create video.")
        return

    print("🎞 Adding transitions and combining clips...")

    # Crossfade transition
    final = concatenate_videoclips(
        clips,
        method="compose",
        padding=-0.4
    ).crossfadein(0.6)

    print("💾 Rendering final video...")

    final.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    print(f"🎉 Video saved at:\n{output_path}")


if __name__ == "__main__":
    create_video()
