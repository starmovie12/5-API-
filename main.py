from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# --- ⚙️ URL LIST (5 APIs to Keep Alive 24/7) ---
SITES_TO_PING = [
    "https://hdhub4u-b1mi.onrender.com",          # HubDrive API
    "https://time-page-bay-pass.onrender.com",    # Timer API
    "https://hdhub4umoviepageurl.onrender.com",   # Movie Page API
    "https://hblinks-dad.onrender.com",           # Hblinks API
    "https://five-api-mzpp.onrender.com"          # ✅ SELF PING (Ye khud ko band hone se rokega)
]

def keep_alive_worker():
    print("🚀 Keep-Alive Service Started...")
    while True:
        print("\n🔄 Pinging 5 Servers...")
        for url in SITES_TO_PING:
            try:
                response = requests.get(url, timeout=30)
                print(f"✅ {url} -> Status: {response.status_code}")
            except Exception as e:
                print(f"❌ {url} -> Error: {str(e)}")
        
        # Har 2 minute (120 seconds) mein ping karega
        print("💤 Sleeping for 2 minutes...")
        time.sleep(120)

# Background Thread start karna
threading.Thread(target=keep_alive_worker, daemon=True).start()

@app.route('/')
def home():
    return "I am Alive and protecting your 5 APIs! 🛡️"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
