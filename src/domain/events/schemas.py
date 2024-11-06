from datetime import datetime
from typing import Literal
from pydantic import BaseModel, field_validator


class UpdateEvent(BaseModel):
    event_id: str = ''
    status: Literal["win", "lose", "wait"]


class Event(BaseModel):
    id: str | None = None
    status: Literal["win", "lose", "wait"]
    coefficient: float = 1.50
    end_date: datetime | str

    @field_validator('coefficient')
    def round_to_two_decimal(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('end_date')
    def prepare_date(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value
