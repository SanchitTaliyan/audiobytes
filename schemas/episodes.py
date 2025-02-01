from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional, Union

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
    time_of_day: Union[TimeOfDay, str]

class EpisodeCreate(EpisodeBase):
    pass
    
class EpisodeInDBBase(EpisodeBase):
    id: int

class EpisodeResponse(EpisodeInDBBase):
    pass

class EpisodeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    published_at: Optional[datetime] = None
    audio_link: Optional[str] = None
    is_bookmark: Optional[bool] = None
    is_deleted: Optional[bool] = None
    time_of_day: Optional[TimeOfDay] = None