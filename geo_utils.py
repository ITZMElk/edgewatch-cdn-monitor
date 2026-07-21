# geo_utils.py
"""Utility functions for geographic distance and latency estimation."""

import math

def haversine_distance(coord1, coord2):
    """Calculate Great Circle distance between two lat/lon pairs in km."""
    R = 6371.0
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def estimate_latency(distance_km, is_hit=True):
    """Distance-based CDN latency: hits 20–40 ms, misses 250–400 ms."""
    if is_hit:
        return round(20 + min(20, distance_km * 0.012), 2)
    return round(250 + min(150, distance_km * 0.075), 2)
