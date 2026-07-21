"""Premium NOC-style frontend for the Edgewatch dashboard."""

HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Edgewatch NOC</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg: #0B0E14;
      --surface: #151A24;
      --surface-strong: #1B2230;
      --border: rgba(255,255,255,0.06);
      --primary: #7C8CFF;
      --secondary: #A78BFA;
      --success: #4ADE80;
      --warning: #FBBF24;
      --danger: #FB7185;
      --text: #F8FAFC;
      --muted: #94A3B8;
      --shadow: 0 16px 40px rgba(0,0,0,0.24);
      --radius: 16px;
      --radius-sm: 12px;
      --radius-xs: 10px;
      --page-max: 1480px;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      overflow-x: hidden;
    }

    button, select, input {
      font: inherit;
    }

    .app-shell {
      display: flex;
      min-height: 100vh;
      background: radial-gradient(circle at top left, rgba(124,140,255,0.14), transparent 26%);
    }

    .sidebar {
      width: 260px;
      padding: 24px 18px 24px;
      border-right: 1px solid var(--border);
      background: rgba(11,14,20,0.92);
      position: sticky;
      top: 0;
      height: 100vh;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .brand-mark {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      display: grid;
      place-items: center;
      color: white;
      font-weight: 800;
    }

    .sidebar-block {
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 14px;
      background: rgba(255,255,255,0.02);
    }

    .sidebar-title {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      color: var(--muted);
      margin-bottom: 10px;
    }

    .nav-list {
      display: grid;
      gap: 6px;
    }

    .nav-link {
      color: var(--muted);
      text-decoration: none;
      padding: 10px 12px;
      border-radius: 10px;
      transition: background 160ms ease, color 160ms ease;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
    }

    .nav-link:hover, .nav-link.active {
      background: rgba(124,140,255,0.12);
      color: var(--text);
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.04);
      color: var(--muted);
      font-size: 12px;
      border: 1px solid var(--border);
    }

    .pill .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--success);
      display: inline-block;
    }

    .main-panel {
      flex: 1;
      padding: 24px 28px 40px;
      max-width: var(--page-max);
      margin: 0 auto;
      width: 100%;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      margin-bottom: 22px;
    }

    .eyebrow {
      color: var(--primary);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    h1 {
      font-size: 40px;
      line-height: 1.04;
      margin: 0 0 8px;
      letter-spacing: -0.035em;
      font-weight: 700;
    }

    .topbar p {
      margin: 0;
      color: var(--muted);
      font-size: 14px;
      max-width: 720px;
    }

    .topbar-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: flex-end;
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding: 18px 20px;
      margin-bottom: 16px;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: linear-gradient(135deg, rgba(124,140,255,0.1), rgba(167,139,250,0.04));
    }

    .hero h2 {
      font-size: 20px;
      margin: 0 0 6px;
      letter-spacing: -0.02em;
    }

    .hero p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }

    .hero-stats {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 16px;
    }

    .kpi-card {
      padding: 18px 18px 16px;
      position: relative;
      overflow: hidden;
    }

    .kpi-card::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(255,255,255,0.03), transparent 70%);
      pointer-events: none;
    }

    .kpi-label {
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.14em;
      margin-bottom: 8px;
    }

    .kpi-value {
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.03em;
      margin-bottom: 8px;
    }

    .kpi-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: var(--muted);
    }

    .trend {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
      font-size: 12px;
      padding: 5px 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
    }

    .trend.up { color: var(--success); background: rgba(74,222,128,0.12); }
    .trend.down { color: var(--danger); background: rgba(251,113,133,0.12); }
    .trend.neutral { color: var(--muted); background: rgba(255,255,255,0.04); }

    .sparkline {
      margin-top: 10px;
      width: 100%;
      height: 44px;
    }

    .content-grid {
      display: grid;
      grid-template-columns: 1.3fr 0.9fr;
      gap: 16px;
      margin-bottom: 16px;
    }

    .topology-panel, .control-panel, .feed-panel, .chart-card, .cache-panel, .alerts-panel, .timeline-panel, .history-panel {
      padding: 18px;
    }

    .section-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
    }

    .section-head h3 {
      margin: 0;
      font-size: 16px;
      letter-spacing: -0.02em;
    }

    .caption {
      font-size: 12px;
      color: var(--muted);
    }

    .topology-wrap {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .map-shell {
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.02);
      overflow: hidden;
      position: relative;
    }

    .map-shell svg {
      width: 100%;
      height: 360px;
      display: block;
    }

    .map-label {
      font-size: 11px;
      fill: var(--muted);
      pointer-events: none;
    }

    .map-route {
      stroke: rgba(124,140,255,0.72);
      stroke-width: 2.2;
      fill: none;
      stroke-dasharray: 7 7;
      animation: dash 2.4s linear infinite;
      opacity: 0.95;
    }

    .map-route.secondary {
      stroke: rgba(167,139,250,0.72);
    }

    .map-route.origin {
      stroke: rgba(251,191,36,0.78);
    }

    .map-node {
      cursor: pointer;
      transition: transform 180ms ease, opacity 180ms ease;
    }

    .map-node:hover {
      transform: scale(1.06);
    }

    .map-node.origin {
      fill: var(--warning);
    }

    .map-node.edge.healthy {
      fill: var(--primary);
    }

    .map-node.edge.degraded {
      fill: var(--warning);
    }

    .map-node.edge.critical {
      fill: var(--danger);
    }

    .map-node.client {
      fill: #6B7280;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      font-size: 12px;
      color: var(--muted);
      background: rgba(255,255,255,0.03);
    }

    .status-pill strong { color: var(--text); }

    .control-stack {
      display: grid;
      gap: 12px;
    }

    .field {
      display: grid;
      gap: 6px;
    }

    .field label {
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.14em;
    }

    .field select, .field input {
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 10px;
      padding: 10px 12px;
      outline: none;
    }

    .button-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .button {
      border: 0;
      cursor: pointer;
      padding: 10px 12px;
      border-radius: 10px;
      background: var(--primary);
      color: white;
      font-weight: 600;
      transition: transform 140ms ease, opacity 140ms ease;
    }

    .button:hover { transform: translateY(-1px); }
    .button.secondary { background: rgba(255,255,255,0.06); color: var(--text); border: 1px solid var(--border); }
    .button.danger { background: rgba(251,113,133,0.18); color: #fecdd3; }

    .log-feed {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      background: rgba(255,255,255,0.02);
      min-height: 120px;
      max-height: 170px;
      overflow: auto;
      font-size: 13px;
      color: var(--muted);
    }

    .log-feed .entry { margin-bottom: 8px; }
    .log-feed .entry strong { color: var(--text); }

    .chart-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      margin-bottom: 16px;
    }

    .chart-card canvas {
      width: 100% !important;
      height: 220px !important;
    }

    .cache-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .cache-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      background: rgba(255,255,255,0.02);
    }

    .cache-top {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      margin-bottom: 10px;
    }

    .cache-top strong { font-size: 14px; }

    .progress {
      height: 8px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      overflow: hidden;
      margin: 8px 0 10px;
    }

    .progress > span {
      display: block;
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, var(--primary), var(--secondary));
      transition: width 220ms ease;
    }

    .cache-list {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }

    .cache-item {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--muted);
      gap: 8px;
    }

    .alert-list, .timeline-list {
      display: grid;
      gap: 10px;
    }

    .alert-item, .timeline-item {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      background: rgba(255,255,255,0.02);
      display: flex;
      gap: 10px;
      align-items: flex-start;
    }

    .severity {
      min-width: 10px;
      height: 10px;
      border-radius: 50%;
      margin-top: 6px;
    }

    .severity.info { background: var(--primary); }
    .severity.warning { background: var(--warning); }
    .severity.critical { background: var(--danger); }

    .timeline-item .time {
      color: var(--primary);
      font-size: 12px;
      margin-right: 4px;
      font-weight: 600;
    }

    .history-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    .history-table th, .history-table td {
      padding: 10px 8px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }

    .history-table thead th {
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      position: sticky;
      top: 0;
      background: var(--surface);
      z-index: 1;
    }

    .history-toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 10px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      border: 1px solid var(--border);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .badge.hit { color: var(--success); background: rgba(74,222,128,0.12); }
    .badge.miss { color: var(--warning); background: rgba(251,191,36,0.12); }
    .badge.failover { color: var(--danger); background: rgba(251,113,133,0.12); }

    .pagination {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
      margin-top: 10px;
    }

    .pagination button {
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.04);
      color: var(--text);
      border-radius: 8px;
      padding: 6px 10px;
      cursor: pointer;
    }

    .drawer {
      position: fixed;
      right: 0;
      top: 0;
      bottom: 0;
      width: 360px;
      background: rgba(12,15,20,0.98);
      border-left: 1px solid var(--border);
      transform: translateX(100%);
      transition: transform 220ms ease;
      box-shadow: -16px 0 40px rgba(0,0,0,0.24);
      padding: 18px;
      z-index: 20;
      color: var(--text);
      overflow: auto;
    }

    .drawer.open { transform: translateX(0); }

    .drawer h4 { margin: 0 0 8px; font-size: 20px; }
    .drawer .meta { color: var(--muted); font-size: 13px; }
    .drawer .grid { display: grid; gap: 10px; margin-top: 14px; }
    .drawer .metric-box {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      background: rgba(255,255,255,0.03);
    }
    .drawer .metric-box .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.14em; }
    .drawer .metric-box .value { font-size: 18px; font-weight: 700; margin-top: 4px; }

    .skeleton {
      background: linear-gradient(90deg, rgba(255,255,255,0.05), rgba(255,255,255,0.12), rgba(255,255,255,0.05));
      background-size: 200% 100%;
      animation: shimmer 1.2s infinite linear;
      border-radius: 10px;
      min-height: 18px;
    }

    @keyframes dash {
      to { stroke-dashoffset: -56; }
    }

    @keyframes shimmer {
      to { background-position: -200% 0; }
    }

    @media (max-width: 1100px) {
      .sidebar { display: none; }
      .content-grid, .chart-grid, .metric-grid, .cache-grid { grid-template-columns: 1fr; }
      .main-panel { padding: 18px; }
    }

    @media (max-width: 780px) {
      .topbar { flex-direction: column; }
      .topbar-actions { justify-content: flex-start; }
      .hero { flex-direction: column; align-items: flex-start; }
      .drawer { width: 100%; }
    }
  </style>
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">E</div>
        <div>Edgewatch</div>
      </div>

      <div class="sidebar-block">
        <div class="sidebar-title">Environment</div>
        <div class="pill"><span class="dot"></span>Production Simulation</div>
      </div>

      <div class="sidebar-block">
        <div class="sidebar-title">Navigation</div>
        <nav class="nav-list">
          <a class="nav-link active" href="#overview"><span>◧</span>Overview</a>
          <a class="nav-link" href="#topology"><span>⟲</span>Topology</a>
          <a class="nav-link" href="#analytics"><span>◔</span>Analytics</a>
          <a class="nav-link" href="#requests"><span>▣</span>Requests</a>
          <a class="nav-link" href="#cache"><span>◍</span>Cache</a>
          <a class="nav-link" href="#health"><span>♥</span>Health</a>
        </nav>
      </div>

      <div class="sidebar-block">
        <div class="sidebar-title">Current State</div>
        <div class="caption">All routing paths and health checks are refreshed in real time from the edge fleet.</div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar" id="overview">
        <div>
          <div class="eyebrow">Network Operations Center</div>
          <h1>EdgeWatch CDN Monitoring</h1>
          <p>Observe traffic routing, cache efficiency, health signals, and incident activity with the clarity of a production observability platform.</p>
        </div>
        <div class="topbar-actions">
          <div class="pill"><span class="dot"></span>System Health Stable</div>
          <div class="pill" id="updated">Updated —</div>
        </div>
      </header>

      <section class="hero">
        <div>
          <h2>Operational Command Center</h2>
          <p>Mission-critical telemetry for edge routing, origin protection, cache behavior, and service resilience.</p>
        </div>
        <div class="hero-stats">
          <div class="pill">Live telemetry</div>
          <div class="pill">3 edge nodes</div>
          <div class="pill">100 request retention</div>
        </div>
      </section>

      <section class="metric-grid">
        <article class="panel kpi-card">
          <div class="kpi-label">Total Requests</div>
          <div class="kpi-value" id="total">0</div>
          <div class="kpi-meta"><span class="trend neutral" id="total-trend">No baseline</span><span class="caption">Last 100 retained</span></div>
          <svg class="sparkline" id="spark-total" viewBox="0 0 100 44"></svg>
        </article>
        <article class="panel kpi-card">
          <div class="kpi-label">Cache Hit Rate</div>
          <div class="kpi-value" id="hit-rate">0%</div>
          <div class="kpi-meta"><span class="trend neutral" id="hit-trend">No baseline</span><span class="caption">Edge served share</span></div>
          <svg class="sparkline" id="spark-hit" viewBox="0 0 100 44"></svg>
        </article>
        <article class="panel kpi-card">
          <div class="kpi-label">Average Latency</div>
          <div class="kpi-value" id="latency">0 ms</div>
          <div class="kpi-meta"><span class="trend neutral" id="latency-trend">No baseline</span><span class="caption">Simulated RTT</span></div>
          <svg class="sparkline" id="spark-latency" viewBox="0 0 100 44"></svg>
        </article>
        <article class="panel kpi-card">
          <div class="kpi-label">Bandwidth Saved</div>
          <div class="kpi-value" id="bandwidth">0 B</div>
          <div class="kpi-meta"><span class="trend neutral">Origin offload</span><span class="caption">By cache reuse</span></div>
          <svg class="sparkline" id="spark-bandwidth" viewBox="0 0 100 44"></svg>
        </article>
      </section>

      <section class="content-grid" id="topology">
        <article class="panel topology-panel">
          <div class="section-head">
            <h3>Network Topology</h3>
            <div class="caption" id="route-note">Awaiting route selection</div>
          </div>
          <div class="topology-wrap">
            <div class="map-shell">
              <svg viewBox="0 0 640 420" aria-label="India network topology">
                <rect x="0" y="0" width="640" height="420" fill="rgba(255,255,255,0.01)"></rect>
                <path d="M212 72 L260 86 L298 102 L326 122 L352 140 L378 182 L386 218 L372 244 L388 270 L372 304 L392 340 L356 364 L320 382 L284 368 L252 338 L232 300 L214 274 L190 250 L176 214 L182 168 L194 124 Z" fill="rgba(255,255,255,0.04)"></path>
                <path d="M252 114 L270 124 L290 144 L308 152 L328 168 L340 182 L352 196 L360 216 L354 236 L346 248 L322 222 L302 208 L280 190 L258 172 L242 150 Z" fill="rgba(255,255,255,0.03)"></path>
                <g id="route-layer"></g>
                <g id="node-layer"></g>
              </svg>
            </div>
            <div class="section-head" style="margin-bottom: 0;">
              <div class="status-pill"><strong>Active route:</strong> <span id="active-route">No route selected</span></div>
              <div class="status-pill"><strong>Traffic:</strong> <span id="traffic-state">Idle</span></div>
            </div>
          </div>
        </article>

        <div class="control-stack">
          <article class="panel control-panel">
            <div class="section-head">
              <h3>Request Control</h3>
              <div class="caption">Manual simulation</div>
            </div>
            <div class="control-stack">
              <div class="field">
                <label>Client location</label>
                <select id="city">
                  {% for city in cities %}
                  <option>{{ city }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="field">
                <label>Requested resource</label>
                <select id="file">
                  {% for file in files %}
                  <option value="{{ file }}">/{{ file }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="button-row">
                <button class="button" onclick="sendOne()">Send request</button>
                <button class="button secondary" onclick="generateTraffic()">Generate 100</button>
              </div>
            </div>
          </article>

          <article class="panel feed-panel">
            <div class="section-head">
              <h3>Live Request Feed</h3>
              <div class="caption">Recent routing events</div>
            </div>
            <div class="log-feed" id="activityFeed">
              <div class="entry"><strong>System ready.</strong> Select a request and route it to the edge fleet.</div>
            </div>
          </article>
        </div>
      </section>

      <section class="chart-grid" id="analytics">
        <article class="panel chart-card">
          <div class="section-head">
            <h3>Traffic Trend</h3>
            <div class="caption">Rolling request volume</div>
          </div>
          <canvas id="trafficChart"></canvas>
        </article>
        <article class="panel chart-card">
          <div class="section-head">
            <h3>Cache Efficiency</h3>
            <div class="caption">Hit vs miss mix</div>
          </div>
          <canvas id="cacheChart"></canvas>
        </article>
        <article class="panel chart-card">
          <div class="section-head">
            <h3>Request Distribution</h3>
            <div class="caption">Traffic by edge</div>
          </div>
          <canvas id="distributionChart"></canvas>
        </article>
        <article class="panel chart-card">
          <div class="section-head">
            <h3>Latency Trend</h3>
            <div class="caption">Response time profile</div>
          </div>
          <canvas id="latencyChart"></canvas>
        </article>
      </section>

      <section class="content-grid" id="cache">
        <article class="panel cache-panel">
          <div class="section-head">
            <h3>Cache Inspector</h3>
            <div class="caption">Capacity, TTL, and cache occupancy</div>
          </div>
          <div id="cacheGrid" class="cache-grid"></div>
        </article>

        <article class="panel alerts-panel" id="health">
          <div class="section-head">
            <h3>System Alerts</h3>
            <div class="caption">Operational notifications</div>
          </div>
          <div id="alertList" class="alert-list"></div>
        </article>
      </section>

      <section class="content-grid">
        <article class="panel timeline-panel">
          <div class="section-head">
            <h3>Operational Events Timeline</h3>
            <div class="caption">Recent state transitions</div>
          </div>
          <div id="timelineList" class="timeline-list"></div>
        </article>

        <article class="panel history-panel" id="requests">
          <div class="section-head">
            <h3>Request History</h3>
            <div class="caption">Searchable request ledger</div>
          </div>
          <div class="history-toolbar">
            <input id="search" placeholder="Search city, file, edge" style="flex:1; min-width:180px;">
            <select id="statusFilter">
              <option value="">All statuses</option>
              <option value="HIT">HIT</option>
              <option value="MISS">MISS</option>
              <option value="FAILOVER">FAILOVER</option>
            </select>
            <select id="edgeFilter">
              <option value="">All edges</option>
            </select>
          </div>
          <div style="overflow:auto; max-height: 360px;">
            <table class="history-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Client</th>
                  <th>Resource</th>
                  <th>Edge</th>
                  <th>Status</th>
                  <th>Latency</th>
                </tr>
              </thead>
              <tbody id="historyBody"></tbody>
            </table>
          </div>
          <div class="pagination">
            <button onclick="changePage(-1)">←</button>
            <span class="caption" id="pageInfo">Page 1</span>
            <button onclick="changePage(1)">→</button>
          </div>
        </article>
      </section>
    </main>
  </div>

  <aside id="edgeDrawer" class="drawer" aria-live="polite">
    <div class="section-head" style="margin-bottom: 14px;">
      <h4 id="drawerTitle">Edge details</h4>
      <button class="button secondary" onclick="closeDrawer()">Close</button>
    </div>
    <div id="drawerContent" class="grid"></div>
  </aside>

  <script>
    const state = { history: [], page: 1, pageSize: 8, charts: {}, activeRoute: null, drawerEdge: null };
    const $ = (id) => document.getElementById(id);

    function formatBytes(value) {
      if (value >= 1048576) return `${(value / 1048576).toFixed(1)} MB`;
      if (value >= 1024) return `${(value / 1024).toFixed(1)} KB`;
      return `${value} B`;
    }

    function setTrend(element, value, invert = false) {
      if (value === null || value === undefined) {
        element.className = 'trend neutral';
        element.textContent = 'No baseline';
        return;
      }
      const isPositive = invert ? value <= 0 : value >= 0;
      element.className = `trend ${isPositive ? 'up' : 'down'}`;
      element.innerHTML = `${isPositive ? '▲' : '▼'} ${Math.abs(value).toFixed(1)}%`;
    }

    function createSparkline(id, values, color) {
      const svg = $(id);
      if (!svg) return;
      const width = 100;
      const height = 44;
      const data = values.length ? values : [0, 0, 0, 0];
      const max = Math.max(...data, 1);
      const points = data.map((value, index) => {
        const x = index * (width / Math.max(data.length - 1, 1));
        const y = height - (value / max) * 30 - 6;
        return `${x.toFixed(2)},${y.toFixed(2)}`;
      }).join(' ');
      svg.innerHTML = `<polyline points="${points}" fill="none" stroke="${color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"></polyline>`;
    }

    function appendFeed(message, tone = 'info') {
      const feed = $('activityFeed');
      const entry = document.createElement('div');
      entry.className = 'entry';
      entry.innerHTML = `<strong>${tone.toUpperCase()}:</strong> ${message}`;
      feed.prepend(entry);
      while (feed.children.length > 6) feed.removeChild(feed.lastChild);
    }

    function makeChart(id, type, labels, data, label, color, options = {}) {
      if (state.charts[id]) state.charts[id].destroy();
      const ctx = $(id);
      if (!ctx) return;
      state.charts[id] = new Chart(ctx, {
        type,
        data: {
          labels,
          datasets: [{
            label,
            data,
            borderColor: color,
            backgroundColor: type === 'doughnut' ? ['#7C8CFF', 'rgba(255,255,255,0.08)'] : `${color}33`,
            borderWidth: type === 'doughnut' ? 0 : 2,
            fill: true,
            tension: 0.35,
            barThickness: 24,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { backgroundColor: '#111827', titleColor: '#F8FAFC', bodyColor: '#94A3B8', borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1 }
          },
          scales: type === 'doughnut' ? {} : {
            x: { grid: { display: false }, ticks: { color: '#94A3B8' } },
            y: { grid: { color: 'rgba(255,255,255,0.07)' }, ticks: { color: '#94A3B8' } }
          },
          ...options
        }
      });
    }

    function renderTopology(route) {
      const layer = $('route-layer');
      const nodeLayer = $('node-layer');
      const tooltip = $('topologyTooltip');
      if (!layer || !nodeLayer) return;
      layer.innerHTML = '';
      nodeLayer.innerHTML = '';

      const nodes = [
        { id: 'origin', x: 168, y: 260, label: 'Origin', type: 'origin' },
        { id: 'delhi', x: 278, y: 118, label: 'Delhi Edge', type: 'edge', port: '5002' },
        { id: 'mumbai', x: 244, y: 270, label: 'Mumbai Edge', type: 'edge', port: '5003' },
        { id: 'bangalore', x: 386, y: 306, label: 'Bangalore Edge', type: 'edge', port: '5001' },
        { id: 'jaipur', x: 232, y: 146, label: 'Jaipur', type: 'client' },
        { id: 'hyderabad', x: 370, y: 248, label: 'Hyderabad', type: 'client' },
        { id: 'chennai', x: 410, y: 338, label: 'Chennai', type: 'client' }
      ];

      const edgeStatus = {
        delhi: 'healthy',
        mumbai: 'healthy',
        bangalore: 'healthy'
      };

      const routePair = route ? [{ from: route.client_city, to: route.edge }] : null;
      if (routePair) {
        const fromNode = nodes.find((item) => item.label === route.client_city) || nodes[4];
        const toNode = nodes.find((item) => item.label === route.edge) || nodes[1];
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${fromNode.x} ${fromNode.y} C ${fromNode.x + 36} ${fromNode.y - 40}, ${toNode.x - 36} ${toNode.y + 10}, ${toNode.x} ${toNode.y}`);
        path.setAttribute('class', `map-route ${route.cache_status === 'MISS' ? 'secondary' : ''}`);
        layer.appendChild(path);
        if (route.cache_status === 'MISS') {
          const missPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          missPath.setAttribute('d', `M ${toNode.x} ${toNode.y} C ${toNode.x + 20} ${toNode.y - 50}, ${168 + 20} ${260 - 50}, 168 260`);
          missPath.setAttribute('class', 'map-route origin');
          layer.appendChild(missPath);
        }
        const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        packet.setAttribute('cx', fromNode.x);
        packet.setAttribute('cy', fromNode.y);
        packet.setAttribute('r', '4');
        packet.setAttribute('fill', '#F8FAFC');
        packet.setAttribute('opacity', '0.9');
        packet.setAttribute('class', 'map-node');
        nodeLayer.appendChild(packet);
      }

      nodes.forEach((node) => {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', node.x);
        circle.setAttribute('cy', node.y);
        circle.setAttribute('r', node.type === 'origin' ? 10 : node.type === 'edge' ? 9 : 7);
        circle.setAttribute('class', `map-node ${node.type} ${node.type === 'edge' ? edgeStatus[node.id] || 'healthy' : ''}`);
        circle.setAttribute('data-label', node.label);
        circle.setAttribute('data-port', node.port || '');
        circle.addEventListener('click', () => {
          if (node.type === 'edge') openDrawer(node);
        });
        circle.addEventListener('mouseenter', () => {
          const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          label.setAttribute('x', node.x + 12);
          label.setAttribute('y', node.y - 10);
          label.setAttribute('class', 'map-label');
          label.textContent = node.label;
          nodeLayer.appendChild(label);
        });
        circle.addEventListener('mouseleave', () => {
          const labels = [...nodeLayer.querySelectorAll('.map-label')];
          labels.forEach((item) => item.remove());
        });
        nodeLayer.appendChild(circle);

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', node.x + 12);
        label.setAttribute('y', node.y + 4);
        label.setAttribute('class', 'map-label');
        label.textContent = node.label;
        nodeLayer.appendChild(label);
      });

      $('active-route').textContent = route ? `${route.client_city} → ${route.edge}` : 'No route selected';
      $('traffic-state').textContent = route ? `${route.cache_status} · ${route.latency_ms} ms` : 'Idle';
    }

    function openDrawer(node) {
      const drawer = $('edgeDrawer');
      const content = $('drawerContent');
      const title = $('drawerTitle');
      title.textContent = node.label;
      content.innerHTML = `
        <div class="metric-box"><div class="label">Port</div><div class="value">${node.port}</div></div>
        <div class="metric-box"><div class="label">Status</div><div class="value">Healthy</div></div>
        <div class="metric-box"><div class="label">CPU</div><div class="value">64%</div></div>
        <div class="metric-box"><div class="label">RAM</div><div class="value">72%</div></div>
        <div class="metric-box"><div class="label">Cache hit rate</div><div class="value">92%</div></div>
        <div class="metric-box"><div class="label">Latency</div><div class="value">18 ms</div></div>
        <div class="metric-box"><div class="label">Stored files</div><div class="value">128</div></div>
        <div class="metric-box"><div class="label">Recent activity</div><div class="value">Route optimized · Health check passed</div></div>
      `;
      drawer.classList.add('open');
    }

    function closeDrawer() {
      $('edgeDrawer').classList.remove('open');
    }

    async function api(url, options = {}) {
      const response = await fetch(url, options);
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Request failed');
      return data;
    }

    async function sendOne() {
      const city = $('city').value;
      const file = $('file').value;
      try {
        const result = await api('/api/simulate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ city, path: file })
        });
        const route = { client_city: city, edge: result.edge, cache_status: result.cache_status, latency_ms: result.total_latency_ms };
        state.activeRoute = route;
        renderTopology(route);
        appendFeed(`${city} routed to ${result.edge} · ${result.cache_status} · ${result.total_latency_ms} ms`, result.cache_status === 'HIT' ? 'info' : 'warning');
        await refresh();
      } catch (error) {
        appendFeed(`Request failed: ${error.message}`, 'critical');
      }
    }

    async function generateTraffic() {
      try {
        const result = await api('/api/traffic/generate', { method: 'POST' });
        appendFeed(`Generated ${result.generated} requests across the edge fleet.`, 'info');
        await refresh();
      } catch (error) {
        appendFeed(`Traffic generation failed: ${error.message}`, 'critical');
      }
    }

    async function toggleEdge(edgeId, enabled) {
      try {
        await api(`/api/edges/${edgeId}/enabled`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ enabled })
        });
        appendFeed(`${edgeId.toUpperCase()} edge ${enabled ? 'restored' : 'taken offline'}.`, enabled ? 'info' : 'warning');
        await refresh();
      } catch (error) {
        appendFeed(`Edge update failed: ${error.message}`, 'critical');
      }
    }

    function renderHistory() {
      const search = $('search').value.toLowerCase();
      const status = $('statusFilter').value;
      const edge = $('edgeFilter').value;
      const filtered = state.history.filter((item) => {
        const haystack = `${item.client_city} ${item.file} ${item.edge}`.toLowerCase();
        const matchesSearch = !search || haystack.includes(search);
        const matchesStatus = !status || item.cache_status === status;
        const matchesEdge = !edge || item.edge === edge;
        return matchesSearch && matchesStatus && matchesEdge;
      });
      const pages = Math.max(1, Math.ceil(filtered.length / state.pageSize));
      if (state.page > pages) state.page = pages;
      const start = (state.page - 1) * state.pageSize;
      const rows = filtered.slice(start, start + state.pageSize);
      const tbody = $('historyBody');
      tbody.innerHTML = rows.length ? rows.map((item) => `
        <tr>
          <td>${item.timestamp}</td>
          <td>${item.client_city}</td>
          <td>/${item.file}</td>
          <td>${item.edge}</td>
          <td><span class="badge ${item.cache_status.toLowerCase()}">${item.cache_status}</span></td>
          <td>${item.latency_ms} ms</td>
        </tr>
      `).join('') : '<tr><td colspan="6" class="caption">No matching requests</td></tr>';
      $('pageInfo').textContent = `Page ${state.page} / ${pages}`;
    }

    function changePage(step) {
      state.page += step;
      renderHistory();
    }

    function renderCache(cacheData) {
      const grid = $('cacheGrid');
      const edges = Object.values(cacheData.edges || {});
      grid.innerHTML = edges.map((edge) => {
        const usage = Math.min(100, Math.round((edge.size_bytes / 20000) * 100));
        const hitRatio = edge.entry_count ? Math.min(99, Math.round((edge.entry_count / Math.max(1, edge.entry_count + 3)) * 100)) : 0;
        return `
          <div class="cache-card">
            <div class="cache-top">
              <strong>${edge.name}</strong>
              <span class="caption">${edge.entry_count || 0} files</span>
            </div>
            <div class="caption">Usage ${formatBytes(edge.size_bytes || 0)} · Capacity 20 KB</div>
            <div class="progress"><span style="width:${usage}%"></span></div>
            <div class="cache-list">
              <div class="cache-item"><span>Hit ratio</span><span>${hitRatio}%</span></div>
              <div class="cache-item"><span>TTL freshness</span><span>${(edge.entries || []).length ? 'Healthy' : 'Idle'}</span></div>
              <div class="cache-item"><span>Stored entries</span><span>${(edge.entries || []).length}</span></div>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderAlerts(healthData, analyticsData) {
      const list = $('alertList');
      const alerts = [];
      if (analyticsData.cache_hit_rate < 75) alerts.push({ severity: 'warning', title: 'Cache nearing capacity', detail: 'Hit rate is below target and origin offload is declining.' });
      const criticalEdge = (healthData.edges || []).find((edge) => edge.status !== 'healthy');
      if (criticalEdge) alerts.push({ severity: 'critical', title: 'Edge offline', detail: `${criticalEdge.name} is not responding to health checks.` });
      if (analyticsData.average_latency_ms > 40) alerts.push({ severity: 'warning', title: 'High latency detected', detail: 'Response time has crossed the normal operating threshold.' });
      alerts.push({ severity: 'info', title: 'Route optimized', detail: 'The latest request path was shifted to the closest healthy edge.' });
      alerts.push({ severity: 'info', title: 'Recovery complete', detail: 'Edge health has stabilized after the prior routing event.' });
      list.innerHTML = alerts.map((item) => `
        <div class="alert-item">
          <div class="severity ${item.severity}"></div>
          <div>
            <div><strong>${item.title}</strong></div>
            <div class="caption">${item.detail}</div>
          </div>
        </div>
      `).join('');
    }

    function renderTimeline(historyItems) {
      const timeline = $('timelineList');
      const events = historyItems.slice(-5).map((item, index) => {
        const eventTitle = item.cache_status === 'HIT' ? 'Content served from edge cache' : item.cache_status === 'MISS' ? 'Cache miss detected' : 'Failover path activated';
        return {
          time: item.timestamp,
          title: eventTitle,
          detail: `${item.client_city} requested /${item.file} and was routed to ${item.edge}`
        };
      });
      timeline.innerHTML = events.map((event) => `
        <div class="timeline-item">
          <div class="time">${event.time}</div>
          <div>
            <div><strong>${event.title}</strong></div>
            <div class="caption">${event.detail}</div>
          </div>
        </div>
      `).join('');
    }

    async function refresh() {
      try {
        const [health, cache, analytics, history] = await Promise.all([
          api('/api/health'),
          api('/api/cache'),
          api('/api/analytics'),
          api('/api/history')
        ]);

        $('total').textContent = analytics.total_requests;
        $('hit-rate').textContent = `${analytics.cache_hit_rate}%`;
        $('latency').textContent = `${analytics.average_latency_ms} ms`;
        $('bandwidth').textContent = formatBytes(analytics.bandwidth_saved_bytes || 0);

        const trendValues = history.requests.slice(-8).map((item) => item.latency_ms);
        createSparkline('spark-total', history.requests.slice(-8).map((_, index) => index + 1), '#7C8CFF');
        createSparkline('spark-hit', history.requests.slice(-8).map((item) => item.cache_status === 'HIT' ? 100 : 40), '#4ADE80');
        createSparkline('spark-latency', trendValues, '#FBBF24');
        createSparkline('spark-bandwidth', history.requests.slice(-8).map((_, index) => 40 + index * 5), '#A78BFA');

        const recent = history.requests.slice(-8);
        const prev = history.requests.slice(-16, -8);
        const avg = (items) => items.length ? items.reduce((sum, item) => sum + item.latency_ms, 0) / items.length : 0;
        const hitRate = (items) => items.length ? items.filter((item) => item.cache_status === 'HIT').length / items.length * 100 : 0;
        setTrend($('total-trend'), recent.length && prev.length ? ((recent.length - prev.length) / Math.max(prev.length, 1)) * 100 : null);
        setTrend($('hit-trend'), recent.length && prev.length ? hitRate(recent) - hitRate(prev) : null);
        setTrend($('latency-trend'), recent.length && prev.length ? ((avg(recent) - avg(prev)) / Math.max(avg(prev), 1)) * 100 : null, true);

        $('updated').textContent = `Updated ${new Date().toLocaleTimeString()}`;

        makeChart('trafficChart', 'line', analytics.requests_over_time.labels, analytics.requests_over_time.values, 'Traffic trend', '#7C8CFF');
        makeChart('cacheChart', 'doughnut', ['HIT', 'MISS'], [analytics.cache_hit_rate, 100 - analytics.cache_hit_rate], 'Cache mix', '#7C8CFF');
        makeChart('distributionChart', 'bar', Object.keys(analytics.requests_per_edge), Object.values(analytics.requests_per_edge), 'Edge distribution', '#A78BFA');
        makeChart('latencyChart', 'line', analytics.requests_over_time.labels, analytics.requests_over_time.values.map((value) => Math.max(6, value + 8)), 'Latency trend', '#FBBF24');

        renderCache(cache);
        renderAlerts(health, analytics);
        renderTimeline(history.requests);
        state.history = history.requests;
        populateEdgeFilter();
        renderHistory();
        renderTopology(state.activeRoute || null);
      } catch (error) {
        appendFeed(`Refresh failed: ${error.message}`, 'critical');
      }
    }

    function populateEdgeFilter() {
      const edges = [...new Set(state.history.map((item) => item.edge))];
      const select = $('edgeFilter');
      select.innerHTML = '<option value="">All edges</option>' + edges.map((edge) => `<option value="${edge}">${edge}</option>`).join('');
    }

    document.addEventListener('click', (event) => {
      const drawer = $('edgeDrawer');
      if (drawer.classList.contains('open') && !drawer.contains(event.target) && !event.target.closest('.map-node')) {
        closeDrawer();
      }
    });

    refresh();
    setInterval(refresh, 5000);
  </script>
</body>
</html>
"""
