"""Flask dashboard and monitoring API for the EdgeWatch observability platform."""

import random
import time

import requests
from flask import Flask, jsonify, render_template_string, request

from client import simulate_client
from config import CITIES, SERVERS
from monitoring import analytics, disabled_edges, get_history, set_edge_enabled

dashboard_app = Flask(__name__)
RESOURCE_FILES = ["index.html", "style.css", "app.js", "video.mp4"]
STARTED_AT = time.time()

LEGACY_TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edgewatch — CDN Monitoring</title><script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root{--bg:#0F1117;--surface:#171A23;--card:#1D2230;--card-strong:#212737;--border:rgba(255,255,255,.06);--indigo:#6D7CFF;--success:#3FB950;--warning:#F2C14E;--danger:#E05D5D;--text:#F5F7FA;--muted:#A0A8B8;--shadow:0 12px 32px rgba(0,0,0,.18)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:14px Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}.sidebar{position:fixed;inset:0 auto 0 0;width:238px;padding:26px 16px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;z-index:5}.brand{font-weight:650;font-size:17px;letter-spacing:-.02em;padding:8px 10px 30px}.brand-mark{display:inline-grid;place-items:center;width:25px;height:25px;margin-right:8px;background:var(--indigo);border-radius:7px;font-size:12px}.environment{margin:0 10px 24px;padding:9px 10px;border:1px solid var(--border);border-radius:9px;color:var(--muted);font-size:12px}.environment i{display:inline-block;width:7px;height:7px;background:var(--success);border-radius:50%;margin-right:7px}.nav{display:grid;gap:4px}.nav a{color:var(--muted);text-decoration:none;padding:10px;border-radius:8px;transition:background .18s,color .18s}.nav a:hover,.nav a.active{background:rgba(109,124,255,.12);color:var(--text)}.nav span{display:inline-block;width:24px;color:#c7cddd}.sidebar-footer{margin-top:auto;color:var(--muted);font-size:12px;padding:10px}.main{margin-left:238px;padding:42px 48px 70px;max-width:1740px}.topbar{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:38px}.eyebrow{font-size:11px;font-weight:600;letter-spacing:.1em;color:var(--indigo);margin-bottom:10px}h1{font-size:32px;letter-spacing:-.045em;margin:0;font-weight:650}h2{font-size:15px;letter-spacing:-.01em;margin:0;font-weight:600}.topbar p{color:var(--muted);margin:9px 0 0;font-size:15px}.timestamp{font-size:12px;color:var(--muted);padding:9px 11px;border:1px solid var(--border);border-radius:8px}.metrics{display:grid;grid-template-columns:1.16fr 1fr 1fr 1fr;gap:14px;margin-bottom:30px}.metric-card,.card{background:var(--card);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow)}.metric-card{padding:20px;min-height:144px}.metric-card.primary{background:var(--card-strong);border-color:rgba(109,124,255,.32)}.metric-label{color:var(--muted);font-size:12px}.metric-value{margin-top:12px;font-size:30px;letter-spacing:-.05em;font-weight:650}.metric-note{margin-top:9px;color:var(--muted);font-size:12px}.trend{display:inline-flex;margin-left:8px;font-size:11px;vertical-align:middle;padding:3px 6px;border-radius:999px}.trend.up{background:rgba(63,185,80,.12);color:#75d185}.trend.down{background:rgba(224,93,93,.12);color:#ed8989}.trend.neutral{background:rgba(160,168,184,.11);color:var(--muted)}.grid{display:grid;gap:16px}.topology-grid{grid-template-columns:minmax(0,1.55fr) minmax(340px,.8fr)}.analytics-grid{grid-template-columns:1.35fr .8fr .8fr}.card{padding:22px}.section-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.subtle{color:var(--muted);font-size:12px}.map{height:440px;width:100%;border-radius:10px;background:#151925;border:1px solid var(--border)}.india{fill:#202635;stroke:#53617d;stroke-width:1.2}.map-label{fill:#d7dce7;font-size:11px}.node-client{fill:#a0a8b8;stroke:#151925;stroke-width:4}.node-edge{fill:var(--indigo);stroke:#151925;stroke-width:4}.node-origin{fill:var(--warning);stroke:#151925;stroke-width:4}.route{stroke:#aeb8ff;stroke-width:3;stroke-dasharray:7 7;animation:route 1.7s linear infinite}.route-origin{stroke:#d9ae5e}@keyframes route{to{stroke-dashoffset:-28}}.legend{display:flex;gap:16px;color:var(--muted);font-size:12px;margin-top:13px}.legend i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px}.control-group{display:grid;gap:13px}.field label{color:var(--muted);font-size:12px;display:block;margin-bottom:6px}.field select,.filter-bar input,.filter-bar select{width:100%;background:#151925;color:var(--text);border:1px solid var(--border);padding:11px;border-radius:8px;outline:none;transition:border-color .18s}.field select:focus,.filter-bar input:focus,.filter-bar select:focus{border-color:rgba(109,124,255,.7)}.button{background:var(--indigo);color:white;border:0;border-radius:8px;padding:11px 13px;font-weight:600;cursor:pointer;transition:background .18s,transform .18s}.button:hover{background:#8190ff}.button:active{transform:translateY(1px)}.button.secondary{background:#2A3040}.button.danger{background:rgba(224,93,93,.16);color:#f19a9a;border:1px solid rgba(224,93,93,.22)}.activity{margin-top:18px;background:#151925;border:1px solid var(--border);border-radius:9px;padding:12px;height:165px;overflow:auto;color:var(--muted);font:12px ui-monospace,SFMono-Regular,Consolas,monospace;line-height:1.65}.health-list{display:grid;gap:8px}.health-row{display:grid;grid-template-columns:1fr auto;align-items:center;padding:13px 0;border-bottom:1px solid var(--border)}.health-row:last-child{border:0}.status{font-size:12px;font-weight:600}.online{color:var(--success)}.offline{color:var(--danger)}.status-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:currentColor;margin-right:6px}.chart-card canvas{max-height:255px}.chart-empty{display:none;position:absolute;inset:52px 0 0;place-items:center;color:var(--muted);font-size:12px;pointer-events:none}.chart-card{position:relative}.section{margin-top:32px}.cache-grid{grid-template-columns:repeat(3,1fr)}.cache-summary{display:flex;justify-content:space-between;color:var(--muted);font-size:12px;padding-bottom:12px;border-bottom:1px solid var(--border)}.cache-file{padding:11px 0;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;gap:8px}.filename{font:13px ui-monospace,SFMono-Regular,Consolas,monospace}.ttl{font-size:11px;color:var(--muted);white-space:nowrap}.memory{height:5px;border-radius:999px;background:#2A3040;margin:12px 0 3px;overflow:hidden}.memory i{display:block;height:100%;border-radius:inherit;background:var(--indigo)}.filter-bar{display:grid;grid-template-columns:1fr 160px 130px;gap:9px;margin-bottom:16px}.table-wrap{max-height:400px;overflow:auto;border:1px solid var(--border);border-radius:10px}table{width:100%;border-collapse:collapse;font-size:13px}thead{position:sticky;top:0;background:#202635;z-index:1}th{text-align:left;color:var(--muted);font-size:11px;font-weight:500;padding:12px 14px;border-bottom:1px solid var(--border)}td{padding:13px 14px;border-bottom:1px solid var(--border)}tbody tr:hover{background:rgba(255,255,255,.025)}.badge{font-size:11px;font-weight:600;padding:4px 7px;border-radius:999px}.badge.hit{background:rgba(63,185,80,.14);color:#89dc96}.badge.miss{background:rgba(242,193,78,.14);color:#f4d37e}.muted{color:var(--muted)}@media(max-width:1100px){.metrics{grid-template-columns:repeat(2,1fr)}.topology-grid,.analytics-grid{grid-template-columns:1fr}.cache-grid{grid-template-columns:1fr 1fr}}@media(max-width:760px){.sidebar{position:static;width:auto;height:auto;flex-direction:row;overflow:auto;padding:12px}.brand,.environment,.sidebar-footer{display:none}.nav{display:flex}.nav a{white-space:nowrap}.main{margin:0;padding:22px}.metrics,.cache-grid{grid-template-columns:1fr}.topbar{display:block}.timestamp{display:inline-block;margin-top:14px}.filter-bar{grid-template-columns:1fr}}
</style></head><body>
<aside class="sidebar"><div class="brand"><span class="brand-mark">E</span>Edgewatch</div><div class="environment"><i></i>Production simulation</div><nav class="nav"><a class="active" href="#overview"><span>⌂</span>Overview</a><a href="#topology"><span>⌘</span>Topology</a><a href="#analytics"><span>◔</span>Analytics</a><a href="#requests"><span>☷</span>Requests</a><a href="#cache"><span>▣</span>Cache</a><a href="#health"><span>♥</span>Health</a></nav><div class="sidebar-footer">CDN Monitor<br>v1.0 · Local environment</div></aside>
<main class="main"><header class="topbar"><div><div class="eyebrow">NETWORK OPERATIONS</div><h1>CDN overview</h1><p>Monitor edge performance, routing, cache efficiency, and service health.</p></div><div class="timestamp" id="updated">Last updated —</div></header>
<section id="overview" class="metrics"><div class="metric-card primary"><div class="metric-label">Total requests</div><div class="metric-value" id="total">0</div><div class="metric-note">Last 100 requests retained <span class="trend neutral" id="total-trend">No trend yet</span></div></div><div class="metric-card"><div class="metric-label">Cache hit rate</div><div class="metric-value" id="hit-rate">0%</div><div class="metric-note">Requests served from an edge <span class="trend neutral" id="hit-trend">No trend yet</span></div></div><div class="metric-card"><div class="metric-label">Average latency</div><div class="metric-value" id="latency">0 ms</div><div class="metric-note">End-to-end simulated latency <span class="trend neutral" id="latency-trend">No trend yet</span></div></div><div class="metric-card"><div class="metric-label">Bandwidth saved</div><div class="metric-value" id="bandwidth">0 B</div><div class="metric-note">Avoided origin transfers <span class="trend neutral" id="bandwidth-trend">Cache-derived</span></div></div></section>
<section id="topology" class="grid topology-grid"><div class="card"><div class="section-head"><h2>Network topology</h2><span class="subtle" id="route-note">No active route</span></div><svg class="map" viewBox="0 0 640 420" aria-label="India network topology"><path class="india" d="M276 37 L307 54 327 82 357 94 374 126 392 144 397 181 384 205 402 239 385 273 396 309 377 345 352 361 323 380 295 358 273 326 256 290 235 271 219 237 230 205 218 169 230 133 244 101 263 76 Z M406 166 L431 154 449 164 438 176 416 179 Z"/><path class="india" d="M438 343 l8 6 -5 12 -7 -6z M450 368 l7 6 -5 11 -7 -7z"/><g id="routes"></g><g><title>Delhi Edge · Port 5002 · northern edge</title><circle class="node-edge" cx="302" cy="104" r="9"/><text class="map-label" x="316" y="108">Delhi edge</text></g><g><title>Mumbai Origin · Port 5000 · primary origin</title><circle class="node-origin" cx="224" cy="244" r="10"/><text class="map-label" x="136" y="267">Mumbai origin</text></g><g><title>Mumbai Edge · Port 5003 · western edge</title><circle class="node-edge" cx="236" cy="266" r="9"/><text class="map-label" x="249" y="270">Mumbai edge</text></g><g><title>Bangalore Edge · Port 5001 · southern edge</title><circle class="node-edge" cx="310" cy="337" r="9"/><text class="map-label" x="324" y="341">Bangalore edge</text></g><g><title>Jaipur client</title><circle class="node-client" cx="278" cy="137" r="7"/><text class="map-label" x="216" y="137">Jaipur</text></g><g><title>Hyderabad client</title><circle class="node-client" cx="346" cy="246" r="7"/><text class="map-label" x="358" y="250">Hyderabad</text></g><g><title>Chennai client</title><circle class="node-client" cx="381" cy="323" r="7"/><text class="map-label" x="393" y="327">Chennai</text></g></svg><div class="legend"><span><i style="background:#6D7CFF"></i>Edge</span><span><i style="background:#F2C14E"></i>Origin</span><span><i style="background:#A0A8B8"></i>Client</span><span>Hover nodes for details</span></div></div>
<div class="card"><div class="section-head"><h2>Request control</h2><span class="subtle">Live simulation</span></div><div class="control-group"><div class="field"><label>Client location</label><select id="city">{% for city in cities %}<option>{{city}}</option>{% endfor %}</select></div><div class="field"><label>Requested resource</label><select id="file">{% for file in files %}<option value="{{file}}">/{{file}}</option>{% endfor %}</select></div><button class="button" onclick="sendOne()">Send request</button><button class="button secondary" onclick="generateTraffic()">Generate 100 random requests</button></div><div class="activity" id="log">System ready. Select a location and resource to begin.</div></div></section>
<section id="analytics" class="section"><div class="section-head"><h2>Analytics</h2><span class="subtle">Rolling request window</span></div><div class="grid analytics-grid"><div class="card chart-card"><canvas id="timeChart"></canvas><div class="chart-empty" id="time-empty">Traffic will appear as requests are routed.</div></div><div class="card chart-card"><canvas id="hitChart"></canvas><div class="chart-empty" id="hit-empty">No cache data yet.</div></div><div class="card chart-card"><canvas id="edgeChart"></canvas><div class="chart-empty" id="edge-empty">No edge distribution yet.</div></div></div></section>
<section id="cache" class="section"><div class="section-head"><h2>Cache inspector</h2><span class="subtle">TTL and memory usage by edge</span></div><div id="cache-grid" class="grid cache-grid"></div></section>
<section id="health" class="section"><div class="section-head"><h2>Health monitoring</h2><span class="subtle">Availability is checked every 3 seconds</span></div><div class="card"><div id="health-list" class="health-list"></div></div></section>
<section id="requests" class="section"><div class="section-head"><h2>Request history</h2><span class="subtle">Last 100 completed requests</span></div><div class="card"><div class="filter-bar"><input id="search" placeholder="Search city, file, or edge" oninput="renderHistory()"><select id="status-filter" onchange="renderHistory()"><option value="">All statuses</option><option>HIT</option><option>MISS</option></select><select id="edge-filter" onchange="renderHistory()"><option value="">All edges</option></select></div><div class="table-wrap"><table><thead><tr><th>Timestamp</th><th>Client city</th><th>Requested file</th><th>Routed edge</th><th>Cache status</th><th>Latency</th></tr></thead><tbody id="history-body"></tbody></table></div></div></section>
</main><script>
const edgePoints={"Delhi Edge":[302,104],"Mumbai Edge":[236,266],"Bangalore Edge":[310,337]},clients={"Delhi":[302,104],"Mumbai":[224,244],"Bangalore":[310,337],"Jaipur":[278,137],"Hyderabad":[346,246],"Chennai":[381,323]},origin=[224,244];let charts={},requestHistory=[];
const log=m=>{const e=document.querySelector('#log');e.innerHTML+=`<br>${m}`;e.scrollTop=e.scrollHeight}; const size=n=>n>=1048576?`${(n/1048576).toFixed(2)} MB`:n>=1024?`${(n/1024).toFixed(1)} KB`:`${n} B`; async function api(url,opts){const r=await fetch(url,opts),d=await r.json();if(!r.ok)throw Error(d.message||'Request failed');return d}
function drawRoute(r){const group=document.querySelector('#routes');group.replaceChildren();const a=clients[r.client_city],b=edgePoints[r.edge];if(!a||!b)return;const line=(from,to,originLine=false)=>{const el=document.createElementNS('http://www.w3.org/2000/svg','line');el.setAttribute('x1',from[0]);el.setAttribute('y1',from[1]);el.setAttribute('x2',to[0]);el.setAttribute('y2',to[1]);el.setAttribute('class',originLine?'route route-origin':'route');group.appendChild(el)};line(a,b);if(r.cache_status==='MISS')line(b,origin,true);document.querySelector('#route-note').textContent=`${r.client_city} → ${r.edge} · ${r.cache_status} · ${r.latency_ms} ms`}
async function sendOne(){const city=cityEl.value,file=fileEl.value;try{const r=await api('/api/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({city,path:file})});drawRoute({client_city:city,edge:r.edge,cache_status:r.cache_status,latency_ms:r.total_latency_ms});log(`${city} ${r.rerouted?'rerouted':'routed'} to <b>${r.edge}</b> · <span class="${r.cache_status==='HIT'?'online':'muted'}">${r.cache_status}</span> · ${r.total_latency_ms} ms`);refresh()}catch(e){log(`<span class="offline">Request failed: ${e.message}</span>`)} } const cityEl=document.querySelector('#city'),fileEl=document.querySelector('#file');
async function generateTraffic(){log('Generating 100 randomized requests…');try{const r=await api('/api/traffic/generate',{method:'POST'});log(`Completed ${r.generated} requests.`);refresh()}catch(e){log(`<span class="offline">${e.message}</span>`)} } async function toggle(id,enabled){await api(`/api/edges/${id}/enabled`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({enabled})});log(`${id.toUpperCase()} edge ${enabled?'restored':'taken offline'}; traffic will be rerouted.`);refresh()}
function chart(id,type,labels,data,label,color){if(charts[id])charts[id].destroy();charts[id]=new Chart(document.getElementById(id),{type,data:{labels,datasets:[{label,data,borderColor:color,backgroundColor:type==='doughnut'?["#6D7CFF","#303747"]:`${color}33`,borderWidth:2,fill:type==='line',tension:.35}]},options:{maintainAspectRatio:false,plugins:{legend:{display:type==='doughnut',labels:{color:'#A0A8B8',boxWidth:10}},title:{display:true,text:label,color:'#F5F7FA',align:'start',font:{size:13,weight:'500'}}},scales:type==='doughnut'?{}:{x:{grid:{display:false},ticks:{color:'#A0A8B8'}},y:{grid:{color:'rgba(255,255,255,.06)'},ticks:{color:'#A0A8B8'},beginAtZero:true}}}})}
function renderHistory(){const q=search.value.toLowerCase(),s=statusFilter.value,e=edgeFilter.value;historyBody.innerHTML=requestHistory.filter(r=>!q||`${r.client_city} ${r.file} ${r.edge}`.toLowerCase().includes(q)).filter(r=>!s||r.cache_status===s).filter(r=>!e||r.edge===e).map(r=>`<tr><td class="muted">${r.timestamp}</td><td>${r.client_city}</td><td class="filename">/${r.file}</td><td>${r.edge}</td><td><span class="badge ${r.cache_status==='HIT'?'hit':'miss'}">${r.cache_status}</span></td><td>${r.latency_ms} ms</td></tr>`).join('')||'<tr><td colspan="6" class="muted">No matching requests</td></tr>'}const search=document.querySelector('#search'),statusFilter=document.querySelector('#status-filter'),edgeFilter=document.querySelector('#edge-filter'),historyBody=document.querySelector('#history-body');
function setTrend(id,value,goodWhenUp=true){const el=document.querySelector('#'+id);if(value===null){el.className='trend neutral';el.textContent='No trend yet';return}const good=goodWhenUp?value>=0:value<=0;el.className=`trend ${good?'up':'down'}`;el.textContent=`${value>=0?'↑':'↓'} ${Math.abs(value).toFixed(1)}%`}
function updateEmpty(hasData){['time','hit','edge'].forEach(id=>document.querySelector('#'+id+'-empty').style.display=hasData?'none':'grid')}
async function refresh(){try{const [health,cache,stats,history]=await Promise.all([api('/api/health'),api('/api/cache'),api('/api/analytics'),api('/api/history')]);total.textContent=stats.total_requests;hitRate.textContent=`${stats.cache_hit_rate}%`;latency.textContent=`${stats.average_latency_ms} ms`;bandwidth.textContent=size(stats.bandwidth_saved_bytes||0);const ordered=[...history.requests].reverse(),split=Math.floor(ordered.length/2),old=ordered.slice(0,split),recent=ordered.slice(split);const avg=a=>a.length?a.reduce((sum,x)=>sum+x.latency_ms,0)/a.length:0;const hit=a=>a.length?a.filter(x=>x.cache_status==='HIT').length/a.length*100:0;setTrend('total-trend',ordered.length>1?((recent.length-old.length)/Math.max(old.length,1))*100:null);setTrend('hit-trend',old.length&&recent.length?hit(recent)-hit(old):null);setTrend('latency-trend',old.length&&recent.length?((avg(recent)-avg(old))/Math.max(avg(old),1))*100:null,false);document.querySelector('#updated').textContent=`Updated ${new Date().toLocaleTimeString()}`;updateEmpty(stats.total_requests>0);chart('timeChart','line',stats.requests_over_time.labels,stats.requests_over_time.values,'Traffic trend','#6D7CFF');chart('hitChart','doughnut',['Cache hits','Cache misses'],[stats.cache_hit_rate,100-stats.cache_hit_rate],'Cache efficiency','#6D7CFF');chart('edgeChart','bar',Object.keys(stats.requests_per_edge),Object.values(stats.requests_per_edge),'Request distribution','#A98CFF');
healthList.innerHTML=health.edges.map(e=>`<div class="health-row"><div><strong>${e.name}</strong><div class="subtle">Port ${e.port} · ${e.enabled?'Routing enabled':'Routing disabled'}</div></div><div style="text-align:right"><div class="status ${e.status==='online'?'online':'offline'}"><i class="status-dot"></i>${e.status==='online'?'Online':'Offline'}</div><button class="button ${e.enabled?'danger':'secondary'}" style="margin-top:8px;padding:7px 9px;font-size:11px" onclick="toggle('${e.id}',${!e.enabled})">${e.enabled?'Simulate failure':'Restore edge'}</button></div></div>`).join('');cacheGrid.innerHTML=Object.values(cache.edges).map(c=>{const ratio=Math.min(100,(c.size_bytes/20000)*100);return `<div class="card"><div class="section-head"><h2>${c.name}</h2><span class="subtle">${c.entry_count} files</span></div><div class="cache-summary"><span>${size(c.size_bytes)} used</span><span>20 KB capacity</span></div><div class="memory"><i style="width:${ratio}%"></i></div>${c.entries.length?c.entries.map(x=>`<div class="cache-file"><span class="filename">${x.filename}</span><span class="ttl">TTL ${x.ttl_remaining_seconds}s · ${size(x.size_bytes)}</span></div>`).join(''):'<div class="cache-file muted">No files cached</div>'}</div>`}).join('');requestHistory=history.requests;const edges=[...new Set(requestHistory.map(r=>r.edge))];edgeFilter.innerHTML='<option value="">All edges</option>'+edges.map(e=>`<option>${e}</option>`).join('');renderHistory()}catch(e){log(`<span class="offline">Monitoring refresh failed: ${e.message}</span>`)} } const total=document.querySelector('#total'),hitRate=document.querySelector('#hit-rate'),latency=document.querySelector('#latency'),bandwidth=document.querySelector('#bandwidth'),healthList=document.querySelector('#health-list'),cacheGrid=document.querySelector('#cache-grid');refresh();setInterval(refresh,3000);
</script></body></html>"""


from noc_template_v2 import HTML_TEMPLATE


def edge_stats(edge_id, timeout=0.7):
    info = SERVERS["edges"][edge_id]
    try:
        response = requests.get(f"{info['url']}/stats", timeout=timeout)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as error:
        return None, str(error)


@dashboard_app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, cities=CITIES.keys(), files=RESOURCE_FILES)


@dashboard_app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.get_json(silent=True) or {}
    city, path = data.get("city"), data.get("path")
    if city not in CITIES or path not in RESOURCE_FILES:
        return jsonify({"message": "Choose a valid city and resource."}), 400
    result = simulate_client(CITIES[city], path, city)
    return jsonify(result), 200 if result.get("status") == "success" else 503


@dashboard_app.route("/api/history")
def history():
    return jsonify({"requests": get_history()})


@dashboard_app.route("/api/analytics")
def analytics_endpoint():
    return jsonify(analytics())


@dashboard_app.route("/api/stats")
def stats_compatibility():
    result = {"origin": SERVERS["origin"]}
    for edge_id, info in SERVERS["edges"].items():
        stats, _ = edge_stats(edge_id)
        result[edge_id] = {**info, "stats": stats or {"hits": 0, "misses": 0}}
    return jsonify(result)


@dashboard_app.route("/api/cache")
def cache():
    edges = {}
    for edge_id, info in SERVERS["edges"].items():
        stats, error = edge_stats(edge_id)
        cache_data = stats.get("cache", {}) if stats else {"entries": [], "entry_count": 0, "size_bytes": 0}
        edges[edge_id] = {"name": info["name"], **cache_data, "error": error}
    return jsonify({"edges": edges})


@dashboard_app.route("/api/health")
def health():
    disabled = disabled_edges()
    edges = []
    for edge_id, info in SERVERS["edges"].items():
        started = time.perf_counter()
        stats, error = edge_stats(edge_id)
        response_time = round((time.perf_counter() - started) * 1000, 1)
        enabled = edge_id not in disabled
        requests_served = (stats or {}).get("hits", 0) + (stats or {}).get("misses", 0)
        entries = (stats or {}).get("cache", {}).get("entry_count", 0)
        status = "healthy" if enabled and not error else "critical"
        edges.append({
            "id": edge_id, "name": info["name"], "port": info["port"], "enabled": enabled,
            "status": status, "availability": 99.99 if status == "healthy" else 0,
            "response_time_ms": response_time if not error else None,
            "cpu_percent": min(92, 18 + requests_served * 2),
            "memory_percent": min(88, 24 + entries * 7), "requests_served": requests_served,
            "cache_entries": entries,
        })
    return jsonify({"edges": edges, "uptime_seconds": round(time.time() - STARTED_AT)})


@dashboard_app.route("/api/edges/<edge_id>/enabled", methods=["POST"])
def update_edge(edge_id):
    if edge_id not in SERVERS["edges"]:
        return jsonify({"message": "Unknown edge."}), 404
    enabled = bool((request.get_json(silent=True) or {}).get("enabled"))
    set_edge_enabled(edge_id, enabled)
    return jsonify({"edge_id": edge_id, "enabled": enabled})


@dashboard_app.route("/api/traffic/generate", methods=["POST"])
def generate_traffic():
    generated = 0
    for _ in range(100):
        city = random.choice(list(CITIES))
        generated += simulate_client(CITIES[city], random.choice(RESOURCE_FILES), city).get("status") == "success"
    return jsonify({"generated": generated})
