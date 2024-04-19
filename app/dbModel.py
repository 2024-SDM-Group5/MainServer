import sqlalchemy as _sql
from datetime import datetime
#import pytz
import api.database as _database  #import the database connect file

class User(_database.Base):
    __tablename__ = "users"
    user_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True, unique=True)
    follow = _sql.Column(_sql.Integer, index=True)
    followed = _sql.Column(_sql.Integer, index=True)
    avatar_url = _sql.Column(_sql.String, index=True)
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    map_id = _sql.Column(_sql.Integer, index=True)
    post_cnt = _sql.Column(_sql.Integer, index=True)

class Map(_database.Base):
    __tablename__ = "maps"
    map_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    map_name = _sql.Column(_sql.String, index=True)
    lat = _sql.Column(_sql.Integer, index=True)
    lng = _sql.Column(_sql.Integer, index=True)
    icon_url = _sql.Column(_sql.String, index=True)
    author = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"),nullable=False)
    tags =  _sql.Column(_sql.ARRAY(_sql.String), index=True)
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    rest_ids =  _sql.Column(_sql.ARRAY(_sql.String), index=True)
    
class Restaurant(_database.Base):
    __tablename__ = "restaurants"
    google_place_id = _sql.Column(_sql.String, primary_key=True, index=True)
    rest_name = _sql.Column(_sql.String, index=True)
    lat = _sql.Column(_sql.Integer, index=True)
    lng = _sql.Column(_sql.Integer, index=True)
    rating = _sql.Column(_sql.Integer, index=True)
    address = _sql.Column(_sql.String, index=True)
    telephone = _sql.Column(_sql.String, index=True)

class Comment(_database.Base):
    __tablename__ = "comments"
    comment_id = _sql.Column(_sql.String, primary_key=True, index=True)
    date = _sql.Column(_sql.String, index=True)
    items =  _sql.Column(_sql.ARRAY(_sql.String), index=True)
    author = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"),nullable=False)
    rest_id = _sql.Column(_sql.String, _sql.ForeignKey("restaurants.google_place_id"), nullable=False)
    content = _sql.Column(_sql.String, index=True)
    rating = _sql.Column(_sql.Integer, index=True)
    
class Diary(_database.Base):
    __tablename__ = "diaries"
    diary_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), nullable=False)
    rest_id = _sql.Column(_sql.String, _sql.ForeignKey("restaurants.google_place_id"), nullable=False)
    visit_date = _sql.Column(_sql.String, index=True)
    note = _sql.Column(_sql.String, index=True)
    image_url = _sql.Column(_sql.String, index=True)

class UserRest(_database.Base):
    __tablename__ = "user_rest"
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), primary_key=True, nullable=False)
    rest_id = _sql.Column(_sql.String, _sql.ForeignKey("restaurants.google_place_id"), primary_key=True, nullable=False)
    fav = _sql.Column(_sql.Boolean, default=False, index=True)
    view_cnt = _sql.Column(_sql.Integer, default=1, index=True)

class UserFollow(_database.Base):
    __tablename__ = "user_follow"
    follow_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    follow = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), nullable=False)
    be_followed = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), nullable=False)

class UserCollect(_database.Base):
    __tablename__ = "user_collect"
    collect_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), nullable=False)
    diary_id = _sql.Column(_sql.Integer, _sql.ForeignKey("diaries.diary_id"), nullable=False)


class UserMap(_database.Base):
    __tablename__ = "user_map"
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), primary_key=True, nullable=False)
    map_id = _sql.Column(_sql.Integer, _sql.ForeignKey("maps.map_id"), primary_key=True, nullable=False)
    fav = _sql.Column(_sql.Boolean, default=False, index=True)
    view_cnt = _sql.Column(_sql.Integer, default=1, index=True)

class Reply(_database.Base):
    __tablename__ = "replies"
    reply_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    diary_id = _sql.Column(_sql.Integer, _sql.ForeignKey("diaries.diary_id"), nullable=False)
    author = _sql.Column(_sql.Integer, _sql.ForeignKey("users.user_id"), nullable=False)
    content = _sql.Column(_sql.String, index=True)
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    