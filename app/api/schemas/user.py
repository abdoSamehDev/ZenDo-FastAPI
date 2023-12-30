from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    first_name: str
    last_name: Optional[str] = None


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(UserBase):
    pass


class User(UserBase):
    id: int
    google_id: Optional[str] = None

    class Config:
        json_schema_extra = {"from_orm": True}
