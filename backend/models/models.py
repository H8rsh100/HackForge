from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class Hackathon(Base):
    __tablename__ = "hackathons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    theme = Column(String(255))
    description = Column(Text)
    venue = Column(String(255))
    mode = Column(Enum('online', 'offline', 'hybrid'), default='offline')
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    max_teams = Column(Integer, default=50)
    registration_deadline = Column(DateTime)
    status = Column(Enum('upcoming', 'ongoing', 'completed'), default='upcoming')
    prize_pool = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime, server_default=func.now())
    teams = relationship("Team", back_populates="hackathon", cascade="all, delete")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id", ondelete="CASCADE"))
    team_name = Column(String(255), nullable=False)
    college = Column(String(255))
    project_idea = Column(Text)
    status = Column(Enum('registered', 'submitted', 'disqualified', 'winner'), default='registered')
    registered_at = Column(DateTime, server_default=func.now())
    hackathon = relationship("Hackathon", back_populates="teams")
    participants = relationship("Participant", back_populates="team", cascade="all, delete")

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    college = Column(String(255))
    year_of_study = Column(Integer)
    role = Column(Enum('leader', 'member'), default='member')
    github_profile = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    team = relationship("Team", back_populates="participants")

class Mentor(Base):
    __tablename__ = "mentors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    expertise = Column(String(255))
    organization = Column(String(255))
    availability = Column(Enum('available', 'busy'), default='available')
    created_at = Column(DateTime, server_default=func.now())

class Judge(Base):
    __tablename__ = "judges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    organization = Column(String(255))
    domain = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

class JudgingCriteria(Base):
    __tablename__ = "judging_criteria"
    id = Column(Integer, primary_key=True, index=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id", ondelete="CASCADE"))
    criterion_name = Column(String(255), nullable=False)
    description = Column(Text)
    max_score = Column(Integer, default=10)
    weightage = Column(DECIMAL(5, 2), default=1.00)

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    judge_id = Column(Integer, ForeignKey("judges.id", ondelete="CASCADE"))
    criterion_id = Column(Integer, ForeignKey("judging_criteria.id", ondelete="CASCADE"))
    score = Column(DECIMAL(5, 2), nullable=False)
    remarks = Column(Text)
    scored_at = Column(DateTime, server_default=func.now())
    __table_args__ = (UniqueConstraint('team_id', 'judge_id', 'criterion_id'),)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), unique=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id", ondelete="CASCADE"))
    project_title = Column(String(255), nullable=False)
    description = Column(Text)
    github_url = Column(String(500))
    demo_url = Column(String(500))
    tech_stack = Column(String(500))
    submitted_at = Column(DateTime, server_default=func.now())

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())