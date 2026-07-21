# edge_server.py
"""Flask application factory for edge servers in the simulation."""

from flask import Flask, jsonify, request
import requests
from config import SERVERS
from cache_manager import MemoryCache


def create_edge_app(edge_id):
    app = Flask(f"edge_{edge_id}")
    cache = MemoryCache(ttl_seconds=120)
    config = SERVERS['edges'][edge_id]
    
    stats = {"hits": 0, "misses": 0}

    @app.route('/stats', methods=['GET'])
    def get_stats():
        return jsonify({
            "edge_id": edge_id,
            "hits": stats["hits"],
            "misses": stats["misses"],
            "cached_files": cache.list_keys(),
            "cache": cache.inspect(),
        })

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "online", "edge_id": edge_id, "name": config["name"]})

    @app.route('/content/<path:filename>', methods=['GET'])
    def get_content(filename):
        cached_data = cache.get(filename)
        if cached_data:
            stats["hits"] += 1
            return jsonify({
                "cache_status": "HIT",
                "served_by": config['name'],
                "filename": filename,
                "content": cached_data
            }), 200

        # Cache Miss -> Fetch from Origin over HTTP
        stats["misses"] += 1
        origin_url = f"{SERVERS['origin']['url']}/fetch/{filename}"
        
        try:
            res = requests.get(origin_url, timeout=2)
            if res.status_code == 200:
                content = res.json()["content"]
                cache.set(filename, content)
                return jsonify({
                    "cache_status": "MISS",
                    "served_by": config['name'],
                    "filename": filename,
                    "content": content
                }), 200
        except Exception as e:
            return jsonify({"error": f"Failed to reach origin: {str(e)}"}), 500

        return jsonify({"error": "File not found on origin"}), 404

    return app
