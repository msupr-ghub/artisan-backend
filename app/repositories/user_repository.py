from sqlmodel import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_system_user(self):
        return self.db.query(User).filter(User.username == 'system').first()

    def get_all(self):
        return self.db.query(User).all()

    def delete(self, user_id: int):
        user = self.get(user_id)
        self.db.delete(user)
        self.db.commit()
        return user

    def update(self, user_id: int, user: User):
        user = self.get(user_id)
        user.email = user.email
        user.password = user.password
        self.db.commit()