# ⚡ HackForge

[![GitHub License](https://img.shields.io/github/license/H8rsh100/HackForge?style=for-the-badge&color=blue)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react)](https://react.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F27?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)

> **Unified Hackathon Management & Analytics Engine** — A professional database-centric portal designed to automate hackathon logistics. Track registrations, coordinate mentor assignments, calculate weighted judge scores, view real-time leaderboards, and monitor college performance metrics.

Developed as a **DBMS Course Project CP1 (Structured SQL & Relational Models)**.

---

## 🗺️ Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    HACKATHON {
        int id PK
        string name
        string theme
        string venue
        enum mode
        datetime start_date
        datetime end_date
        decimal prize_pool
    }
    TEAM {
        int id PK
        int hackathon_id FK
        string team_name
        string college
        enum status
    }
    PARTICIPANT {
        int id PK
        int team_id FK
        string name
        string email
        enum role
    }
    MENTOR {
        int id PK
        string name
        string email
        string expertise
        enum availability
    }
    MENTOR_ASSIGNMENT {
        int id PK
        int mentor_id FK
        int team_id FK
        int hackathon_id FK
    }
    JUDGE {
        int id PK
        string name
        string email
        string domain
    }
    JUDGING_CRITERIA {
        int id PK
        int hackathon_id FK
        string criterion_name
        int max_score
        decimal weightage
    }
    SCORE {
        int id PK
        int team_id FK
        int judge_id FK
        int criterion_id FK
        decimal score
    }
    SUBMISSION {
        int id PK
        int team_id FK
        int hackathon_id FK
        string project_title
        string github_url
    }
    ANNOUNCEMENT {
        int id PK
        int hackathon_id FK
        string title
    }

    HACKATHON ||--o{ TEAM : hosts
    TEAM ||--o{ PARTICIPANT : contains
    HACKATHON ||--o{ MENTOR_ASSIGNMENT : manages
    MENTOR ||--o{ MENTOR_ASSIGNMENT : fulfills
    TEAM ||--o{ MENTOR_ASSIGNMENT : receives
    HACKATHON ||--o{ JUDGING_CRITERIA : defines
    TEAM ||--o{ SCORE : graded-by
    JUDGE ||--o{ SCORE : evaluates
    JUDGING_CRITERIA ||--o{ SCORE : metrics
    TEAM ||--|| SUBMISSION : uploads
    HACKATHON ||--o{ SUBMISSION : tracks
    HACKATHON ||--o{ ANNOUNCEMENT : issues
```

---

## 🗄️ Database Features (RDBMS Layer)

This project leverages native relational constraints and operations to ensure high reliability and speed:
1. **Views**: 
   - `leaderboard`: Calculates weighted scoreboard indices using criterion weightage variables.
   - `college_analytics`: Aggregates performance matrices (registrations, scores) across colleges.
2. **Triggers**:
   - `after_submission_insert`: Auto-updates team state to `'submitted'` upon repository upload.
   - `prevent_score_overflow`: Validates that a judge's score does not exceed the criterion's max score cap.
   - `after_hackathon_end`: Automatically shifts active state to `'completed'` when the end date passes.
3. **Stored Procedures**:
   - `GetLeaderboard(hack_id)`: Fetches sorted rank arrays for a specific event.
   - `AssignMentor(mentor_id, team_id, hack_id)`: Assigns a mentor to a team and sets availability to `'busy'` within a single transaction.

---

## 🚀 Running HackForge Locally

### 1. Database Setup
Ensure you have MySQL installed and running:

```bash
mysql -u root -p -e "CREATE DATABASE hackforge;"
mysql -u root -p hackforge < backend/database/schema.sql
```

### 2. Backend API Setup
Create a `.env` file in the `backend/` directory:

```bash
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/hackforge
```

Run installation steps:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Swagger UI will be live at `http://localhost:8000/docs`.

### 3. Frontend Portal Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🤝 License

Distributed under the [MIT License](LICENSE).