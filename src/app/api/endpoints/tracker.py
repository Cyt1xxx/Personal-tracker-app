from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
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
    skip_entries: int = Query(0, description="Number of items to skip"),
    limit_entries: int = Query(25, description="Limit of entries in single page of user"),
    sort_by: str = Query("created_at", description="Sorts entries by parametr selected"),
    db: Session = Depends(get_db)
):
    allowed_limits = [25, 50, 75, 100]
    if limit_entries not in allowed_limits:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Limit must be one of {allowed_limits}"
        )
    
    entries = crud_tracker.get_tracker_entries_by_user(db=db, user_id=current_user.id, skip=skip_entries, limit=limit_entries, sort_by=sort_by)
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

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tracker_entry_api(
    entry_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    del_func = crud_tracker.delete_tracker_entry(db=db, entry_id=entry_id, user_id=current_user.id)
    if not del_func:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    