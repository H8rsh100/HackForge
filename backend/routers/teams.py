from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.db import get_db
from models.models import Team, Submission
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TeamCreate(BaseModel):
    hackathon_id: int
    team_name: str
    college: Optional[str]
    project_idea: Optional[str]

class SubmissionCreate(BaseModel):
    hackathon_id: int
    project_title: str
    description: Optional[str]
    github_url: Optional[str]
    demo_url: Optional[str]
    tech_stack: Optional[str]

@router.get("/")
def get_all_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@router.get("/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    t = db.query(Team).filter(Team.id == team_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    return t

@router.get("/{team_id}/profile")
def get_team_profile(team_id: int, db: Session = Depends(get_db)):
    db.execute(text("CALL GetTeamFullProfile(:id)"), {"id": team_id})
    result = db.execute(text("CALL GetTeamFullProfile(:id)"), {"id": team_id})
    return [dict(row._mapping) for row in result]

@router.post("/")
def create_team(data: TeamCreate, db: Session = Depends(get_db)):
    t = Team(**data.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    t = db.query(Team).filter(Team.id == team_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(t)
    db.commit()
    return {"message": "Deleted successfully"}

@router.post("/{team_id}/submit")
def submit_project(team_id: int, data: SubmissionCreate, db: Session = Depends(get_db)):
    existing = db.query(Submission).filter(Submission.team_id == team_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team already submitted")
    sub = Submission(team_id=team_id, **data.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub