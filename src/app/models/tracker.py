from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.app.database.database import Base

class TrackerEntry(Base):
    __tablename__ = "tracker_entries"

    __table_args__ = (
        UniqueConstraint("owner_id", "title", name="_owner_id_title_uc"),
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tracker_entries")