import requests
import re
import time
from threading import Thread

# --- CONFIGURATION ---
CHANNEL_USERNAME = "Tradecryptolife" 
# ---------------------

processed_posts = set()

def telegram_view_worker(channel, post_id, status_dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        session = requests.Session()
        # Direct view trigger via telegram embed link
        base_url = f"https://t.me/{channel}/{post_id}?embed=1"
        response = session.get(base_url, headers=headers, timeout=10)
        if response.status_code == 200:
            status_dict['count'] += 1
    except:
        pass

def boost_post_views(channel, post_id):
    target_views = 500  # Number of views to send
    status_dict = {'count': 0}
    print(f"[🔥] New post detected! ID: {post_id}. Boosting started...")
    
    # Sending views with a slight delay to prevent blocking
    for _ in range(target_views):
        telegram_view_worker(channel, post_id, status_dict)
        time.sleep(1) 
    print(f"[🎉] Finished boosting Post ID: {post_id}. Total: {status_dict['count']}")

def get_latest_post_id():
    try:
        res = requests.get(f"https://t.me/s/{CHANNEL_USERNAME}", timeout=10)
        if res.status_code == 200:
            matches = re.findall(rf'href="https://t.me/{CHANNEL_USERNAME}/(\d+)"', res.text)
            if matches:
                return int(matches[-1])
    except:
        pass
    return None

def main():
    print(f"[+] Monitoring channel: @{CHANNEL_USERNAME}")
    last_id = get_latest_post_id()
    if last_id: 
        processed_posts.add(last_id)
        print(f"[*] Current latest post ID: {last_id} (Skipped)")
    
    # Infinite loop for 24/7 monitoring
    while True:
        try:
            current_id = get_latest_post_id()
            if current_id and current_id not in processed_posts:
                processed_posts.add(current_id)
                boost_post_views(CHANNEL_USERNAME, current_id)
        except:
            pass
        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    main()

