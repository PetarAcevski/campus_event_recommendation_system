from datetime import time

from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    name: str
    email: str
    faculty: str
    year_of_study: int
    latitude: float
    longitude: float
    interests: str
    available_from: time
    available_to: time
    max_price: float


class StudentResponse(StudentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)