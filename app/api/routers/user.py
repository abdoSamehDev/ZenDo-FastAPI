from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.api.crud.user import create_user, get_user_by_email
from app.utils import security
from app.api.schemas.user import UserCreate, UserLogin, User
from app.api.database.db import get_db

router = APIRouter()


@router.post("/register/", response_model=User)
async def user_register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user=user)


@router.post("/login/", response_model=User)
async def user_login(
    user: UserLogin, db: Session = Depends(get_db), request: Request = None
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user and security.verify_password(user.password, db_user.password):
        request.session["user_id"] = db_user.id
        return db_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )
