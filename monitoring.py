"""In-process observability state for the CDN simulator.

The simulator runs its Flask services in one Python process, so this module is a
safe, lightweight shared store.  It deliberately keeps only the most recent
100 requests to make the demo bounded and easy to understand.
"""

from collections import deque
from datetime import datetime, timezone
from threading import Lock
from persistence import init_db, load_requests, log_activity, save_request


_lock = Lock()
init_db()
_history = deque(load_requests(), maxlen=100)
_disabled_edges = set()


def record_request(record):
    """Add one completed request and return the stored record."""
    entry = {
        "timestamp": datetime.now(timezone.utc).astimezone().strftime("%H:%M:%S"),
        **record,
    }
    with _lock:
        _history.append(entry)
    save_request(entry)
    return entry


def activity(message, level="info"):
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%H:%M:%S")
    log_activity(timestamp, message, level)


def get_history():
    with _lock:
        return list(reversed(_history))


def set_edge_enabled(edge_id, enabled):
    with _lock:
        if enabled:
            _disabled_edges.discard(edge_id)
        else:
            _disabled_edges.add(edge_id)


def is_edge_enabled(edge_id):
    with _lock:
        return edge_id not in _disabled_edges


def disabled_edges():
    with _lock:
        return set(_disabled_edges)


def analytics():
    """Return chart-ready analytics calculated from the retained history."""
    with _lock:
        records = list(_history)

    total = len(records)
    hits = sum(item["cache_status"] == "HIT" for item in records)
    bandwidth_saved = sum(
        item.get("content_size_bytes", 0)
        for item in records
        if item["cache_status"] == "HIT"
    )
    average_latency = round(
        sum(item["latency_ms"] for item in records) / total, 2
    ) if total else 0
    per_edge = {}
    by_time = {}
    for item in records:
        per_edge[item["edge"]] = per_edge.get(item["edge"], 0) + 1
        by_time[item["timestamp"]] = by_time.get(item["timestamp"], 0) + 1

    return {
        "total_requests": total,
        "cache_hit_rate": round((hits / total) * 100, 1) if total else 0,
        "average_latency_ms": average_latency,
        "bandwidth_saved_bytes": bandwidth_saved,
        "requests_per_edge": per_edge,
        "requests_over_time": {
            "labels": list(by_time.keys()),
            "values": list(by_time.values()),
        },
    }
