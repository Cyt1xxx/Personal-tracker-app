from sqlalchemy.orm import Session
from typing import List

from src.app.models.tracker import TrackerEntry
from src.app.schemas.tracker import TrackerEntryCreate


def create_tracker_entry(db: Session, entry: TrackerEntryCreate, user_id: int) -> TrackerEntry:
    db_entry = TrackerEntry(
        title = entry.title,
        description = entry.description,
        owner_id = user_id
    )

    db.add(db_entry)

    db.commit()

    db.refresh(db_entry)

    return db_entry

def get_tracker_entries_by_user(db: Session, user_id: int) -> List[TrackerEntry]:
    return db.query(TrackerEntry).filter(TrackerEntry.owner_id == user_id).all()

def search_tracker_entries_by_title(db: Session, title: str, user_id: int) -> List[TrackerEntry]:
    return db.query(TrackerEntry).filter(
        TrackerEntry.owner_id == user_id,
        TrackerEntry.title.ilike(f"%{title}%")
    ).all()