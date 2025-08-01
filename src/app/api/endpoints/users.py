from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.app.schemas.user import UserCreate, UserResponse
from src.app.models.user import User
from src.app.database.database import get_db
from src.app.crud import user as crud_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    new_user = crud_user.create_user(db=db, user=user)
    
    return new_user

@router.get("/{username}", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=username)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db_user