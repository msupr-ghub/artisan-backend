from sqlmodel import Session

from app.models.user import User, UserType


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    async def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    async def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    async def get_system_user(self):
        return self.db.query(User).filter(User.user_type == UserType.SYSTEM).first()

    async def get_all(self):
        return self.db.query(User).all()

    async def delete(self, user_id: int):
        user = self.get(user_id)
        self.db.delete(user)
        self.db.commit()
        return user

    async def update(self, user_id: int, user: User):
        user = self.get(user_id)
        user.email = user.email
        user.password = user.password
        self.db.commit()