from sqlalchemy.orm import Session
from app.models.dbModel import Restaurant, UserRestCollect, UserRestLike, UserRestDislike

def get_restaurant(db: Session, place_id: str) -> Restaurant:
    return db.query(Restaurant).filter(Restaurant.google_place_id == place_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 10) -> list[Restaurant]:
    return db.query(Restaurant).offset(skip).limit(limit).all()

def create_restaurant(db: Session, restaurant_data: dict) -> Restaurant:
    db_restaurant = Restaurant(**restaurant_data)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def update_restaurant(db: Session, place_id: str, updates: dict) -> Restaurant:
    restaurant = db.query(Restaurant).filter(Restaurant.google_place_id == place_id).first()
    if restaurant:
        for key, value in updates.items():
            setattr(restaurant, key, value)
        db.commit()
        db.refresh(restaurant)
    return restaurant

def delete_restaurant(db: Session, place_id: str):
    restaurant = db.query(Restaurant).filter(Restaurant.google_place_id == place_id).first()
    if restaurant:
        db.delete(restaurant)
        db.commit()

def collect_restaurant(db: Session, user_id: int, place_id: str):
    collection_entry = UserRestCollect(user_id=user_id, rest_id=place_id)
    db.add(collection_entry)
    db.commit()

def uncollect_restaurant(db: Session, user_id: int, place_id: str):
    collection_entry = db.query(UserRestCollect).filter(UserRestCollect.user_id == user_id, UserRestCollect.rest_id == place_id).first()
    if collection_entry:
        db.delete(collection_entry)
        db.commit()

def like_restaurant(db: Session, user_id: int, place_id: str):
    like_entry = UserRestLike(user_id=user_id, rest_id=place_id)
    db.add(like_entry)
    db.commit()

def unlike_restaurant(db: Session, user_id: int, place_id: str):
    like_entry = db.query(UserRestLike).filter(UserRestLike.user_id == user_id, UserRestLike.rest_id == place_id).first()
    if like_entry:
        db.delete(like_entry)
        db.commit()

def dislike_restaurant(db: Session, user_id: int, place_id: str):
    dislike_entry = UserRestDislike(user_id=user_id, rest_id=place_id)
    db.add(dislike_entry)
    db.commit()

def undislike_restaurant(db: Session, user_id: int, place_id: str):
    dislike_entry = db.query(UserRestDislike).filter(UserRestDislike.user_id == user_id, UserRestDislike.rest_id == place_id).first()
    if dislike_entry:
        db.delete(dislike_entry)
        db.commit()
