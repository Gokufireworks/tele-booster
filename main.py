# Updated simple view pusher (No proxy needed)
def telegram_view_worker(channel, post_id, status_dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        session = requests.Session()
        # Direct view trigger
        base_url = f"https://t.me/{channel}/{post_id}?embed=1"
        response = session.get(base_url, headers=headers, timeout=10)
        if response.status_code == 200:
            status_dict['count'] += 1
    except:
        pass

def boost_post_views(channel, post_id):
    target_views = 500 # Adjust as needed
    status_dict = {'count': 0}
    print(f"[+] Started boosting Post ID: {post_id}")
    
    for _ in range(target_views):
        telegram_view_worker(channel, post_id, status_dict)
        time.sleep(2) # Delay to prevent getting blocked
    print(f"[🎉] Finished boosting Post ID: {post_id}")

