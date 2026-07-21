"""Client-side request simulator that routes traffic through the CDN model."""

import requests
import time
from dns_router import resolve_edge
from geo_utils import estimate_latency
from monitoring import record_request
from config import SERVERS
from geo_utils import haversine_distance


def simulate_client(client_coords, filepath, city_name="Unknown"):
    try:
        edge_id, edge_config, dist = resolve_edge(client_coords)
    except RuntimeError as error:
        return {"status": "error", "message": str(error)}
    edge_url = f"{edge_config['url']}/content/{filepath}"
    ideal_edge_id = min(
        SERVERS["edges"],
        key=lambda candidate: haversine_distance(client_coords, SERVERS["edges"][candidate]["coords"]),
    )

    start_time = time.time()
    try:
        res = requests.get(edge_url, timeout=5)
        if res.status_code == 200:
            payload = res.json()
            network_delay = estimate_latency(
                dist, is_hit=payload.get("cache_status") == "HIT"
            )
            total_time_ms = round((time.time() - start_time) * 1000 + network_delay, 2)
            result = {
                "status": "success",
                "edge_id": edge_id,
                "edge": edge_config['name'],
                "rerouted": edge_id != ideal_edge_id,
                "cache_status": payload['cache_status'],
                "distance_km": dist,
                "total_latency_ms": total_time_ms,
                "content": payload['content']
            }
            record_request({
                "client_city": city_name,
                "file": filepath,
                "edge": edge_config["name"],
                "edge_id": edge_id,
                "cache_status": payload["cache_status"],
                "latency_ms": total_time_ms,
                "distance_km": dist,
                "content_size_bytes": len(str(payload["content"]).encode("utf-8")),
            })
            return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Request failed"}
