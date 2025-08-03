from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.app.database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tracker_entries = relationship("TrackerEntry", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"