from sqlalchemy.orm import Session, aliased
from app.models.dbModel import User, UserFollow, Diary, Map
from sqlalchemy import func, select, exists, distinct
from app.schemas.users import UserDisplay
from app.schemas.diaries import SimplifiedDiary
from app.crud.diaries import simplified_query

def query_sql(user_id = None, auth_user_id: int = -1, name_match: str = None, order_by: str = None):
    Followings = aliased(UserFollow)
    Followers = aliased(UserFollow)

    stmt = select(
        User.user_id.label('id'),
        User.user_name.label('displayName'),
        User.avatar_url.label('avatarUrl'),
        Map.map_id.label('mapId'),
        func.count(distinct(Followings.be_followed)).label('following'),
        func.count(distinct(Followers.follow)).label('followed'),
        func.count(distinct(Diary.diary_id)).label('postCount'),
        exists(
            select(1).where(
                UserFollow.follow == auth_user_id, UserFollow.be_followed == User.user_id
            )
        ).label('isFollowing')
    ).outerjoin(Map, Map.author == User.user_id) \
    .outerjoin(Followings, Followings.be_followed == User.user_id) \
    .outerjoin(Followers, Followers.follow == User.user_id)  \
    .outerjoin(Diary, Diary.user_id == User.user_id)

    if user_id:
        stmt = stmt.where(User.user_id == user_id)

    if name_match:
        stmt = stmt.where(User.user_name.like(f"%{name_match}%"))
    
    stmt = stmt.group_by(User.user_id, Map.map_id)
    if order_by:
        if order_by == "following":
            stmt = stmt.order_by(func.count(distinct(Followings.be_followed)).desc())
        elif order_by == "createTime":
            stmt = stmt.order_by(User.created.desc())
    return stmt

def get_user(db: Session, user_id: int, auth_user_id: int) -> User:
    stmt = query_sql(user_id=user_id, auth_user_id=auth_user_id)
    result = db.execute(stmt).first()
    if result:
        return UserDisplay(**result._asdict())
    else:
        return None

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User:
    return db.query(User).filter(User.user_id == user_id).first()

def get_users(db: Session, query) -> list[User]:
    stmt = query_sql(auth_user_id=query["auth_user_id"], name_match=query["q"], order_by=query["orderBy"]).limit(query["limit"]).offset(query["offset"])
    result = db.execute(stmt).all()
    return [UserDisplay(**user._asdict()) for user in result]

def create_user(db: Session, user: dict) -> User:
    db_user = User(user_name=user['user_name'], email=user['email'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_map = Map(map_name="我的地圖", author=db_user.user_id, description="這裡收集了我喜愛的美食")
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_user

def update_user(db: Session, user_id: int, updates: dict) -> User:
    user = db.query(User).filter(User.user_id == user_id).first()
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

def get_user_diaries(db: Session, user_id: int):
    stmt = simplified_query(author_id=user_id, order_by="createTime")
    result = db.execute(stmt).all()
    diaries = [SimplifiedDiary(**diary._asdict()) for diary in result]
    return diaries