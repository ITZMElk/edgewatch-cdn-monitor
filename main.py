"""Entry point for launching the simulated CDN services and dashboard."""

import threading
import time
import webbrowser
import logging
import os
from persistence import init_db

init_db()

from config import SERVERS, DASHBOARD_PORT
from origin_server import origin_app
from edge_server import create_edge_app
from dashboard_server import dashboard_app

# Silence standard Flask startup spam
logging.getLogger('werkzeug').setLevel(logging.ERROR)

def run_app(app, port):
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)

def main():
    print("=" * 60)
    print("🚀 LAUNCHING MULTI-PORT SOCKET CDN SYSTEM")
    print("=" * 60)

    # 1. Start Origin (Port 5000)
    threading.Thread(target=run_app, args=(origin_app, SERVERS['origin']['port']), daemon=True).start()
    print(f"✅ Origin Server listening on http://localhost:{SERVERS['origin']['port']}")

    # 2. Start Edges (Port 5001 & 5002)
    for edge_id, config in SERVERS['edges'].items():
        app = create_edge_app(edge_id)
        threading.Thread(target=run_app, args=(app, config['port']), daemon=True).start()
        print(f"✅ Edge Server [{config['name']}] listening on http://localhost:{config['port']}")

    # 3. Start Dashboard (Port 6000)
    threading.Thread(target=run_app, args=(dashboard_app, DASHBOARD_PORT), daemon=True).start()
    print(f"📊 Dashboard available at: http://localhost:{DASHBOARD_PORT}")
    print("=" * 60)

    time.sleep(1)
    if os.environ.get("DISABLE_BROWSER") != "1":
        webbrowser.open(f"http://localhost:{DASHBOARD_PORT}")

    print("\nSystem running! Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")

if __name__ == "__main__":
    main()
