from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
import pytest
import os

# Set dummy env vars so db.py engine initialization doesn't throw errors
os.environ["DB_USER"] = "test"
os.environ["DB_PASSWORD"] = "test"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "3306"
os.environ["DB_NAME"] = "hackforge"

# Mock the database engine for SQLite database
import models.models
from models.models import Base
from database.db import get_db

# Create a file-based SQLite database for testing to avoid connection sharing issues
TEST_DATABASE_URL = "sqlite:///test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Recreate the schema tables
Base.metadata.drop_all(bind=test_engine)
Base.metadata.create_all(bind=test_engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

from backend.main import app
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root_endpoint():
    """Verify live check endpoint returns status messages."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "HackForge API is live"}

def test_create_and_get_hackathon():
    """Test creating a new hackathon and retrieving it via SQLite."""
    response = client.post("/api/hackathons/", json={
        "name": "Hack Testing 2026",
        "theme": "Automated Quality Assurance",
        "description": "Mocked test environment for database models",
        "venue": "Virtual Testing Environment",
        "mode": "online",
        "start_date": "2026-07-05T09:00:00",
        "end_date": "2026-07-06T18:00:00",
        "max_teams": 30,
        "registration_deadline": "2026-07-01T23:59:59",
        "prize_pool": 1000.00
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Hack Testing 2026"
    assert data["id"] is not None
    
    # Retrieve the created hackathon
    get_res = client.get(f"/api/hackathons/{data['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["theme"] == "Automated Quality Assurance"

@patch("sqlalchemy.orm.Session.execute")
def test_get_leaderboard_mock(mock_execute):
    """Test leaderboard view execution (SQL View mocked due to MySQL dialect dependency)."""
    mock_row = MagicMock()
    mock_row._mapping = {
        "team_id": 1,
        "team_name": "TestNinjas",
        "college": "Test University",
        "weighted_score": 9.5,
        "judges_count": 3,
        "team_rank": 1
    }
    
    # Set up mock execute return structure
    mock_execute.return_value = [mock_row]
    
    response = client.get("/api/hackathons/1/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["team_name"] == "TestNinjas"
    assert data[0]["weighted_score"] == 9.5
