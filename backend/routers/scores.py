from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import Score
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ScoreCreate(BaseModel):
    team_id: int
    judge_id: int
    criterion_id: int
    score: float
    remarks: Optional[str]

@router.get("/")
def get_all_scores(db: Session = Depends(get_db)):
    return db.query(Score).all()

@router.post("/")
def submit_score(data: ScoreCreate, db: Session = Depends(get_db)):
    existing = db.query(Score).filter(
        Score.team_id == data.team_id,
        Score.judge_id == data.judge_id,
        Score.criterion_id == data.criterion_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Score already submitted for this criteria")
    s = Score(**data.dict())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.put("/{score_id}")
def update_score(score_id: int, data: ScoreCreate, db: Session = Depends(get_db)):
    s = db.query(Score).filter(Score.id == score_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Score not found")
    for key, value in data.dict().items():
        setattr(s, key, value)
    db.commit()
    db.refresh(s)
    return s