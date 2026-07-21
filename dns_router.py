"""Route selection logic for choosing the nearest healthy edge server."""

from config import SERVERS
from geo_utils import haversine_distance
from monitoring import is_edge_enabled


def resolve_edge(client_coords):
    """Finds the nearest Edge server based on Haversine distance."""
    closest_edge_id = None
    min_distance = float('inf')

    for edge_id, config in SERVERS['edges'].items():
        if not is_edge_enabled(edge_id):
            continue
        dist = haversine_distance(client_coords, config['coords'])
        if dist < min_distance:
            min_distance = dist
            closest_edge_id = edge_id

    if closest_edge_id is None:
        raise RuntimeError("No edge servers are currently available")
    return closest_edge_id, SERVERS['edges'][closest_edge_id], min_distance
