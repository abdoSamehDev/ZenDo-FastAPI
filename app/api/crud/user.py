from sqlalchemy.orm import Session
from app.api.schemas.user import UserCreate, UserUpdate
from app.api.database.models.user import User
from app.utils.security import hash_password


def create_user(db: Session, user: UserCreate):
    new_user = User(**user.model_dump())
    new_user.password = hash_password(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    if user_update.password:
        user_update.password = hash_password(user_update.password)
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    # Commit the changes to the database
    db.commit()
    # Refresh the user object to reflect the changes in the database
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return user
