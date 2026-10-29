import os
import json
from moviepy import ImageClip, concatenate_videoclips

QUEUE_DIR = "queue/1_gambar_ready"
OUTPUT_DIR = "output/videos"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_video_for_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        images = data.get("downloaded_images", [])
        if not images:
            print(f"[Divisi 2 - Hijau] Error MoviePy: Tidak ada gambar valid untuk dirender pada {os.path.basename(json_path)}")
            return False

        clips = []
        for img_path in images:
            if os.path.exists(img_path):
                # Sintaks MoviePy v2: menggunakan with_duration dan with_fps
                clip = ImageClip(img_path).with_duration(3)
                clips.append(clip)

        if not clips:
            print(f"[Divisi 2 - Hijau] Error MoviePy: Gambar tidak ditemukan di disk untuk {os.path.basename(json_path)}")
            return False

        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip = final_clip.with_fps(24)

        base_name = os.path.splitext(os.path.basename(json_path))[0]
        output_video_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

        final_clip.write_videofile(output_video_path, codec="libx264", audio=False)

        # Close clips to free memory
        for c in clips:
            c.close()
        final_clip.close()

        print(f"[Divisi 2 - Hijau] Berhasil merender video: {output_video_path}")
        return True

    except Exception as e:
        print(f"[Divisi 2 - Hijau] Error MoviePy: {e}")
        print(f"[Divisi 2 - Hijau] Gagal merender video untuk {os.path.basename(json_path)}")
        return False

def main():
    if not os.path.exists(QUEUE_DIR):
        print("[Divisi 2 - Hijau] Folder queue/1_gambar_ready tidak ditemukan.")
        return

    files = [f for f in os.listdir(QUEUE_DIR) if f.endswith('.json')]
    if not files:
        print("[Divisi 2 - Hijau] Tidak ada queue video yang perlu dirender.")
        return

    for file_name in files:
        json_path = os.path.join(QUEUE_DIR, file_name)
        print(f"[Divisi 2 - Hijau] Memproses RENDER REAL VIDEO untuk: {file_name}")
        render_video_for_json(json_path)

if __name__ == "__main__":
    main()
