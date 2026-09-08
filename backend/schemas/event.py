from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventCreate(BaseModel):
    title: str
    description: str
    category: str
    organizer: str
    location_name: str
    latitude: float
    longitude: float
    start_datetime: datetime
    end_datetime: datetime
    capacity: int = Field(ge=1)
    registered_count: int = Field(default=0, ge=0)
    target_audience: str
    price: float = Field(ge=0)
    is_online: bool = False


class EventResponse(EventCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)