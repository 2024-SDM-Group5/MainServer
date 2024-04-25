from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.dbModel import Diary, UserDiaryCollect, UserDiaryLike
from typing import List

def get_diaries(db: Session, skip: int = 0, limit: int = 100, order_by: str = "created", reverse: bool = False) -> List[Diary]:
    if order_by == "collectCount":
        order_column = Diary.collect_count
    else:
        order_column = Diary.created

    if reverse:
        order_column = desc(order_column)
    else:
        order_column = asc(order_column)

    return db.query(Diary).order_by(order_column).offset(skip).limit(limit).all()

def create_diary(db: Session, diary_data: dict) -> Diary:
    db_diary = Diary(
        title=diary_data['title'],
        avatar_url=diary_data['avatar_url'],
        user_id=diary_data['user_id'],
        rest_id=diary_data['rest_id'],
        content=diary_data['content'],
        photos=diary_data['photos']
    )
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary

def get_diary(db: Session, diary_id: int) -> Diary:
    return db.query(Diary).filter(Diary.diary_id == diary_id).first()

def update_diary(db: Session, diary_id: int, updates: dict) -> Diary:
    diary = db.query(Diary).filter(Diary.diary_id == diary_id).first()
    if diary:
        for key, value in updates.items():
            setattr(diary, key, value)
        db.commit()
        db.refresh(diary)
    return diary

def delete_diary(db: Session, diary_id: int):
    diary = db.query(Diary).filter(Diary.diary_id == diary_id).first()
    if diary:
        db.delete(diary)
        db.commit()

def collect_diary(db: Session, user_id: int, diary_id: int) -> UserDiaryCollect:
    collection = UserDiaryCollect(user_id=user_id, diary_id=diary_id)
    db.add(collection)
    db.commit()
    return collection

def uncollect_diary(db: Session, user_id: int, diary_id: int):
    collection = db.query(UserDiaryCollect).filter(UserDiaryCollect.user_id == user_id, UserDiaryCollect.diary_id == diary_id).first()
    if collection:
        db.delete(collection)
        db.commit()

def favorite_diary(db: Session, user_id: int, diary_id: int) -> UserDiaryLike:
    like = UserDiaryLike(user_id=user_id, diary_id=diary_id)
    db.add(like)
    db.commit()
    return like

def unfavorite_diary(db: Session, user_id: int, diary_id: int):
    like = db.query(UserDiaryLike).filter(UserDiaryLike.user_id == user_id, UserDiaryLike.diary_id == diary_id).first()
    if like:
        db.delete(like)
        db.commit()