from datetime import datetime

from pydantic import BaseModel


class RecommendationItem(BaseModel):
    event_id: int
    title: str
    category: str
    organizer: str
    location_name: str
    start_datetime: datetime
    end_datetime: datetime
    distance_km: float
    price: float
    available_places: int
    score: int
    reason: str


class RecommendationResponse(BaseModel):
    student_id: int | None
    student_name: str
    recommendations: list[RecommendationItem]