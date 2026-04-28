content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import hackathons, teams, participants, judges, scores, analytics

app = FastAPI(
    title="HackForge API",
    description="Hackathon Management Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hackathons.router, prefix="/api/hackathons", tags=["Hackathons"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(participants.router, prefix="/api/participants", tags=["Participants"])
app.include_router(judges.router, prefix="/api/judges", tags=["Judges"])
app.include_router(scores.router, prefix="/api/scores", tags=["Scores"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "HackForge API is live"}
"""

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("main.py fixed!")