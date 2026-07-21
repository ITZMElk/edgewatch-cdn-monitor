# Project Structure

```text
EdgeWatch/
├── cache_manager.py          # In-memory TTL cache implementation
├── client.py                 # Request simulation client and telemetry recorder
├── config.py                 # Server topology, ports, and city coordinates
├── dashboard_server.py       # Flask dashboard routes and API endpoints
├── dns_router.py             # Edge selection and failover routing logic
├── edge_server.py            # Edge server Flask app with cache behavior
├── geo_utils.py              # Geographic calculations and latency estimation
├── main.py                   # Multi-service startup entry point
├── monitoring.py             # In-memory analytics and request history state
├── noc_template.py           # Legacy dashboard template
├── noc_template_v2.py        # Premium NOC-style dashboard template
├── origin_server.py          # Origin server content endpoint
├── persistence.py            # SQLite persistence layer
├── requirements.txt          # Python dependency list
├── README.md                 # Project overview and setup guide
├── PROJECT_STRUCTURE.md      # Repository structure reference
├── .gitignore                # Git ignore rules for Python and VS Code
├── docker-compose.yml        # Container orchestration for local deployment
├── Dockerfile                # Container image definition
└── edgewatch.db              # Local SQLite database (ignored by git)
```
