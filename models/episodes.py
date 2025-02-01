from enum import Enum as PyEnum
import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, Index

from models.base_model import Base

class TimeOfDay(PyEnum):
    MORNING = "MORNING"
    MIDDAY = "MIDDAY"
    ENDOFDAY = "ENDOFDAY"
    ENDOFWEEK = "ENDOFWEEK"

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)  # Duration in minutes
    published_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    audio_link = Column(String, nullable=False)
    is_bookmark = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    time_of_day: Column[Enum] = Column(Enum(*[enum.value for enum in TimeOfDay], name="episode_time"), nullable=False)
    demo_flag = Column(Boolean, default=True)

    # Creating indexes for is_bookmark and time_of_day columns
    __table_args__ = (
        Index('idx_is_bookmark', 'is_bookmark'),
        Index('idx_time_of_day', 'time_of_day'),
    )