from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from typing import List
from src.app.models.user import User
from src.app.models.tracker import TrackerEntry
from src.app.schemas.tracker import TrackerEntryCreate, TrackerEntryResponse, TrackerEntryUpdate
from src.app.crud import tracker as crud_tracker
from src.app.database.database import get_db
from src.app.security import get_current_user_from_token

router = APIRouter(
    prefix="/tracker",
    tags=["tracker"]
)

@router.post("/", response_model=TrackerEntryResponse, status_code=status.HTTP_201_CREATED)
def create_tracker_entry_api(
    entry: TrackerEntryCreate,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    
    return crud_tracker.create_tracker_entry(db=db, entry=entry, user_id=current_user.id)

@router.get("/", response_model=List[TrackerEntryResponse])
def read_tracker_entries(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    entries = crud_tracker.get_tracker_entries_by_user(db=db, user_id=current_user.id)
    return entries

@router.get("/search", response_model=List[TrackerEntryResponse])
def sarch_tracker_entries(
    title: str = Query(..., description = "The title of the tracker entry to search for"),
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    entries = crud_tracker.search_tracker_entries_by_title(db=db, title=title, user_id=current_user.id)
    return entries 

@router.put("/{entry_id}", response_model=TrackerEntryUpdate, status_code=status.HTTP_200_OK)
def update_tracker_entry_api(
    entry: TrackerEntryUpdate,
    entry_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    entry_update = crud_tracker.update_tracker_entry(db=db, entry_id=entry_id, user_id=current_user.id, entry_update=entry)
    if not entry_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )
    return entry_update