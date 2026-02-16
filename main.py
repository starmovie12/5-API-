from flask import Flask, render_template_string
import threading
import time
import requests
from datetime import datetime
import logging

# Flask Logging बंद करें ताकि Render Logs साफ़ रहें
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# --- ⚙️ UPDATED URL LIST ---
SITES_TO_PING = [
    "https://hdhub4u-b1mi.onrender.com",
    "https://time-page-bay-pass.onrender.com",
    "https://hdhub4umoviepageurl.onrender.com",
    "https://hblinks-dad.onrender.com",
    "https://five-api-mzpp.onrender.com",
    "https://hubcdn-bypass.onrender.com"  # <--- New Link Added
]

# डिक्शनरी जो सबका स्टेटस स्टोर करेगी
SERVER_STATUS = {url: "⏳ Initializing..." for url in SITES_TO_PING}
LAST_CHECK_TIME = "Not yet checked"

def keep_alive_worker():
    """Background Thread जो 24/7 चलता रहेगा"""
    global LAST_CHECK_TIME
    # सर्वर स्टार्ट होने के लिए 5 सेकंड का वेट
    time.sleep(5) 
    print("🚀 Keep-Alive Worker Started...")
    
    while True:
        for url in SITES_TO_PING:
            try:
                # 10 सेकंड का टाइमआउट ताकि कोई साइट अटकने पर पूरा लूप न रुके
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    SERVER_STATUS[url] = "🟢 Running"
                else:
                    SERVER_STATUS[url] = f"⚠️ Status: {response.status_code}"
            except Exception:
                SERVER_STATUS[url] = "🔴 Down / Error"
        
        # समय अपडेट करें (IST या UTC के हिसाब से)
        LAST_CHECK_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"✅ All sites checked at {LAST_CHECK_TIME}")
        
        # हर 2 मिनट (120 सेकंड) में चेक करेगा
        time.sleep(120)

# Background thread को शुरू करें
threading.Thread(target=keep_alive_worker, daemon=True).start()

# --- DASHBOARD UI ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Status Monitor</title>
    <meta http-equiv="refresh" content="120">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f0f0f; color: #e0e0e0; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        h2 { color: #00d4ff; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
        .container { width: 100%; max-width: 600px; }
        .card { background: #1a1a1a; padding: 15px; margin-bottom: 12px; border-radius: 10px; border-left: 5px solid #444; box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: 0.3s; }
        .card:hover { transform: scale(1.02); }
        .url { font-size: 13px; color: #888; display: block; margin-bottom: 5px; word-break: break-all; }
        .status { font-size: 16px; font-weight: bold; }
        .running { color: #4caf50; border-left-color: #4caf50; }
        .down { color: #f44336; border-left-color: #f44336; }
        .footer { margin-top: 20px; font-size: 12px; color: #666; }
        .refresh-text { font-size: 10px; color: #444; margin-top: 5px; }
    </style>
</head>
<body>
    <h2>⚡ API MONITOR</h2>
    <div class="container">
        {% for url, status in statuses.items() %}
        <div class="card {{ 'running' if '🟢' in status else 'down' }}">
            <span class="url">{{ url }}</span>
            <span class="status">{{ status }}</span>
        </div>
        {% endfor %}
    </div>
    <div class="footer">Last Full Scan: {{ last_check }}</div>
    <div class="refresh-text">Auto-refreshes every 2 minutes</div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, statuses=SERVER_STATUS, last_check=LAST_CHECK_TIME)

# Render Health Check
@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    # Render default port is 10000
    app.run(host='0.0.0.0', port=10000)
