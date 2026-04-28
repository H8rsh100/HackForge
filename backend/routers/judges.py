from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.db import get_db
from models.models import Judge, JudgingCriteria
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class JudgeCreate(BaseModel):
    name: str
    email: str
    organization: Optional[str]
    domain: Optional[str]

class CriteriaCreate(BaseModel):
    hackathon_id: int
    criterion_name: str
    description: Optional[str]
    max_score: int = 10
    weightage: float = 1.00

@router.get("/")
def get_all_judges(db: Session = Depends(get_db)):
    return db.query(Judge).all()

@router.post("/")
def create_judge(data: JudgeCreate, db: Session = Depends(get_db)):
    j = Judge(**data.dict())
    db.add(j)
    db.commit()
    db.refresh(j)
    return j

@router.delete("/{judge_id}")
def delete_judge(judge_id: int, db: Session = Depends(get_db)):
    j = db.query(Judge).filter(Judge.id == judge_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Judge not found")
    db.delete(j)
    db.commit()
    return {"message": "Deleted"}

@router.get("/criteria/{hackathon_id}")
def get_criteria(hackathon_id: int, db: Session = Depends(get_db)):
    return db.query(JudgingCriteria).filter(JudgingCriteria.hackathon_id == hackathon_id).all()

@router.post("/criteria")
def create_criteria(data: CriteriaCreate, db: Session = Depends(get_db)):
    c = JudgingCriteria(**data.dict())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c