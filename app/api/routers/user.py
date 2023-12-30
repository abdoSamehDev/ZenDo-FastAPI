from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.api.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    update_user,
    delete_user,
)
from app.utils import security
from app.api.schemas.user import UserCreate, UserLogin, UserUpdate, User
from app.api.database.db import get_db

router = APIRouter()


@router.post("/register/", response_model=User)
async def user_register(
    user: UserCreate, db: Session = Depends(get_db), request: Request = None
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user = create_user(db=db, user=user)
    request.session["user_id"] = new_user.id
    return new_user


@router.post("/login/", response_model=User)
async def user_login(
    user: UserLogin, db: Session = Depends(get_db), request: Request = None
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user and security.verify_password(user.password, db_user.password):
        request.session["user_id"] = db_user.id
        user_id = request.session.get("user_id")
        print("User ID in logging in: ", str(user_id))
        print("User ID type in logging in: ", type(user_id))
        return db_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


@router.get("/profile", response_model=User)
async def user_profile(db: Session = Depends(get_db), request: Request = None):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/logout")
async def user_logout(request: Request):
    user_id = request.session.get("user_id")
    print("User ID in logging out: ", str(user_id))
    if user_id is not None:
        del request.session["user_id"]
        return {"message": "User logged out successfully"}
    raise HTTPException(
        status_code=401,
        detail="User not authenticated",
    )
    # user_id = request.session.get("user_id")
    # print("User ID in logging out: ", str(user_id))
    # print("User ID type in logging out: ", type(user_id))
    # return {"message": "User logged out successfully"}


@router.put("/update", response_model=User)
async def user_update(
    user_update: UserUpdate, db: Session = Depends(get_db), request: Request = None
):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    updated_user = update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/delete")
async def user_delete(db: Session = Depends(get_db), request: Request = None):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
