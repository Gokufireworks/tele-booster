import requests
import re
import time

CHANNEL_USERNAME = "Tradecryptolife"
processed_posts = set()

def send_view(post_id):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
        requests.get(url, headers=headers, timeout=10)
        return True
    except:
        return False

def get_latest_post():
    try:
        res = requests.get(f"https://t.me/s/{CHANNEL_USERNAME}", timeout=10)
        matches = re.findall(rf'href="https://t.me/{CHANNEL_USERNAME}/(\d+)"', res.text)
        return int(matches[-1]) if matches else None
    except:
        return None

print("Bot started...")
while True:
    post_id = get_latest_post()
    if post_id and post_id not in processed_posts:
        print(f"New post detected: {post_id}")
        for _ in range(300): # ৩০০ ভিউ পাঠানোর জন্য
            send_view(post_id)
        processed_posts.add(post_id)
        print("Boosting complete.")
    time.sleep(60) # ১ মিনিট পরপর চেক করবে

