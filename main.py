from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# --- ⚙️ URL LIST (Jo 24/7 chalani hai) ---
SITES_TO_PING = [
    "https://hdhub4u-b1mi.onrender.com",
    "https://time-page-bay-pass.onrender.com",
    "https://hdhub4umoviepageurl.onrender.com",
    "https://hblinks-dad.onrender.com"
    # Jab Render par is app ka URL milega, use yahan niche add kar dena
]

def keep_alive_worker():
    print("🚀 Keep-Alive Service Started...")
    while True:
        print("\n🔄 Pinging Servers...")
        for url in SITES_TO_PING:
            try:
                response = requests.get(url, timeout=20)
                print(f"✅ {url} -> Status: {response.status_code}")
            except Exception as e:
                print(f"❌ {url} -> Error: {str(e)}")
        
        # 2 Minute (120 Seconds) ka wait
        print("💤 Sleeping for 2 minutes...")
        time.sleep(120)

# Background Thread start karna (Taaki Flask server block na ho)
threading.Thread(target=keep_alive_worker, daemon=True).start()

@app.route('/')
def home():
    return "I am Alive and pinging your APIs every 2 minutes! 🚀"

if __name__ == "__main__":
    # Render port environment variable se uthata hai, default 10000
    app.run(host='0.0.0.0', port=10000)
