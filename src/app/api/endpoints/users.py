from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.app.schemas.user import UserCreate, UserResponse
from src.app.models.user import User
from src.app.database.database import get_db
from src.app.crud import user as crud_user
from src.app.schemas.user import Token
from src.app.security import create_access_token
from src.app.core.config import get_settings
from datetime import timedelta

settings = get_settings()

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

@router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    if not crud_user.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    #TODO: Create role scheme in Pydantic model and make alembic migration with it, make asyncio CRUD functions
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": "user"},
        expires_delta= access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"} 
