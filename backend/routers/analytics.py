from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.db import get_db

router = APIRouter()

@router.get("/leaderboard/{hackathon_id}")
def leaderboard(hackathon_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM leaderboard WHERE hackathon_id = :id ORDER BY team_rank"),
        {"id": hackathon_id}
    )
    return [dict(row._mapping) for row in result]

@router.get("/colleges/{hackathon_id}")
def college_breakdown(hackathon_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM college_analytics WHERE hackathon_id = :id"),
        {"id": hackathon_id}
    )
    return [dict(row._mapping) for row in result]

@router.get("/submissions/{hackathon_id}")
def submission_overview(hackathon_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM submission_status WHERE hackathon_id = :id"),
        {"id": hackathon_id}
    )
    return [dict(row._mapping) for row in result]

@router.get("/summary/{hackathon_id}")
def hackathon_summary(hackathon_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT
            h.name,
            COUNT(DISTINCT t.id) AS total_teams,
            COUNT(DISTINCT p.id) AS total_participants,
            COUNT(DISTINCT s.id) AS total_submissions,
            COUNT(DISTINCT sc.id) AS total_scores_entered,
            h.prize_pool
        FROM hackathons h
        LEFT JOIN teams t ON t.hackathon_id = h.id
        LEFT JOIN participants p ON p.team_id = t.id
        LEFT JOIN submissions s ON s.hackathon_id = h.id
        LEFT JOIN scores sc ON sc.team_id = t.id
        WHERE h.id = :id
        GROUP BY h.id, h.name, h.prize_pool
    """), {"id": hackathon_id})
    return [dict(row._mapping) for row in result]