import os
import json
import glob
import requests

def download_image(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"[Divisi 1] Gagal mengunduh {url}: {e}")
    return False

def process_download():
    stok_files = glob.glob("queue/0_stok_link/*.json")
    if not stok_files:
        print("[Divisi 1 - Biru] Tidak ada stok link baru di queue/0_stok_link/.")
        return

    for filepath in stok_files:
        filename = os.path.basename(filepath)
        task_id = os.path.splitext(filename)[0]
        print(f"[Divisi 1 - Biru] Memproses unduhan nyata untuk: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        img_urls = data.get("image_urls", [])
        saved_image_paths = []
        
        task_img_dir = os.path.join("output", "images", task_id)
        os.makedirs(task_img_dir, exist_ok=True)
        
        for idx, url in enumerate(img_urls):
            img_path = os.path.join(task_img_dir, f"img_{idx+1}.jpg")
            if download_image(url, img_path):
                saved_image_paths.append(img_path)
                
        if not saved_image_paths:
            placeholder_path = os.path.join(task_img_dir, "default.jpg")
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1080, 1920), color=(30, 30, 30))
            d = ImageDraw.Draw(img)
            d.text((100, 960), f"PRODUK: {data.get('product_title', 'SHOPEE PRODUCT')}", fill=(255, 255, 255))
            img.save(placeholder_path)
            saved_image_paths.append(placeholder_path)

        data["status"] = "IMAGES_READY"
        data["downloaded_images"] = saved_image_paths
        
        target_path = os.path.join("queue/1_gambar_ready", filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        os.remove(filepath)
        print(f"[Divisi 1 - Biru] Berhasil unduh {len(saved_image_paths)} gambar. Dipindahkan ke queue/1_gambar_ready/{filename}")

if __name__ == "__main__":
    process_download()
