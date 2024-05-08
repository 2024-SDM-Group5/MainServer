from sqlalchemy.orm import Session, aliased
from sqlalchemy import desc, asc, select, func, select, distinct, exists
from app.models.dbModel import Diary, UserDiaryCollect, UserDiaryLike, Restaurant, UserFollow, User, Comment
from app.schemas.diaries import DiaryCreate, DiaryUpdate, SimplifiedDiary, DiaryDisplay, Reply
from typing import List
from fastapi import HTTPException

def simplified_query(
    auth_user_id: int = -1, 
    order_by: str = None, 
    following: bool = False, 
    q: str = None,
    author_id: int = None
):
    stmt = select(
        Diary.diary_id.label('id'),
        Restaurant.rest_name.label('restaurantName'),
        Diary.photos[1].label('imageUrl'),
    ).outerjoin(Restaurant, Restaurant.google_place_id == Diary.rest_id)

    if following:
        stmt = stmt.join(UserFollow, UserFollow.be_followed == Diary.user_id) \
        .where(UserFollow.follow == auth_user_id)
    
    if author_id:
        stmt = stmt.where(Diary.user_id == author_id)

    if order_by == "collectCount":
        stmt = stmt.outerjoin(UserDiaryCollect, UserDiaryCollect.diary_id == Diary.diary_id) \
            .order_by(func.count(distinct(UserDiaryCollect.user_id)).desc())
    elif order_by == "createTime":
        stmt = stmt.order_by(Diary.created.desc())

    if q:
        stmt = stmt.where(Restaurant.rest_name.like(f"%{q}%"))
    
    stmt = stmt.group_by(Diary.diary_id, Restaurant.rest_name)
    return stmt

def get_diaries(db: Session, user_id: int, query: dict) -> List[SimplifiedDiary]:
    stmt = simplified_query(
        auth_user_id=user_id, 
        order_by=query["orderBy"], 
        following=query["following"],
        q=query["q"]
    )
    result = db.execute(stmt).all()
    diaries = [SimplifiedDiary(**diary._asdict()) for diary in result]
    offset = query["offset"]
    limit = query["limit"]
    return len(diaries), diaries[offset:offset+limit]

def create_diary(db: Session, diary: DiaryCreate, user_id: int) -> Diary:
    if not diary.photos:
        raise HTTPException(status_code=400, detail="Diary must have at least one photo")
    db_diary = Diary(
        user_id=user_id,
        rest_id=diary.restaurantId,
        content=diary.content,
        items=diary.items,
        photos=diary.photos
    )
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary

def full_query(diary_id: int, auth_user_id: int):
    Favorites = aliased(UserDiaryLike)
    Collects = aliased(UserDiaryCollect)
    stmt = select(
        Diary.diary_id.label('id'),
        User.user_name.label('username'),
        Diary.user_id.label('userId'),
        Diary.rest_id.label('restaurantId'),
        Restaurant.rest_name.label('restaurantName'),
        User.avatar_url.label('avatarUrl'),
        Diary.photos,
        Diary.items,
        Diary.content,
        Diary.created.label('createdAt'),
        func.count(distinct(Favorites.user_id)).label('favCount'),
        func.count(distinct(Collects.user_id)).label('collectCount'),
        exists(
            select(1).where(
                UserDiaryCollect.user_id == auth_user_id, UserDiaryCollect.diary_id == Diary.diary_id
            )
        ).label('hasCollected'),
        exists(
            select(1).where(
                UserDiaryLike.user_id == auth_user_id, UserDiaryLike.diary_id == Diary.diary_id
            )
        ).label('hasFavorited')
    ).outerjoin(Collects, Collects.diary_id == Diary.diary_id) \
     .outerjoin(Favorites, Favorites.diary_id == Diary.diary_id) \
     .outerjoin(Restaurant, Restaurant.google_place_id == Diary.rest_id) \
     .outerjoin(User, User.user_id == Diary.user_id) \
     .group_by(Diary.diary_id, User.user_name, User.avatar_url, Restaurant.rest_name) \
     .where(Diary.diary_id == diary_id)
    return stmt

def get_replies_query(diary_id: int):
    stmt = select(
        Comment.comment_id.label('id'),
        Comment.author.label('authorId'),
        User.user_name.label('username'),
        User.avatar_url.label('avatarUrl'),
        Comment.content,
        Comment.created.label('createdAt')
    ).join(User, User.user_id == Comment.author) \
     .where(Comment.diary_id == diary_id)
    return stmt

def get_diary(db: Session, diary_id: int, auth_user_id: int) -> DiaryDisplay:
    stmt = full_query(diary_id, auth_user_id)
    result = db.execute(stmt).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Diary with id {diary_id} not found")
    replies_stmt = get_replies_query(diary_id)
    replies = db.execute(replies_stmt).all()
    replies = [Reply(**{**reply._asdict(), 'avatarUrl': reply.avatarUrl or ''}) for reply in replies]
    diary = DiaryDisplay(**{**result._asdict(), 'avatarUrl': result.avatarUrl or ''})
    diary.replies = replies
    return diary

def update_diary(db: Session, diary_id: int, user_id: int, updates: DiaryUpdate) -> Diary:
    diary = db.query(Diary).filter(Diary.diary_id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail=f"Diary with id {diary_id} not found")
    if diary.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this diary")
    upd_dict = {}
    if updates.photos:
        upd_dict["photos"] = updates.photos
    if updates.content:
        upd_dict["content"] = updates.content
    if updates.items:
        upd_dict["items"] = updates.items
    if diary:
        for key, value in upd_dict.items():
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
    collection = db.query(UserDiaryCollect).filter(UserDiaryCollect.user_id == user_id, UserDiaryCollect.diary_id == diary_id).first()
    if collection:
        return collection
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
    like = db.query(UserDiaryLike).filter(UserDiaryLike.user_id == user_id, UserDiaryLike.diary_id == diary_id).first()
    if like:
        return like
    like = UserDiaryLike(user_id=user_id, diary_id=diary_id)
    db.add(like)
    db.commit()
    return like

def unfavorite_diary(db: Session, user_id: int, diary_id: int):
    like = db.query(UserDiaryLike).filter(UserDiaryLike.user_id == user_id, UserDiaryLike.diary_id == diary_id).first()
    if like:
        db.delete(like)
        db.commit()