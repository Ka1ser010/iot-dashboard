from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReadingCreate(BaseModel):
    temperature: float
    humidity: float


class ReadingOut(ReadingCreate):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
