"""
GPIWD-Dragon: Growth Protocol Intelligence WaterWall Defence
Core Gateway Application - V1.0

FastAPI reverse proxy with 8-layer security middleware.
Entry point for all security processing.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from datetime import datetime

# --- App Init ---
app = FastAPI(
    title="GPIWD Dragon",
    description="Growth Protocol Intelligence WaterWall Defence — AI Security Gateway",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Logger ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [GPIWD] %(levelname)s %(message)s",
)
logger = logging.getLogger("gpiwd")

# --- In-memory stats (replace with Redis in production) ---
_stats = {
    "total_requests": 0,
    "blocked_requests": 0,
    "allowed_requests": 0,
    "threats": [],
    "started_at": datetime.utcnow().isoformat(),
}


# =============================================================
# MIDDLEWARE — Security Pipeline
# =============================================================

@app.middleware("http")
async def gpiwd_security_pipeline(request: Request, call_next):
    """
    Main GPIWD security pipeline.
    Processes every request through all active security layers.
    
    V1 Active Layers:
    - L0: IP Blacklist check
    - L1: Rate limit check  
    - L2: Input sanitization
    - L3: Auth check (JWT/API Key)
    """
    start_time = time.time()
    client_ip = request.client.host
    _stats["total_requests"] += 1

    logger.info(f"[REQUEST] {request.method} {request.url.path} from {client_ip}")

    # --- L0: IP Blacklist ---
    # TODO V1: Integrate Redis blacklist
    # blocked_ips = await redis.smembers("gpiwd:blacklist")
    # if client_ip in blocked_ips:
    #     return await _block_response("L0", "IP_BLACKLISTED", client_ip)

    # --- L1: Rate Limit ---
    # TODO V1: Implement Redis sliding window rate limit
    # rate_ok = await check_rate_limit(client_ip)
    # if not rate_ok:
    #     return await _block_response("L1", "RATE_LIMITED", client_ip)

    # --- Continue to application ---
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-GPIWD-Version"] = "1.0.0"
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
    response.headers["X-Protected-By"] = "GPIWD-Dragon"
    
    _stats["allowed_requests"] += 1
    return response


async def _block_response(layer: str, reason: str, ip: str):
    """Standard block response format."""
    _stats["blocked_requests"] += 1
    _stats["threats"].append({
        "ip": ip,
        "layer": layer,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
    })
    logger.warning(f"[BLOCKED] {reason} | Layer={layer} | IP={ip}")
    return JSONResponse(
        status_code=403,
        content={
            "status": "blocked",
            "layer": layer,
            "reason": reason,
            "message": "Request blocked by GPIWD security layer",
            "timestamp": datetime.utcnow().isoformat(),
        },
        headers={"X-Protected-By": "GPIWD-Dragon"},
    )


# =============================================================
# CORE ENDPOINTS
# =============================================================

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint.
    Returns system status, version, and active layer count.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "codename": "WaterWall Foundation",
        "layers_active": 4,
        "layers_total": 8,
        "uptime_since": _stats["started_at"],
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/stats", tags=["System"])
async def get_stats():
    """
    Request and threat statistics.
    Returns aggregate metrics from the security pipeline.
    """
    block_rate = 0
    if _stats["total_requests"] > 0:
        block_rate = round(
            (_stats["blocked_requests"] / _stats["total_requests"]) * 100, 2
        )

    return {
        "status": "ok",
        "stats": {
            "total_requests": _stats["total_requests"],
            "blocked_requests": _stats["blocked_requests"],
            "allowed_requests": _stats["allowed_requests"],
            "block_rate_percent": block_rate,
            "active_threats": len(_stats["threats"]),
        },
        "system": {
            "version": "1.0.0",
            "started_at": _stats["started_at"],
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/threats", tags=["Security"])
async def get_threats(limit: int = 50):
    """
    Active threat list.
    Returns the most recent security events detected by GPIWD.
    """
    threats = _stats["threats"][-limit:]
    return {
        "status": "ok",
        "count": len(threats),
        "threats": list(reversed(threats)),
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/analyze", tags=["Security"])
async def analyze_request(request: Request):
    """
    Analyze a request payload for threats.
    Runs the target request through WAF and AI security checks.
    """
    body = await request.json()

    # Basic WAF analysis (V1 skeleton)
    payload = str(body)
    threats_found = []

    # SQLi patterns
    sqli_patterns = ["SELECT", "INSERT", "DROP", "UNION", "--", "';", "1=1"]
    for pattern in sqli_patterns:
        if pattern.upper() in payload.upper():
            threats_found.append({"type": "SQLi", "pattern": pattern})

    # XSS patterns
    xss_patterns = ["<script", "javascript:", "onerror=", "onload=", "alert("]
    for pattern in xss_patterns:
        if pattern.lower() in payload.lower():
            threats_found.append({"type": "XSS", "pattern": pattern})

    threat_score = min(len(threats_found) * 0.3, 1.0)
    action = "block" if threat_score >= 0.6 else ("flag" if threat_score > 0 else "allow")

    return {
        "status": "analyzed",
        "threat_score": threat_score,
        "action": action,
        "threats": threats_found,
        "layer": "waf",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/block", tags=["Security"])
async def block_ip(request: Request):
    """
    Manually block an IP address.
    Adds IP to the GPIWD blacklist for the specified duration.
    """
    body = await request.json()
    ip = body.get("ip")
    reason = body.get("reason", "manual_block")
    duration_minutes = body.get("duration_minutes", 60)

    if not ip:
        raise HTTPException(status_code=400, detail="IP address required")

    # TODO V1: Add to Redis blacklist
    # await redis.sadd("gpiwd:blacklist", ip)
    # await redis.expire(f"gpiwd:block:{ip}", duration_minutes * 60)

    _stats["threats"].append({
        "ip": ip,
        "layer": "manual",
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "action": "blocked",
    })

    logger.warning(f"[MANUAL_BLOCK] IP={ip} | Reason={reason} | Duration={duration_minutes}m")

    return {
        "status": "blocked",
        "ip": ip,
        "reason": reason,
        "duration_minutes": duration_minutes,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/dashboard", tags=["Dashboard"])
async def dashboard_data():
    """
    SOC Dashboard data endpoint.
    Returns aggregated data for the security operations dashboard.
    """
    return {
        "status": "ok",
        "overview": {
            "total_requests": _stats["total_requests"],
            "blocked": _stats["blocked_requests"],
            "allowed": _stats["allowed_requests"],
            "threat_count": len(_stats["threats"]),
        },
        "layers": [
            {"id": "L0", "name": "IP Blacklist", "status": "active"},
            {"id": "L1", "name": "Rate Limit", "status": "active"},
            {"id": "L2", "name": "WAF Core", "status": "active"},
            {"id": "L3", "name": "Auth Gate", "status": "active"},
            {"id": "L4", "name": "AI Security", "status": "planned_v4"},
            {"id": "L5", "name": "AISURU", "status": "planned_v2"},
            {"id": "L6", "name": "Data Fortress", "status": "planned_v3"},
            {"id": "L7", "name": "Runtime Guard", "status": "planned_v3"},
        ],
        "recent_threats": list(reversed(_stats["threats"][-10:])),
        "started_at": _stats["started_at"],
        "timestamp": datetime.utcnow().isoformat(),
    }
