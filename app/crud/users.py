from sqlalchemy.orm import Session, aliased
from app.models.dbModel import User, UserFollow, Diary, Map
from sqlalchemy import func, select, exists, distinct
from app.schemas.users import UserDisplay

def query_sql(user_id = None, auth_user_id: int = -1):
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
    stmt = stmt.group_by(User.user_id, Map.map_id)
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

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = query_sql().limit(limit).offset(skip)
    result = db.execute(stmt).all()
    return [UserDisplay(**user._asdict()) for user in result]

def create_user(db: Session, user: dict) -> User:
    db_user = User(user_name=user['user_name'], email=user['email'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
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
