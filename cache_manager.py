"""Simple in-memory TTL cache used by edge servers in the simulation."""

import time


class MemoryCache:
    def __init__(self, ttl_seconds=60):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key] # Expired
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())

    def list_keys(self):
        self._remove_expired()
        return list(self.cache.keys())

    def _remove_expired(self):
        now = time.time()
        for key, (_, timestamp) in list(self.cache.items()):
            if now - timestamp >= self.ttl:
                del self.cache[key]

    def inspect(self):
        """Return cache entries and a useful approximate payload size."""
        self._remove_expired()
        now = time.time()
        entries = []
        total_bytes = 0
        for key, (value, timestamp) in self.cache.items():
            size = len(str(value).encode("utf-8"))
            total_bytes += size
            entries.append({
                "filename": key,
                "ttl_remaining_seconds": max(0, round(self.ttl - (now - timestamp), 1)),
                "size_bytes": size,
            })
        return {"entries": entries, "entry_count": len(entries), "size_bytes": total_bytes}
