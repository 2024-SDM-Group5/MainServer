from sqlalchemy.orm import Session
from app.models.dbModel import UserFollow

def create_follow(db: Session, follower: int, followee: int) -> UserFollow:
    db_follow = db.query(UserFollow).filter(UserFollow.follow == follower, UserFollow.be_followed == followee).first()
    if db_follow:
        return db_follow
    db_follow = UserFollow(follow=follower, be_followed=followee)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

def delete_follow(db: Session, follower: int, followee: int) -> UserFollow:
    db_follow = db.query(UserFollow).filter(UserFollow.follow == follower, UserFollow.be_followed == followee).first()
    if db_follow:
        db.delete(db_follow)
        db.commit()
    return db_follow 
