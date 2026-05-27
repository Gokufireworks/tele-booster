import requests
import re
import time
import random
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

CHANNEL_USERNAME = "Tradecryptolife"
processed_posts = set()

# --- Render Free Web Service er jonno dummy server (Port Error thik korar jonno) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is active and running on Render Free Plan!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, DummyHandler)
    httpd.serve_forever()

# Background-e dummy server chalu kora
Thread(target=run_dummy_server, daemon=True).start()
# ----------------------------------------------------------------------------------

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

print("Bot started on Render Free Web Service...")
while True:
    post_id = get_latest_post()
    if post_id and post_id not in processed_posts:
        # 500 theke 5000 porjonto random view select hobe
        random_views = random.randint(500, 5000)
        print(f"New post detected: {post_id}. Target views: {random_views}")
        
        for i in range(random_views):
            send_view(post_id)
            if i % 10 == 0:
                time.sleep(0.5) # Server block rukhter jonno choto break
                
        processed_posts.add(post_id)
        print(f"Boosting complete for {post_id}. Total sent: {random_views}")
    time.sleep(60)

