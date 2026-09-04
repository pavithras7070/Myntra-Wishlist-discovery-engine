import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Integer, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RawConversation(Base):
    __tablename__ = 'raw_conversations'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    platform = Column(String(50), nullable=False) # e.g., google_play, reddit, youtube
    source_url = Column(String(1000))
    author_hash = Column(String(256))
    content = Column(String, nullable=False)
    content_clean = Column(String)
    language = Column(String(10))
    date = Column(DateTime)
    rating = Column(Integer, nullable=True)
    metadata_json = Column(JSON)
    content_hash = Column(String(256), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_processed = Column(Boolean, default=False)
