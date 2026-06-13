<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,8&height=220&section=header&text=GPIWD%20Dragon&fontSize=72&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Growth%20Protocol%20Intelligence%20WaterWall%20Defence&descAlignY=58&descSize=20"/>

<br/>

**🛡️ Your Server Has An Immune System.**

[![Version](https://img.shields.io/badge/Version-1.0.0--alpha-FF4500?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/Muhamadridwanjr/GPIWD-Dragon)
[![License](https://img.shields.io/badge/License-MIT-00C851?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](docker/)
[![Status](https://img.shields.io/badge/Status-Active_Dev-F7B731?style=for-the-badge)](https://github.com/Muhamadridwanjr/GPIWD-Dragon)

<br/>

> *"Bukan Firewall. Bukan WAF. Bukan SIEM.*
> *GPIWD adalah **AI Security Operating System** untuk infrastruktur modern."*

</div>

---

## 🧬 What is GPIWD?

**GPIWD (Growth Protocol Intelligence WaterWall Defence)** adalah open-source adaptive security middleware yang berdiri di antara internet dan aplikasi kamu.

Berbeda dari firewall konvensional yang hanya *memblokir*, GPIWD:

```
🔴 Firewall biasa     →  Block berdasarkan rules statis
🟡 WAF biasa          →  Deteksi berdasarkan signature
🟢 GPIWD              →  Signature + Behavior + Anomaly + AI Learning
```

GPIWD menjaga:
- 🌐 **REST APIs & Web Applications**
- 🤖 **AI Agents & LLM Endpoints**
- 💬 **Telegram Bots & Messaging Platforms**
- ☁️ **Infrastructure & Microservices**
- 🧠 **RAG Systems & Memory Stores**

---

## 🏗️ Architecture

```
                          INTERNET
                             │
                      Cloudflare Proxy
                             │
                    ┌────────┴────────┐
                    │  GPIWD Gateway  │  :7777
                    │  8-Layer Shield  │
                    └────────┬────────┘
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
┌─────┴──────┐        ┌──────┴──────┐        ┌──────┴──────┐
│ Identity   │        │  WAF Core   │        │  AI Shield  │
│ Engine     │        │  + Network  │        │  + AISURU   │
└────────────┘        └─────────────┘        └─────────────┘
      │                      │                      │
      └──────────────┬────────────────────────────┘
                     │
              ┌──────┴──────┐
              │   Audit &   │
              │  Dashboard  │
              └─────────────┘
                     │
              Target Application
```

---

## 🛡️ 8 Security Layers

| # | Layer | Module | Function |
|---|---|---|---|
| 1 | **Identity & Perimeter** | Identity Engine | IP Reputation, ASN, Geo, VPN Check |
| 2 | **Network Shield** | Network Shield | Rate Limit, DDoS, Burst, Port Scan |
| 3 | **Access Control** | Auth Gate | JWT, API Key, RBAC, Zero Trust |
| 4 | **WAF Core** | WAF Engine | SQLi, XSS, SSRF, RCE, Path Traversal |
| 5 | **AI Security Firewall** | Dragon Mind | Prompt Injection, Jailbreak, Agent Guard |
| 6 | **Threat Intelligence** | AISURU | Anomaly Detection, Pattern Learning, Antibody |
| 7 | **Data Fortress** | Data Shield | Encryption, Secret Mgmt, Data Masking |
| 8 | **Audit & Governance** | Audit Center | Logging, Alerts, Dashboard, Telegram |

> 🔥 **Layer 5 (AI Security Firewall)** adalah pembeda utama GPIWD dari semua WAF lainnya di dunia.

---

## 🚀 Quick Start

### Prerequisites

```bash
Python >= 3.11
Docker >= 24.x
Redis >= 7.x
PostgreSQL >= 15.x
```

### Installation

```bash
# Clone repository
git clone https://github.com/Muhamadridwanjr/GPIWD-Dragon.git
cd GPIWD-Dragon

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run with Docker (recommended)
docker compose up -d

# OR run locally
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7777 --reload
```

### Verify

```bash
curl http://localhost:7777/health
# {"status":"healthy","version":"1.0.0","layers":8}
```

---

## 📡 Core API Endpoints (V1)

```http
GET  /health          # System health check
GET  /stats           # Threat & request statistics
GET  /threats         # Active threat list
POST /analyze         # Analyze a request for threats
POST /block           # Manually block an IP/token
GET  /dashboard       # SOC dashboard data
```

---

## 🗂️ Repository Structure

```
GPIWD-Dragon/
├── core/                 # Core gateway engine
├── gateway/              # Reverse proxy & routing
├── identity/             # Identity & perimeter security
├── network/              # Network shield modules
├── waf/                  # Web Application Firewall
├── ai_security/          # AI Security Firewall (Dragon Mind)
├── aisuru/               # AISURU community intelligence
├── data_fortress/        # Data protection layer
├── runtime_guard/        # Runtime & container monitoring
├── audit/                # Logging, alerting, dashboard
├── dashboard/            # React SOC dashboard
├── docs/                 # Full documentation
├── tests/                # Unit & integration tests
├── docker/               # Docker configurations
├── examples/             # Usage examples
├── README.md
├── AGENTS.md             # AI contributor instructions
├── ROADMAP.md            # Version roadmap
├── CONTRIBUTING.md       # Contribution guide
└── CHANGELOG.md          # Version history
```

---

## 🗺️ Version Roadmap

| Version | Codename | Focus | Status |
|---|---|---|---|
| **V1.0** | WaterWall Foundation | Core Gateway, WAF, Dashboard | 🔄 **Active** |
| **V2.0** | AISURU Community | Anomaly Detection, Pattern Learning | 📋 Planned |
| **V3.0** | Dragon Guardian | Dragon Kingdom Branding | 📋 Planned |
| **V4.0** | Dragon Mind | AI Security Firewall | 📋 Planned |
| **V5.0** | Dragon Emperor | Enterprise, Multi-Tenant | 📋 Planned |
| **V6.0** | Dragon Cloud | SaaS, Hosted Security | 🔮 Vision |
| **V10.0** | Dragon Guardian Prime | Full AI Security OS | 🔮 Vision |

---

## 💻 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

</div>

---

## 🤝 Contributing

GPIWD adalah proyek open source. Kontribusi sangat disambut!

1. Fork repo ini
2. Buat branch: `feature/nama-fitur`
3. Commit dengan [Conventional Commits](https://www.conventionalcommits.org/)
4. Open Pull Request

Baca [CONTRIBUTING.md](CONTRIBUTING.md) dan [AGENTS.md](AGENTS.md) sebelum mulai.

---

## 📄 License

MIT License — lihat [LICENSE](LICENSE) untuk detail lengkap.

---

<div align="center">

**🐉 "The Smarter The Attack, The Stronger We Get."**

**"One Dragon. One Kingdom. Infinite Protection."** 🛡️🚀

*Built with 🔥 by [Muhamad Ridwan](https://muhamadridwanjr.xyz) · Golden Dragon Ecosystem · Indonesia 🇮🇩*

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,8&height=100&section=footer"/>

</div>
