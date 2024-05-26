from pydantic import BaseModel, Field, EmailStr
from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class User(Base):
    __tablename__ = "usuarios"

    first_name = Column(String)
    last_name = Column(String)
    country = Column(String)
    city = Column(String)
    phone = Column(String)
    email = Column(String, primary_key=True, index=True)
    password = Column(String)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Jhon",
                "last_name": "Doe",
                "country": "Colombia",
                "city": "Bogota",
                "phone": "1234567",
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class UsedAccessToken(Base):
    __tablename__ = "used_access_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWJkdWxhemVleiJ9.1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI",
            }
        }