from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class ConferenceModel(BaseModel):
    id: Optional[int]
    title: str
    description: str
    start_time: datetime = datetime.now()
    end_time: Optional[datetime]
    Capacity: int

    @classmethod
    @validator('capacity')
    def check_capacity(cls, v):
        if v <= 0:
            raise ValueError('Capacity must be greater than 0')
        return v

    @classmethod
    @validator('start_time', 'end_time', pre=True, always=True)
    def check_time(cls, v, values):
        if 'start_time' in values and 'end_time' in values and values['start_time'] >= values['end_time']:
            raise ValueError('start_time should be before end time')
        return v
