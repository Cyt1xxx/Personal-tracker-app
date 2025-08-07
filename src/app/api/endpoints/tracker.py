from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List
from src.app.models.user import User
from src.app.schemas.tracker import TrackerEntryCreate, TrackerEntryResponse
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