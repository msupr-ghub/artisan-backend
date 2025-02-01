from pydantic import BaseModel

from app.models.user import User

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    def to_user(self) -> User:
        user = User()
        user.username = self.name
        user.email = self.email
        user.hashed_password = self.password
        return user

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    is_superuser: bool

    def from_user(self, user: User):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.is_active = user.is_active
        self.is_superuser = user.is_superuser
        return self