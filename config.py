"""Configuration for the local CDN simulation environment."""

DASHBOARD_PORT = 8000

SERVERS = {
    "origin": {
        "name": "Mumbai Origin",
        "port": 5000,
        "url": "http://127.0.0.1:5000",
        "coords": (19.0760, 72.8777)
    },
    "edges": {
        "blr": {
            "name": "Bangalore Edge",
            "city": "Bangalore",
            "port": 5001,
            "url": "http://127.0.0.1:5001",
            "coords": (12.9716, 77.5946)
        },
        "del": {
            "name": "Delhi Edge",
            "city": "Delhi",
            "port": 5002,
            "url": "http://127.0.0.1:5002",
            "coords": (28.7041, 77.1025)
        },
        "bom": {
            "name": "Mumbai Edge",
            "city": "Mumbai",
            "port": 5003,
            "url": "http://127.0.0.1:5003",
            "coords": (19.0760, 72.8777)
        }
    }
}

CITIES = {
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Delhi": (28.7041, 77.1025),
    "Jaipur": (26.9124, 75.7873),
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777)
}
