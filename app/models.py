from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class UserCreate(BaseModel):
    name: str
    email: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50))
    email = Column(String(length=100))