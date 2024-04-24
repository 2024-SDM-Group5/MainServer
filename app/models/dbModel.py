from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, ForeignKey
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    avatar_url = Column(String, index=True)
    created = Column(DateTime, default=datetime.now)
    map_id = Column(Integer, index=True)

class Map(Base):
    __tablename__ = "maps"
    map_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    map_name = Column(String, index=True)
    lat = Column(Integer, index=True)
    lng = Column(Integer, index=True)
    icon_url = Column(String, index=True)
    author = Column(Integer, ForeignKey("users.user_id"),nullable=False)
    tags =  Column(ARRAY(String), index=True)
    created = Column(DateTime, default=datetime.now)
    rest_ids =  Column(ARRAY(String), index=True)
    view_cnt = Column(Integer, default=0,index=True)
    
class Restaurant(Base):
    __tablename__ = "restaurants"
    google_place_id = Column(String, primary_key=True, index=True)
    rest_name = Column(String, index=True)
    lat = Column(Integer, index=True)
    lng = Column(Integer, index=True)
    rating = Column(Integer, index=True)
    address = Column(String, index=True)
    telephone = Column(String, index=True)
    view_cnt = Column(Integer, default=0, index=True)

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(String, primary_key=True, index=True, autoincrement=True)
    author = Column(Integer, ForeignKey("users.user_id"),nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), nullable=False)
    content = Column(String, index=True)
    
class Diary(Base):
    __tablename__ = "diaries"
    diary_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), nullable=False)
    created = Column(DateTime, default=datetime.now)
    content = Column(String, index=True)
    photos = Column(ARRAY(String), index=True)

class UserRestCollect(Base):
    __tablename__ = "user_rest_collect"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), primary_key=True, nullable=False)

class UserRestLike(Base):
    __tablename__ = "user_rest_like"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), primary_key=True, nullable=False)

class UserRestDislike(Base):
    __tablename__ = "user_rest_dislike"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), primary_key=True, nullable=False)

class UserRestRate(Base):
    __tablename__ = "user_rest_rate"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), primary_key=True, nullable=False)
    rating = Column(Integer, index=True)

class UserFollow(Base):
    __tablename__ = "user_follow"
    follow_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    follow = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    be_followed = Column(Integer, ForeignKey("users.user_id"), nullable=False)

class UserDiaryCollect(Base):
    __tablename__ = "user_diary_collect"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True,nullable=False)
    diary_id = Column(Integer, ForeignKey("diaries.diary_id"), primary_key=True,nullable=False)

class UserDiaryLike(Base):
    __tablename__ = "user_diary_like"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True,nullable=False)
    diary_id = Column(Integer, ForeignKey("diaries.diary_id"), primary_key=True,nullable=False)

class UserMapCollect(Base):
    __tablename__ = "user_map_collect"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    map_id = Column(Integer, ForeignKey("maps.map_id"), primary_key=True, nullable=False)

class Reply(Base):
    __tablename__ = "replies"
    reply_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey("diaries.diary_id"), nullable=False)
    author = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(String, index=True)
    created = Column(DateTime, default=datetime.now)
    