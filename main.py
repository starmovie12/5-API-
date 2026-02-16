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

# --- ⚙️ URL LIST ---
SITES_TO_PING = [
    "https://hdhub4u-b1mi.onrender.com",
    "https://time-page-bay-pass.onrender.com",
    "https://hdhub4umoviepageurl.onrender.com",
    "https://hblinks-dad.onrender.com",
    "https://five-api-mzpp.onrender.com"
]

SERVER_STATUS = {url: "⏳ Initializing..." for url in SITES_TO_PING}
LAST_CHECK_TIME = "Not yet checked"

def keep_alive_worker():
    """Background Thread jo 24/7 chalega"""
    global LAST_CHECK_TIME
    # Server start hone ka thoda wait karega taaki port bind ho jaye
    time.sleep(5) 
    print("🚀 Keep-Alive Worker Started in Background...")
    
    while True:
        for url in SITES_TO_PING:
            try:
                # Timeout kam rakha taaki thread fast chale
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    SERVER_STATUS[url] = "🟢 Running"
                else:
                    SERVER_STATUS[url] = f"⚠️ {response.status_code}"
            except:
                SERVER_STATUS[url] = "🔴 Down"
        
        LAST_CHECK_TIME = datetime.now().strftime("%H:%M:%S UTC")
        print(f"✅ Checked all sites at {LAST_CHECK_TIME}")
        
        # 2 Minute Wait
        time.sleep(120)

# Thread ko daemon mode me start karo
threading.Thread(target=keep_alive_worker, daemon=True).start()

# --- DASHBOARD UI ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Status Monitor</title>
    <meta http-equiv="refresh" content="120">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #111; color: white; padding: 20px; text-align: center; }
        .card { background: #222; padding: 10px; margin: 10px; border-radius: 8px; border: 1px solid #444; }
        .running { color: #4caf50; font-weight: bold; }
        .down { color: #f44336; font-weight: bold; }
    </style>
</head>
<body>
    <h2>⚡ API MONITOR</h2>
    {% for url, status in statuses.items() %}
    <div class="card">
        <small>{{ url }}</small><br>
        <span class="{{ 'running' if 'Running' in status else 'down' }}">{{ status }}</span>
    </div>
    {% endfor %}
    <p style="color:#888; font-size:12px;">Last Check: {{ last_check }}</p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, statuses=SERVER_STATUS, last_check=LAST_CHECK_TIME)

# Health Check Endpoint for Render
@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
