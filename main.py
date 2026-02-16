from flask import Flask, render_template_string
import threading
import time
import requests
from datetime import datetime

app = Flask(__name__)

# --- ⚙️ URL LIST ---
SITES_TO_PING = [
    "https://hdhub4u-b1mi.onrender.com",          # HubDrive API
    "https://time-page-bay-pass.onrender.com",    # Timer API
    "https://hdhub4umoviepageurl.onrender.com",   # Movie Page API
    "https://hblinks-dad.onrender.com",           # Hblinks API
    "https://five-api-mzpp.onrender.com"          # Self Ping
]

# Global Variable to store status
SERVER_STATUS = {url: "⏳ Checking..." for url in SITES_TO_PING}
LAST_CHECK_TIME = "Not yet checked"

def keep_alive_worker():
    global LAST_CHECK_TIME
    print("🚀 Keep-Alive Service Started...")
    
    while True:
        print("\n🔄 Checking All Servers...")
        for url in SITES_TO_PING:
            try:
                response = requests.get(url, timeout=20)
                if response.status_code == 200:
                    SERVER_STATUS[url] = "🟢 Running"
                else:
                    SERVER_STATUS[url] = f"⚠️ Status {response.status_code}"
            except Exception as e:
                SERVER_STATUS[url] = "🔴 Down"
        
        LAST_CHECK_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("✅ Status Updated. Sleeping for 2 minutes...")
        time.sleep(120)  # 2 Minute Wait

# Background Thread Start
threading.Thread(target=keep_alive_worker, daemon=True).start()

# --- 🖥️ DASHBOARD UI (HTML) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>API Status Monitor</title>
    <meta http-equiv="refresh" content="120"> <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .container { width: 100%; max-width: 600px; background: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        h2 { text-align: center; color: #3b82f6; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        .status-card { display: flex; justify-content: space-between; align-items: center; background: #0f172a; padding: 15px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #334155; }
        .url { font-size: 13px; color: #cbd5e1; word-break: break-all; }
        .badge { font-weight: bold; padding: 5px 10px; border-radius: 5px; font-size: 12px; min-width: 80px; text-align: center; }
        .running { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
        .down { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
        .checking { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
        .footer { margin-top: 20px; font-size: 12px; color: #64748b; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚡ 5-API STATUS MONITOR</h2>
        {% for url, status in statuses.items() %}
        <div class="status-card">
            <div class="url">{{ url }}</div>
            <div class="badge {{ 'running' if 'Running' in status else 'down' if 'Down' in status else 'checking' }}">
                {{ status }}
            </div>
        </div>
        {% endfor %}
        <div class="footer">
            Last Updated: {{ last_check }}<br>
            Auto-refreshing every 2 minutes...
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, statuses=SERVER_STATUS, last_check=LAST_CHECK_TIME)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
