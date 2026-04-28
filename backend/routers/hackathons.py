from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.db import get_db
from models.models import Hackathon
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class HackathonCreate(BaseModel):
    name: str
    theme: Optional[str]
    description: Optional[str]
    venue: Optional[str]
    mode: Optional[str] = "offline"
    start_date: datetime
    end_date: datetime
    max_teams: Optional[int] = 50
    registration_deadline: Optional[datetime]
    prize_pool: Optional[float] = 0.00

@router.get("/")
def get_all_hackathons(db: Session = Depends(get_db)):
    return db.query(Hackathon).all()

@router.get("/{hackathon_id}")
def get_hackathon(hackathon_id: int, db: Session = Depends(get_db)):
    h = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return h

@router.post("/")
def create_hackathon(data: HackathonCreate, db: Session = Depends(get_db)):
    h = Hackathon(**data.dict())
    db.add(h)
    db.commit()
    db.refresh(h)
    return h

@router.put("/{hackathon_id}")
def update_hackathon(hackathon_id: int, data: HackathonCreate, db: Session = Depends(get_db)):
    h = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    for key, value in data.dict().items():
        setattr(h, key, value)
    db.commit()
    db.refresh(h)
    return h

@router.delete("/{hackathon_id}")
def delete_hackathon(hackathon_id: int, db: Session = Depends(get_db)):
    h = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    db.delete(h)
    db.commit()
    return {"message": "Deleted successfully"}

@router.get("/{hackathon_id}/leaderboard")
def get_leaderboard(hackathon_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("CALL GetLeaderboard(:id)"), {"id": hackathon_id})
    return [dict(row._mapping) for row in result]

@router.get("/{hackathon_id}/announcements")
def get_announcements(hackathon_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM announcements WHERE hackathon_id = :id ORDER BY created_at DESC"),
        {"id": hackathon_id}
    )
    return [dict(row._mapping) for row in result]