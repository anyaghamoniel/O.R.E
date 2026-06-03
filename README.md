# O.R.E - AI Workforce SaaS Platform

**Oniel and Ryan Enterprise**: A cloud-based AI workforce SaaS platform that allows businesses, marketers, agencies, and e-commerce brands to hire and interact with a team of specialized AI employees.

## 🎯 Vision

Instead of using separate AI tools for content creation, strategy, video editing, marketing, and distribution, users interact with a unified system of AI agents that can work independently or collaboratively.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FastAPI Backend                   │
├─────────────────────────────────────────────────────┤
│  • Task Router (Core Decision Engine)               │
│  • Workflow Engine (Multi-step execution)           │
│  • Agent Services (Independent AI Workers)          │
│  • Job Queue System (Redis + RQ)                    │
│  • Cloud Storage Integration                        │
│  • Database Layer (SQLite → PostgreSQL)             │
└─────────────────────────────────────────────────────┘
```

## 🧠 AI Employee System (Core Agents)

1. **Strategy Agent** - Research & Marketing Intelligence
2. **Script Agent** - Content & Copywriting
3. **Video Agent (Zoey)** - Video production & editing
4. **Voice Agent** - Audio & narration generation
5. **Media Agent** - Asset sourcing & content support
6. **Distribution Agent** - Social media posting & optimization

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI
- **Database**: SQLite (MVP) → PostgreSQL (Production)
- **Job Queue**: Redis + RQ
- **Video Processing**: FFmpeg
- **Storage**: Cloud storage integration

## 📁 Project Structure

```
O.R.E/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── agents/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── architecture.md
│   ├── api_design.md
│   └── deployment.md
└── .gitignore
```

## 🚀 Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/anyaghamoniel/O.R.E.git
cd O.R.E

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

### Running the Backend

```bash
# Start FastAPI server
uvicorn app.main:app --reload

# In another terminal, start Redis
redis-server

# In another terminal, start RQ worker
rq worker
```

## 📚 Documentation

- [Architecture](docs/architecture.md)
- [API Design](docs/api_design.md)
- [Deployment Guide](docs/deployment.md)

## 🔄 Development Roadmap

- [ ] Phase 1: Core Infrastructure (Task Router, Job Queue, Database)
- [ ] Phase 2: Video Agent (Zoey) - MVP
- [ ] Phase 3: Strategy Agent
- [ ] Phase 4: Script Agent
- [ ] Phase 5: Voice & Media Agents
- [ ] Phase 6: Distribution Agent
- [ ] Phase 7: Full Frontend & Dashboard
- [ ] Phase 8: Production Scaling (PostgreSQL, Celery)

## 📝 License

Private - O.R.E Platform

---

Built with ❤️ for AI-powered marketing automation
