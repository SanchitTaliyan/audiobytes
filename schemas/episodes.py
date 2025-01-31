from datetime import datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Optional

from models.episodes import TimeOfDay

__all__ = (
    "EpisodeCreate",
    "EpisodeInDBBase",
    "EpisodeUpdate",
    "EpisodeResponse",
)
    
class EpisodeBase(BaseModel):
    title: str
    description: str
    duration: int
    published_at: datetime
    audio_link: str
    is_bookmark: bool
    is_deleted: bool
    time_of_day: TimeOfDay

class EpisodeCreate(EpisodeBase):
    pass
    
class EpisodeInDBBase(EpisodeBase):
    id: int

class EpisodeResponse(EpisodeInDBBase):
    pass

class EpisodeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    duration: Optional[int]
    published_at: Optional[datetime]
    audio_link: Optional[str]
    is_bookmark: Optional[bool]
    is_deleted: Optional[bool]
    time_of_day: Optional[TimeOfDay]