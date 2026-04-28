from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import Participant
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ParticipantCreate(BaseModel):
    team_id: int
    name: str
    email: str
    phone: Optional[str]
    college: Optional[str]
    year_of_study: Optional[int]
    role: Optional[str] = "member"
    github_profile: Optional[str]

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(Participant).all()

@router.get("/{participant_id}")
def get_one(participant_id: int, db: Session = Depends(get_db)):
    p = db.query(Participant).filter(Participant.id == participant_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    return p

@router.post("/")
def create(data: ParticipantCreate, db: Session = Depends(get_db)):
    p = Participant(**data.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{participant_id}")
def delete(participant_id: int, db: Session = Depends(get_db)):
    p = db.query(Participant).filter(Participant.id == participant_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(p)
    db.commit()
    return {"message": "Deleted"}