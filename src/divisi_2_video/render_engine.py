import os
import json
import glob
from PIL import Image, ImageDraw

def render_real_video(task_id, images, title, output_video_path):
    try:
        from moviepy.editor import ImageClip, concatenate_videoclips
        
        clips = []
        for img_path in images:
            if os.path.exists(img_path):
                clip = ImageClip(img_path).set_duration(3).resize(newsize=(1080, 1920))
                clips.append(clip)
                
        if not clips:
            raise Exception("Tidak ada gambar valid untuk dirender.")
            
        final_clip = concatenate_videoclips(clips, method="compose")
        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
        final_clip.write_videofile(
            output_video_path,
            fps=24,
            codec="libx264",
            audio=False,
            preset="ultrafast",
            logger=None
        )
        print(f"[Divisi 2 - Hijau] RENDER SELESAI: Berkas video fisik tercipta di {output_video_path}")
        return True
    except Exception as e:
        print(f"[Divisi 2 - Hijau] Error MoviePy: {e}")
        return False

def process_render():
    gambar_files = glob.glob("queue/1_gambar_ready/*.json")
    rejected_files = glob.glob("queue/4_rejected/*.json")
    
    target_files = gambar_files + rejected_files
    if not target_files:
        print("[Divisi 2 - Hijau] Tidak ada antrean video baru/revisi.")
        return

    for filepath in target_files:
        filename = os.path.basename(filepath)
        task_id = os.path.splitext(filename)[0]
        print(f"[Divisi 2 - Hijau] Memproses RENDER REAL VIDEO untuk: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        images = data.get("downloaded_images", [])
        title = data.get("product_title", "Produk Rekomendasi")
        output_video = os.path.join("output", "videos", f"{task_id}.mp4")
        
        success = render_real_video(task_id, images, title, output_video)
        
        if success:
            data["status"] = "AWAITING_APPROVAL"
            data["video_path"] = output_video
            
            target_path = os.path.join("queue/2_video_ready", filename)
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            os.remove(filepath)
            print(f"[Divisi 2 - Hijau] Video nyata dikirim ke Ruang Direktur: queue/2_video_ready/{filename}")
        else:
            print(f"[Divisi 2 - Hijau] Gagal merender video untuk {filename}")

if __name__ == "__main__":
    process_render()
