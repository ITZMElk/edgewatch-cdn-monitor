# EdgeWatch – Distributed CDN Monitoring & Edge Cache Observability Platform

EdgeWatch is a Python-based distributed systems simulation that models a lightweight Content Delivery Network (CDN) with edge caching, routing, health monitoring, traffic generation, and a live observability dashboard. It is designed as a portfolio-ready demonstration of backend systems thinking, distributed architecture concepts, and practical monitoring patterns.

## Project Overview

EdgeWatch simulates a small CDN environment composed of:
- an origin server that hosts content,
- multiple edge servers with in-memory caches,
- a routing layer that selects the nearest available edge,
- a monitoring layer that records request performance and cache behavior,
- and a dashboard for visualizing traffic and operational health.

The platform demonstrates how a real-world CDN might route requests, cache responses, detect failures, and expose observability metrics to operators.

## Key Features

- DNS-style routing simulation for client requests
- Edge server monitoring and health checks
- Cache hit and miss analytics
- Request history persistence with SQLite
- Network topology visualization
- Traffic simulation and request generation
- Real-time dashboard with charts and operational metrics
- Lightweight architecture suitable for local experimentation and portfolio demos

## Architecture

```text
Client / Browser
    │
    ▼
Dashboard Server (Flask)
    │
    ├── Request Simulation API
    ├── Monitoring / Analytics API
    └── Cache & Health APIs
            │
            ▼
Routing Layer
    │
    └── Selects nearest available edge
            │
            ├── Edge Server 1 (Bangalore)
            ├── Edge Server 2 (Delhi)
            └── Edge Server 3 (Mumbai)
                    │
                    ▼
                Origin Server
```

## Tech Stack

- Python 3.10+
- Flask
- SQLite
- HTML, CSS, and JavaScript
- Chart.js
- Requests

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for the full repository layout.

## Installation

### Prerequisites

- Python 3.10 or newer
- pip

### Setup

```bash
git clone <repository-url>
cd EdgeWatch
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Access the Dashboard

Open your browser and visit:

```text
http://localhost:8000
```

## Usage

1. Launch the simulation with `python main.py`.
2. Open the dashboard in your browser.
3. Select a client city and resource.
4. Send a request to observe routing and cache behavior.
5. Generate traffic to populate analytics and request history.
6. Disable an edge to simulate failover and watch the routing behavior change.

## Screenshots

Add screenshots here as the project evolves:
- Dashboard overview
- Topology and route visualization
- Analytics and request history view
- Edge failover simulation

## Future Improvements

- Add real container orchestration for multi-service deployment
- Introduce authentication and role-based access for the dashboard
- Add more realistic latency and failure models
- Expand analytics with historical trend comparisons
- Replace the in-memory cache with a more production-like distributed cache
- Add automated tests for routing and monitoring logic

## License

This project is licensed under the MIT License.

## Portfolio Notes

EdgeWatch is a strong example of backend service design, distributed systems concepts, observability and monitoring patterns, lightweight API development, and practical Python engineering. It is suitable for internship applications, entry-level backend portfolios, and technical interview discussions.

## GitHub Repository Description

A Python-based CDN simulation platform for edge routing, cache observability, health monitoring, and live analytics.

## GitHub Topics

- python
- flask
- sqlite
- distributed-systems
- monitoring
- observability
- backend
- cdn
- portfolio-project
