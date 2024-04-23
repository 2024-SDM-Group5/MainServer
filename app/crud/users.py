from sqlalchemy.orm import Session
from app.models.dbModel import User

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: dict) -> User:
    print(user)
    db_user = User(user_name=user['user_name'], email=user['email'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, updates: dict) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in updates.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
