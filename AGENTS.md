# AGENTS.md — GPIWD Project Instructions

> This file is the **source of truth** for all AI assistants (Claude, Gemini, GPT-, Codex, Cursor, Windsurf) working on this codebase.
> Read this file **before writing any code**.

---

## Project Identity

```
Project   : GPIWD — Growth Protocol Intelligence WaterWall Defence
Tagline   : Your Server Has An Immune System
Author    : Muhamad Ridwan
Ecosystem : Golden Dragon Ecosystem
Website   : https://muhamadridwanjr.xyz
GitHub    : https://github.com/Muhamadridwanjr/GPIWD-Dragon
```

---

## Mission

Build an open-source adaptive security middleware that protects:
- REST APIs and Web Applications
- AI Agents and LLM endpoints
- Telegram Bots and messaging platforms
- Microservices and infrastructure
- RAG systems and memory stores

---

## Core Principles

1. **Security First** — Every decision starts with security implications
2. **Zero Trust** — Never trust, always verify. No implicit access
3. **Adaptive Learning** — The system gets smarter with every threat
4. **AI Security** — First-class support for protecting AI systems
5. **Open Source Friendly** — Clean code, great docs, easy to contribute
6. **Modular Architecture** — Each layer is independent and replaceable
7. **Developer Experience First** — Fast to install, easy to configure

---

## Architecture Rules

Every feature MUST belong to one of these layers:

```
Layer 1-10    → identity/        Identity & Perimeter
Layer 11-20   → network/         Network Shield
Layer 21-30   → gateway/         Access Control & Routing
Layer 31-40   → waf/             WAF Core
Layer 41-50   → ai_security/     AI Security Firewall
Layer 51-60   → aisuru/          Threat Intelligence
Layer 61-70   → aisuru/          AISURU Community
Layer 71-80   → data_fortress/   Data Fortress
Layer 81-90   → runtime_guard/   Runtime Guard
Layer 91-100  → audit/           Audit & Governance
```

**Never create modules outside this structure.**

---

## Naming Conventions

```python
# Module prefixes
gpiwd_*        # Core gateway modules
dragon_*       # Dragon-branded features (V3+)
aisuru_*       # AISURU community intelligence
antibody_*     # Threat memory and learning
shield_*       # Protection modules
guard_*        # Guard and monitoring modules
```

```python
# File naming
snake_case.py                    # All Python files
gpiwd_identity_engine.py        # Module files
test_gpiwd_identity_engine.py   # Test files
```

---

## Code Standards

### Python / FastAPI

```python
# Always use async
async def check_ip_reputation(ip: str) -> ThreatResult:
    ...

# Always type-hint
def analyze_request(request: Request) -> SecurityDecision:
    ...

# Always document
class IdentityEngine:
    """
    Layer 1-10: Identity & Perimeter security.
    Checks IP reputation, ASN, geolocation, and VPN detection.
    """
```

### Preferred Stack (V1)

```
Backend    : Python 3.11+ with FastAPI
Cache      : Redis 7+
Database   : PostgreSQL 15+
Container  : Docker + Docker Compose
Testing    : pytest + httpx
Linting    : ruff + black
```

---

## Security Requirements

- All new security modules MUST have unit tests in `tests/`
- No hardcoded secrets, tokens, or credentials — use `.env`
- All user inputs MUST be sanitized before processing
- Rate limiting MUST be applied to all public endpoints
- All security decisions MUST be logged to `audit/`

---

## Documentation Requirements

When implementing any feature, always update:

1. `README.md` — If it changes the user interface
2. `docs/` — Full technical documentation
3. `CHANGELOG.md` — Under `[Unreleased]` section

---

## API Design Rules

```python
# Standard response format
{
    "status": "ok" | "blocked" | "flagged",
    "layer": "identity" | "network" | "waf" | ...,
    "reason": "Human readable reason",
    "threat_score": 0.0-1.0,
    "action": "allow" | "block" | "challenge",
    "timestamp": "ISO 8601"
}
```

---

## V1 Scope (Do NOT exceed this)

V1 must deliver exactly these working features:

```
✅ Gateway reverse proxy on port 7777
✅ IP reputation check (AbuseIPDB integration)
✅ Rate limiting per IP (Redis-backed)
✅ WAF: SQLi + XSS detection
✅ JWT / API Key authentication
✅ Telegram alert on threat detection
✅ /health endpoint
✅ /stats endpoint
✅ /threats endpoint
✅ Docker Compose deployment
✅ Basic SOC dashboard (read-only)
```

Everything else belongs to V2+. Do not scope creep.

---

## Commit Convention

```
feat(layer): description          # New feature
fix(layer): description           # Bug fix
security(layer): description      # Security hardening
docs(layer): description          # Documentation
test(layer): description          # Test coverage
refactor(layer): description      # Code refactor
chore: description                # Tooling/config

# Examples:
feat(identity): add AbuseIPDB IP reputation check
fix(waf): correct XSS detection false positive for JSON
security(gateway): enforce TLS 1.3 minimum
```

---

## Directory Quick Reference

```
core/           → Shared utilities, base classes, config
gateway/        → Reverse proxy, routing, load balancing
identity/       → IP check, ASN, geo, VPN detection
network/        → Rate limit, DDoS, burst, port scan
waf/            → SQLi, XSS, SSRF, RCE, path traversal
ai_security/    → Prompt injection, jailbreak, agent guard
aisuru/         → Anomaly detection, pattern learning
data_fortress/  → Encryption, secrets, data masking
runtime_guard/  → Container monitoring, file integrity
audit/          → Logging, alerts, Telegram notifications
dashboard/      → React SOC dashboard frontend
docs/           → Full project documentation
tests/          → pytest test suite
docker/         → Dockerfiles and compose configs
examples/       → Integration examples
```

---

*🐉 One Dragon. One Kingdom. Infinite Protection.*
