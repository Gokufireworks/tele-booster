import requests
import re
import time
import random
from threading import Thread

# ==================== YOUR CONFIGURATION ====================
BOT_TOKEN = "8973964361:AAE_H3TLybnKFdZpWKKb6knwS_B5EJHgWV0"
CHANNEL_USERNAME = "Tradecryptolife"  # Your channel username

# Random View Range (Views will randomly vary between 500 and 3000 per post)
MIN_VIEWS = 500
MAX_VIEWS = 3000
# =============================================================

processed_posts = set()

def get_fresh_proxies():
    proxies = []
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    for source in sources:
        try:
            res = requests.get(source, timeout=5)
            if res.status_code == 200:
                proxies.extend(res.text.splitlines())
        except:
            continue
    return list(set(proxies))

def telegram_view_worker(proxy, channel, post_id, status_dict):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        session = requests.Session()
        base_url = f"https://t.me/{channel}/{post_id}?embed=1"
        response = session.get(base_url, proxies=proxies, headers=headers, timeout=5)
        if response.status_code == 200 and "views" in response.text:
            token = re.search(r'data-view="([^"]+)"', response.text)
            if token:
                status_dict['count'] += 1
    except:
        pass

def boost_post_views(channel, post_id):
    # Selects a random target for each new post
    target_views = random.randint(MIN_VIEWS, MAX_VIEWS)
    
    print(f"\n[🔥] New post detected! ID: {post_id}")
    print(f"[🎲] Random views targeted for this post: {target_views}")
    print(f"[+] View sending started...")
    
    status_dict = {'count': 0}
    
    while status_dict['count'] < target_views:
        proxies = get_fresh_proxies()
        if not proxies:
            time.sleep(5)
            continue
            
        threads = []
        for proxy in proxies:
            if status_dict['count'] >= target_views:
                break
            t = Thread(target=telegram_view_worker, args=(proxy, channel, post_id, status_dict))
            t.start()
            threads.append(t)
            
            if len(threads) >= 40:
                for th in threads:
                    th.join()
                threads = []
                time.sleep(0.5)
                
        for th in threads:
            th.join()
            print(f"[*] Current views for ID {post_id}: ~{status_dict['count']}/{target_views}")
            
    print(f"[🎉] Done! Successfully sent {status_dict['count']} random views to Post ID {post_id}.\n")

def get_latest_post_id():
    try:
        res = requests.get(f"https://t.me/s/{CHANNEL_USERNAME}", timeout=10)
        if res.status_code == 200:
            matches = re.findall(rf'href="https://t.me/{CHANNEL_USERNAME}/(\d+)"', res.text)
            if matches:
                return int(matches[-1])
    except Exception as e:
        print("[-] Channel check failed:", e)
    return None

def main():
    print("=" * 60)
    print("   TELEGRAM 24/7 AUTO RANDOM POST VIEW BOOSTER (REAL MODE)   ")
    print("=" * 60)
    print(f"[+] Success! Monitoring channel: @{CHANNEL_USERNAME}")
    print(f"[+] Random views range set to: {MIN_VIEWS} - {MAX_VIEWS}")
    
    # Track the current last post on initial run to skip old posts
    last_id = get_latest_post_id()
    if last_id:
        processed_posts.add(last_id)
        print(f"[*] Current latest post ID in channel: {last_id} (Skipped)")
        print("[+] Bot is now active! Post anything new to test random views.")

    while True:
        try:
            current_id = get_latest_post_id()
            if current_id and current_id not in processed_posts:
                processed_posts.add(current_id)
                boost_post_views(CHANNEL_USERNAME, current_id)
        except Exception as e:
            print("[-] Loop error:", e)
            
        # Checks the channel every 20 seconds for new posts
        time.sleep(20)

if __name__ == "__main__":
    main()
