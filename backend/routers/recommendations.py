from datetime import time
from types import SimpleNamespace

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Event, Student
from backend.schemas.recommendation import RecommendationResponse
from backend.services.recommendation import build_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_active_events(db: Session):
    statement = (
        select(Event)
        .where(Event.deleted_at.is_(None))
        .order_by(Event.start_datetime)
    )
    return db.scalars(statement).all()


@router.get("", response_model=RecommendationResponse)
def get_recommendations_by_location(
    lat: float,
    lon: float,
    interests: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    custom_profile = SimpleNamespace(
        id=None,
        name="Custom profile",
        latitude=lat,
        longitude=lon,
        interests=interests,
        faculty="",
        available_from=time(0, 0),
        available_to=time(23, 59),
        max_price=None,
    )

    return {
        "student_id": None,
        "student_name": custom_profile.name,
        "recommendations": build_recommendations(
            custom_profile,
            get_active_events(db),
        ),
    }


@router.get("/{student_id}", response_model=RecommendationResponse)
def get_recommendations_for_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if not student or student.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Student not found.")

    return {
        "student_id": student.id,
        "student_name": student.name,
        "recommendations": build_recommendations(
            student,
            get_active_events(db),
        ),
    }