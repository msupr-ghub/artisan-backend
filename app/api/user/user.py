from fastapi import Depends, APIRouter
from sqlmodel import Session

from app.db.config import get_session
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = user.to_user()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return UserResponse().from_user(db_user)
