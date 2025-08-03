from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.app.database.database import Base

class TrackerEntry(Base):
    __tablename__ = "tracker_enrites"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tracker_entries")