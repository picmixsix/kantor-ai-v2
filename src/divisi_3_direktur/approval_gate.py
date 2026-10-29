import os
import json
import glob
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def send_approval_with_buttons():
    ready_files = glob.glob("queue/2_video_ready/*.json")
    if not ready_files:
        print("[Divisi 3 - Direktur] Tidak ada video baru di queue/2_video_ready/.")
        return

    for filepath in ready_files:
        filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        video_path = data.get('video_path', '')
        
        msg = (
            f"🎬 *LAPORAN DIREKTUR - PERSETUJUAN KONTEN*\n\n"
            f"📌 *Task ID*: `{filename}`\n"
            f"📦 *Produk*: {data.get('product_title', 'Produk Shopee')}\n"
            f"🔗 *Link*: {data.get('product_url', '-')}\n"
            f"📁 *Video Path*: `{video_path}`\n\n"
            f"Pilih tindakan di bawah ini untuk melanjutkan alur:"
        )
        
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ APPROVE (Lanjut Upload)", "callback_data": f"approve:{filename}"},
                    {"text": "❌ REJECT (Revisi Render)", "callback_data": f"reject:{filename}"}
                ]
            ]
        }
        
        if TELEGRAM_TOKEN and CHAT_ID:
            if os.path.exists(video_path):
                url_vid = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
                with open(video_path, 'rb') as vf:
                    requests.post(url_vid, data={"chat_id": CHAT_ID, "caption": msg, "parse_mode": "Markdown", "reply_markup": json.dumps(keyboard)}, files={"video": vf})
            else:
                url_msg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(url_msg, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "reply_markup": keyboard})
            print(f"[Divisi 3 - Direktur] Video & Tombol Approval terkirim ke Telegram: {filename}")
        else:
            print(f"[Divisi 3 - Direktur] No Telegram Token. Auto-approving untuk pengujian...")
            target_path = os.path.join("queue/3_approved", filename)
            data["status"] = "APPROVED"
            with open(target_path, 'w', encoding='utf-8') as out_f:
                json.dump(data, out_f, indent=2)
            os.remove(filepath)

if __name__ == "__main__":
    send_approval_with_buttons()
