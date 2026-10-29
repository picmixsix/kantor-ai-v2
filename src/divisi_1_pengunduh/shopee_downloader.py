import os
import json
import gdown

QUEUE_INPUT_DIR = "queue/0_stok_link"
QUEUE_OUTPUT_DIR = "queue/1_gambar_ready"
IMAGE_OUTPUT_DIR = "output/images"

os.makedirs(QUEUE_OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

def download_from_gdrive(drive_url, target_folder):
    try:
        # Menangani tautan folder atau file tunggal dari Google Drive
        if "folder" in drive_url or "id=" in drive_url or "folders" in drive_url:
            gdown.download_folder(url=drive_url, output=target_folder, quiet=False, remaining_ok=True)
        else:
            gdown.download(url=drive_url, output=os.path.join(target_folder, "gdrive_img.jpg"), quiet=False)
        
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        downloaded_files = []
        for root, _, files in os.walk(target_folder):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    downloaded_files.append(os.path.join(root, file))
        return downloaded_files
    except Exception as e:
        print(f"[Divisi 1 - Biru] Error download dari Google Drive: {e}")
        return []

def process_queue():
    if not os.path.exists(QUEUE_INPUT_DIR):
        return

    files = [f for f in os.listdir(QUEUE_INPUT_DIR) if f.endswith('.json')]
    if not files:
        print("[Divisi 1 - Biru] Tidak ada stok link baru di queue/0_stok_link/")
        return

    for file_name in files:
        input_json_path = os.path.join(QUEUE_INPUT_DIR, file_name)
        base_name = os.path.splitext(file_name)[0]

        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        drive_url = data.get("gdrive_url") or data.get("product_url", "")
        target_img_dir = os.path.join(IMAGE_OUTPUT_DIR, base_name)
        os.makedirs(target_img_dir, exist_ok=True)

        print(f"[Divisi 1 - Biru] Mengunduh gambar dari Google Drive untuk: {file_name}")
        downloaded = download_from_gdrive(drive_url, target_img_dir)

        data["downloaded_images"] = downloaded
        data["status"] = "GAMBAR_READY"

        output_json_path = os.path.join(QUEUE_OUTPUT_DIR, file_name)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        os.remove(input_json_path)
        print(f"[Divisi 1 - Biru] Berhasil mengunduh {len(downloaded)} gambar. Dipindahkan ke {output_json_path}")

if __name__ == "__main__":
    process_queue()
