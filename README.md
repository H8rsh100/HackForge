# ⚡ HackForge

> Unified Hackathon Management & Analytics Engine

A full-stack application to manage hackathons end-to-end — teams, participants, judges, scoring, leaderboards, and analytics.

Built as **DBMS Course Project CP1 (Structured SQL)**.

## Tech Stack

- **Backend** — Python, FastAPI, SQLAlchemy, MySQL
- **Frontend** — React, Vite, Recharts
- **Database** — MySQL with Views, Triggers, Stored Procedures

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your DB credentials
uvicorn main:app --reload
```

### Database
```bash
mysql -u root -p < database/schema.sql
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Docs
Visit `http://localhost:8000/docs` for full Swagger UI.