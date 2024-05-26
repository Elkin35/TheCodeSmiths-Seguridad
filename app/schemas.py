from pydantic import BaseModel, Field, EmailStr
from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class UserSchema(BaseModel):

    first_name: str = Field(...)
    last_name: str = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    phone: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

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

        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }

class UsedAccessTokenSchema(BaseModel):
    id: int = Field(default=None)
    token: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWJkdWxhemVleiJ9.1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI",
            }
        }