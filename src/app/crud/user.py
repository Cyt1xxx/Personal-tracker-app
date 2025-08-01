from sqlalchemy.orm import Session
from src.app.models.user import User
from src.app.schemas.user import UserCreate

def get_password_hash(password: str) -> str:
    return password + "_hashed"

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username = user.username,
        password_hash = hashed_password,
        email = user.email,     
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

