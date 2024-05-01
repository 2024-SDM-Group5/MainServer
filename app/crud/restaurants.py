from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.dbModel import Restaurant, UserRestCollect, UserRestLike, UserRestDislike
from app.schemas.restaurants import CreateRestaurant
def get_restaurant(db: Session, place_id: str) -> Restaurant:
    return db.query(Restaurant).filter(Restaurant.google_place_id == place_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 10) -> list[Restaurant]:
    return db.query(Restaurant).offset(skip).limit(limit).all()

def bulk_insert(db: Session, restaurants: list[CreateRestaurant]) -> list[Restaurant]:
    db_restaurants = [{
        "google_place_id": restaurant.place_id,
        "rest_name": restaurant.name,
        "lat": restaurant.location['lat'],
        "lng": restaurant.location['lng'],
        "rating": restaurant.rating,
        "photo_url": restaurant.photo_url
    } for restaurant in restaurants]

    stmt = insert(Restaurant).values(db_restaurants)
    stmt = stmt.on_conflict_do_update(
        constraint="restaurants_pkey",
        set_= {
            "rest_name": stmt.excluded.rest_name,
            "lat": stmt.excluded.lat,
            "lng": stmt.excluded.lng,
            "rating": stmt.excluded.rating,
            "photo_url": stmt.excluded.photo_url
        }
    )
    db.execute(stmt)
    db.commit()
    return db_restaurants

def create_restaurant(db: Session, restaurant_data: CreateRestaurant) -> Restaurant:
    db_restaurant = Restaurant(
        google_place_id=restaurant_data.place_id,
        rest_name=restaurant_data.name,
        lat=restaurant_data.location.lat,
        lng=restaurant_data.location.lng,
        rating=restaurant_data.rating,
        photo_url=restaurant_data.photoUrl
    )
    existing_restaurant = db.query(Restaurant).filter(Restaurant.google_place_id == restaurant_data.placeId).first()
    if existing_restaurant:
        for key, value in restaurant_data.items():
            setattr(existing_restaurant, key, value)
        db_restaurant = existing_restaurant
    else:
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
    dislike_entry = UserRestDislike(user_id=user_id, rest_id=place_id)
    if dislike_entry:
        db.delete(dislike_entry)
    db.add(like_entry)
    db.commit()

def unlike_restaurant(db: Session, user_id: int, place_id: str):
    like_entry = db.query(UserRestLike).filter(UserRestLike.user_id == user_id, UserRestLike.rest_id == place_id).first()
    if like_entry:
        db.delete(like_entry)
        db.commit()

def dislike_restaurant(db: Session, user_id: int, place_id: str):
    dislike_entry = UserRestDislike(user_id=user_id, rest_id=place_id)
    like_entry = UserRestLike(user_id=user_id, rest_id=place_id)
    if like_entry:
        db.delete(like_entry)
    db.add(dislike_entry)
    db.commit()

def undislike_restaurant(db: Session, user_id: int, place_id: str):
    dislike_entry = db.query(UserRestDislike).filter(UserRestDislike.user_id == user_id, UserRestDislike.rest_id == place_id).first()
    if dislike_entry:
        db.delete(dislike_entry)
        db.commit()
