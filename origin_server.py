"""Origin server implementation used as the upstream content source."""

from flask import Flask, jsonify, request
import time

origin_app = Flask(__name__)

# Sample static files hosted on origin
ORIGIN_STORAGE = {
    "index.html": "<html><body><h1>Welcome to Main Origin Server</h1></body></html>",
    "style.css": "body { background: #121212; color: #ffffff; }",
    "app.js": "console.log('App initialized from Origin Server');",
    "video.mp4": "[Binary Video Payload Sample - 10MB]"
}

@origin_app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "role": "origin_server"})

@origin_app.route('/fetch/<path:filename>', methods=['GET'])
def fetch_file(filename):
    # Simulate origin server retrieval delay
    time.sleep(0.1)
    if filename in ORIGIN_STORAGE:
        return jsonify({
            "status": "success",
            "filename": filename,
            "content": ORIGIN_STORAGE[filename],
            "source": "Mumbai Origin Server"
        }), 200
    return jsonify({"error": "File not found"}), 404