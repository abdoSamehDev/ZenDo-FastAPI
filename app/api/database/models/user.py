from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.api.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    google_id = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="user")
