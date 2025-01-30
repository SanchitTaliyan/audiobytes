from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
import datetime

from models.base_model import Base

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