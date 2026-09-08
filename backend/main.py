from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from backend.database import engine


from backend.routers import events, students

from backend.routers import events, recommendations, students

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Campus Event Recommendation System",
    version="0.1.0",
)
    
app.include_router(students.router)
app.include_router(events.router)
app.include_router(recommendations.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Campus Event Recommendation System API"}


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed.",
        ) from error