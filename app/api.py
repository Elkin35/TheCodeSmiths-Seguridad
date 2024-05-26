import time
from fastapi import FastAPI, Body, Depends
from fastapi.responses import JSONResponse
from http.client import HTTPResponse
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt, decode_jwt
from app.schemas import PostSchema, UserSchema, UserLoginSchema

from sqlalchemy.orm import Session

import hashlib

from . import models

from app.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]


app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }
        

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }

# ----------------- importante corregir create_user, check_user (hashing) ---------------------------------

def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def hash_password(password: str):
    password = password.encode("utf-8")
    hash_object = hashlib.sha256(password)
    hex_dig = hash_object.hexdigest()
    return hex_dig


@app.post("/user/signup", response_model = dict,  tags=["user"])
async def create_user(user: UserSchema = Body(...), db: Session = Depends(get_db)):

    if check_user(user, db):
        return JSONResponse(status_code=400, content={"error": "User already exists!"})

    hashed_password = hash_password(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        country=user.country,
        city=user.city,
        phone=user.phone,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return JSONResponse(status_code=201, content={"data": "User created."})

def check_user(data: UserLoginSchema, db: Session):
    usuario = get_user_by_email(data.email, db)
    password_data = hash_password(data.password)
    if usuario:
        if usuario.password == password_data:
            return True
    return False


@app.post("/user/login", response_model=None , tags=["user"])
async def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    if check_user(user, db):
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }


@app.get("/user/is_authenticated", tags=["user"])
async def is_authenticated(token: str, db: Session = Depends(get_db)):
    email = decode_jwt(token)

    tokens_usados = db.query(models.UsedAccessToken).all()
    token_modelo_usado = False

    for token_usado in tokens_usados:
        if token == token_usado.token:
            token_modelo_usado = True


    if email and not token_modelo_usado:
        return {
            "data": "User is authenticated."
        }
    return {
        "error": "User is not authenticated."
    }


@app.get("/user/info", tags=["user"])
async def user_info(token: str, db: Session = Depends(get_db)):
    email = decode_jwt(token)['user_id']

    if email:
        return {
            "data": get_user_by_email(email, db)
        }
    return {
        "error": "User is not authenticated."
    }


@app.get("/user/logout", tags=["user"])
async def user_logout(token: str, db: Session = Depends(get_db)):

    # Agregar el token a la base de datos de tokens usados
    token_model = models.UsedAccessToken(token=token)
    db.add(token_model)
    db.commit()
    db.refresh(token_model)
    return {
        "data": "User has been logged out."
    }
@app.get("/health-check", tags=["root"])
def health_check():

    return HTTPResponse(status=200, body="OK")
