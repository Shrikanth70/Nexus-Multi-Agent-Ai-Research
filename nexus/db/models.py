from sqlalchemy import JSON, Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class DBTaskSession(Base):
    """Stores the overarching research session and its full NexusState as JSON."""
    __tablename__ = "task_sessions"

    session_id = Column(String, primary_key=True, default=lambda: f"req_{uuid.uuid4().hex[:8]}")
    user_query = Column(String, nullable=False)
    state_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
