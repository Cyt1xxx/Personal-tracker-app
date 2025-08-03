from sqlalchemy.orm import Session
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

