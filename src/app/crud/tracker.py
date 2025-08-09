from sqlalchemy.orm import Session
from typing import List

from src.app.models.tracker import TrackerEntry
from src.app.schemas.tracker import TrackerEntryCreate, TrackerEntryUpdate


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

def get_tracker_entries_by_user(db: Session, user_id: int, skip: int, limit: int, sort_by: str) -> List[TrackerEntry]:
    return db.query(TrackerEntry).filter(TrackerEntry.owner_id == user_id).order_by(getattr(TrackerEntry, sort_by)).offset(skip).limit(limit).all()

def search_tracker_entries_by_title(db: Session, title: str, user_id: int) -> List[TrackerEntry]:
    return db.query(TrackerEntry).filter(
        TrackerEntry.owner_id == user_id,
        TrackerEntry.title.ilike(f"%{title}%")
    ).all()

def update_tracker_entry(db: Session, entry_id: int, user_id: int, entry_update: TrackerEntryUpdate) -> TrackerEntryUpdate | None:
    db_entry = db.query(TrackerEntry).filter(
        TrackerEntry.id == entry_id,
        TrackerEntry.owner_id == user_id     
    ).first()

    if not db_entry:
        return None

    update_data = entry_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_entry, key, value)

    db.commit()

    return db_entry


def delete_tracker_entry(db: Session, entry_id: int, user_id: int) -> bool:
    db_entry = db.query(TrackerEntry).filter(
        TrackerEntry.id == entry_id,
        TrackerEntry.owner_id == user_id
    ).first()

    if not db_entry:
        return False
    
    db.delete(db_entry)

    db.commit()

    return True