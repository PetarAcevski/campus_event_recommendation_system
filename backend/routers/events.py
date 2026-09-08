from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Event
from backend.schemas.event import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=list[EventResponse])
def get_events(
    category: str | None = None,
    date: date | None = None,
    free_only: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    statement = select(Event).where(Event.deleted_at.is_(None))

    if category:
        statement = statement.where(
            func.lower(Event.category) == category.strip().lower()
        )

    if date:
        start_of_day = datetime.combine(date, time.min)
        start_of_next_day = start_of_day + timedelta(days=1)

        statement = statement.where(
            Event.start_datetime >= start_of_day,
            Event.start_datetime < start_of_next_day,
        )

    if free_only:
        statement = statement.where(Event.price == 0)

    statement = statement.order_by(Event.start_datetime)

    return db.scalars(statement).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)

    if not event or event.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Event not found.")

    return event


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    if event_data.registered_count > event_data.capacity:
        raise HTTPException(
            status_code=422,
            detail="Registered count cannot exceed capacity.",
        )

    event = Event(**event_data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)

    return event