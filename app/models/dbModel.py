from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, ForeignKey
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    follow = Column(Integer, index=True)
    followed = Column(Integer, index=True)
    avatar_url = Column(String, index=True)
    created = Column(DateTime, default=datetime.now)
    map_id = Column(Integer, index=True)
    post_cnt = Column(Integer, index=True)

class Map(Base):
    __tablename__ = "maps"
    map_id = Column(Integer, primary_key=True, index=True)
    map_name = Column(String, index=True)
    lat = Column(Integer, index=True)
    lng = Column(Integer, index=True)
    icon_url = Column(String, index=True)
    author = Column(Integer, ForeignKey("users.user_id"),nullable=False)
    tags =  Column(ARRAY(String), index=True)
    created = Column(DateTime, default=datetime.now)
    rest_ids =  Column(ARRAY(String), index=True)
    
class Restaurant(Base):
    __tablename__ = "restaurants"
    google_place_id = Column(String, primary_key=True, index=True)
    rest_name = Column(String, index=True)
    lat = Column(Integer, index=True)
    lng = Column(Integer, index=True)
    rating = Column(Integer, index=True)
    address = Column(String, index=True)
    telephone = Column(String, index=True)

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(String, primary_key=True, index=True)
    date = Column(String, index=True)
    items =  Column(ARRAY(String), index=True)
    author = Column(Integer, ForeignKey("users.user_id"),nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), nullable=False)
    content = Column(String, index=True)
    rating = Column(Integer, index=True)
    
class Diary(Base):
    __tablename__ = "diaries"
    diary_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), nullable=False)
    visit_date = Column(String, index=True)
    note = Column(String, index=True)
    image_url = Column(String, index=True)

class UserRest(Base):
    __tablename__ = "user_rest"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    rest_id = Column(String, ForeignKey("restaurants.google_place_id"), primary_key=True, nullable=False)
    fav = Column(Boolean, default=False, index=True)
    view_cnt = Column(Integer, default=1, index=True)

class UserFollow(Base):
    __tablename__ = "user_follow"
    follow_id = Column(Integer, primary_key=True, index=True)
    follow = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    be_followed = Column(Integer, ForeignKey("users.user_id"), nullable=False)

class UserCollect(Base):
    __tablename__ = "user_collect"
    collect_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    diary_id = Column(Integer, ForeignKey("diaries.diary_id"), nullable=False)


class UserMap(Base):
    __tablename__ = "user_map"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    map_id = Column(Integer, ForeignKey("maps.map_id"), primary_key=True, nullable=False)
    fav = Column(Boolean, default=False, index=True)
    view_cnt = Column(Integer, default=1, index=True)

class Reply(Base):
    __tablename__ = "replies"
    reply_id = Column(Integer, primary_key=True, index=True)
    diary_id = Column(Integer, ForeignKey("diaries.diary_id"), nullable=False)
    author = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(String, index=True)
    created = Column(DateTime, default=datetime.now)
    