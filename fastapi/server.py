from fastapi import FastAPI, status, Depends, HTTPException
from sqlmodel import create_engine, SQLModel, Field, select, Session
import bcrypt
from typing import List
from sqlalchemy.orm import load_only
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
import jwt



engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})

def hash(pwd: str) -> str:
    pwd_bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def get_db():
    with Session(engine) as session:
        yield session

class UserBase(SQLModel):
    email: str = Field(primary_key=True, index=True)

class UserRegister(UserBase):
    password: str

class User(UserBase, table=True):
    __tablename__ = "user"
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=3600)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "SECRET", algorithm="HS256")

app = FastAPI(lifespan=lifespan)

@app.get("/user", response_model=List[UserBase], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    statement = select(User).options(load_only(User.email))
    users = db.exec(statement).all()
    return users

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.exec(statement).first()
    print(user_data.password)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username exists"
        )

    new_user = User(
        email=user_data.email,
        password=hash(user_data.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "jwt": create_access_token(data={"sub": new_user.email})
    }