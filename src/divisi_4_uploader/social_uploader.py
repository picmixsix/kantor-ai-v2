import os
import json
import glob

def process_uploads():
    approved_files = glob.glob("queue/3_approved/*.json")
    if not approved_files:
        print("[Divisi 4 - Biru] Tidak ada konten APPROVED untuk diunggah.")
        return

    for filepath in approved_files:
        filename = os.path.basename(filepath)
        print(f"[Divisi 4 - Biru] Memproses unggahan untuk: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        video_path = data.get('video_path', '')
        
        if os.path.exists(video_path):
            print(f"[Divisi 4 - Biru] Simulasi Mengunggah video: {video_path}")
            
            data["status"] = "DONE"
            target_path = os.path.join("queue/5_done", filename)
            
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as out_f:
                json.dump(data, out_f, indent=2)
                
            os.remove(filepath)
            print(f"[Divisi 4 - Biru] Unggahan SELESAI & diarsipkan: {filename}")
        else:
            print(f"[Divisi 4 - Biru] Error: Berkas video tidak ditemukan: {video_path}")

if __name__ == "__main__":
    process_uploads()
