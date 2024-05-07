from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.dbModel import Restaurant, UserRestCollect, UserRestLike, UserRestDislike, Map, Diary
from app.schemas.restaurants import CreateRestaurant, SimplifiedRestaurant, FullCreateRestaurant, Restaurant as ClientRestaurant
from app.schemas.diaries import SimplifiedDiary
from sqlalchemy import func, select, and_, literal, distinct, exists
from sqlalchemy.orm import Session, aliased

def base_query(auth_user_id: int, order_by: str = None):
    Collects = aliased(UserRestCollect)
    Likes = aliased(UserRestLike)
    Dislikes = aliased(UserRestDislike)
    stmt = select(
        Restaurant.rest_name.label('name'),
        func.json_build_object('lat', Restaurant.lat, 'lng', Restaurant.lng).label('location'),
        Restaurant.telephone,
        Restaurant.address,
        Restaurant.rating,
        Restaurant.google_place_id.label('placeId'),
        Restaurant.photo_url.label('photoUrl'),
        literal(0).label('viewCount'), 
        func.count(distinct(Collects.user_id)).label('collectCount'),
        func.count(distinct(Likes.user_id)).label('likeCount'),
        func.count(distinct(Dislikes.user_id)).label('dislikeCount'),
        exists(
            select(1).where(
                UserRestCollect.user_id == auth_user_id, UserRestCollect.rest_id == Restaurant.google_place_id
            )
        ).label('hasCollected'),
        exists(select(1).where(and_(UserRestLike.user_id == auth_user_id, UserRestLike.rest_id == Restaurant.google_place_id))).label('hasLiked'),
        exists(select(1).where(and_(UserRestDislike.user_id == auth_user_id, UserRestDislike.rest_id == Restaurant.google_place_id))).label('hasDisliked')
    ).outerjoin(Collects, Collects.rest_id == Restaurant.google_place_id) \
     .outerjoin(Likes, Likes.rest_id == Restaurant.google_place_id) \
     .outerjoin(Dislikes, Dislikes.rest_id == Restaurant.google_place_id) \
     .group_by(Restaurant.google_place_id)
    

    if order_by:
        if order_by == "rating":
            stmt = stmt.order_by(Restaurant.rating.desc())
        elif order_by == "name":
            stmt = stmt.order_by(Restaurant.rest_name)
        elif order_by == "collectCount":
            stmt = stmt.order_by(func.count(distinct(Collects.user_id)).desc())

    return stmt

def query_restaurants(session: Session, query_params: dict):
    order_by = query_params.get("orderBy")
    offset = query_params.get("offset", 0)
    limit = query_params.get("limit", 10)
    q = query_params.get("q")
    auth_user_id = query_params.get("auth_user_id", -1)
    sw_lat = query_params.get("sw_lat")
    sw_lng = query_params.get("sw_lng")
    ne_lat = query_params.get("ne_lat")
    ne_lng = query_params.get("ne_lng")

    stmt = base_query(auth_user_id, order_by)

    if sw_lat and sw_lng and ne_lat and ne_lng:
        stmt = stmt.where(
            and_(
                Restaurant.lat.between(sw_lat, ne_lat),
                Restaurant.lng.between(sw_lng, ne_lng)
            )
        )

    if q:
        stmt = stmt.where(Restaurant.rest_name.like(f"%{q}%"))
    # Ordering

    # Pagination
    stmt = stmt.offset(offset).limit(limit)
    count_query = select(func.count(Restaurant.google_place_id))
    if sw_lat and sw_lng and ne_lat and ne_lng:
        count_query = count_query.where(
            and_(
                Restaurant.lat.between(sw_lat, ne_lat),
                Restaurant.lng.between(sw_lng, ne_lng)
            )    
        )
    count = session.execute(count_query).scalar()
    results = session.execute(stmt).all()
    restaurants = [SimplifiedRestaurant(**result._asdict()) for result in results]

    return count, restaurants

def get_restaurant(db: Session, place_id: str, user_id: int) -> Restaurant:
    stmt = base_query(user_id)
    stmt = stmt.where(Restaurant.google_place_id == place_id)
    result = db.execute(stmt).first()
    restaurant = ClientRestaurant(**result._asdict(), diaries=[])
    
    diary_stmt = select(
        Diary.diary_id.label('id'),
        Restaurant.rest_name.label('restaurantName'),
        Diary.photos[1].label('imageUrl'),
    ).outerjoin(Restaurant, Restaurant.google_place_id == Diary.rest_id) \
    .where(Diary.rest_id == place_id)
    diaries = db.execute(diary_stmt).all()
    restaurant.diaries = [SimplifiedDiary(**diary._asdict()) for diary in diaries]
    return restaurant

def bulk_insert(db: Session, restaurants: list[CreateRestaurant]) -> list[Restaurant]:
    if not restaurants:
        return []
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

def create_update_restaurant(db: Session, restaurant: FullCreateRestaurant) -> Restaurant:
    existing_restaurant = db.query(Restaurant).filter(Restaurant.google_place_id == restaurant.place_id).first()
    if existing_restaurant:
        updates = {
            "rest_name": restaurant.name,
            "address": restaurant.address,
            "lat": restaurant.location.get('lat', 0),
            "lng": restaurant.location.get('lng', 0),
            "telephone": restaurant.telephone,
            "rating": restaurant.rating,
            "photo_url": restaurant.photo_url
        }
        for key, value in updates.items():
            setattr(existing_restaurant, key, value)
        db_restaurant = existing_restaurant
    else:
        db_restaurant = Restaurant(
            rest_name=restaurant.name,
            address=restaurant.address,
            google_place_id=restaurant.place_id,
            lat=restaurant.location.get('lat', 0),
            lng=restaurant.location.get('lng', 0),
            telephone=restaurant.telephone,
            rating=restaurant.rating,
            photo_url=restaurant.photo_url
        )
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
    collection_entry = db.query(UserRestCollect).filter(UserRestCollect.user_id == user_id, UserRestCollect.rest_id == place_id).first()
    if not collection_entry:
        collection_entry = UserRestCollect(user_id=user_id, rest_id=place_id)
        db.add(collection_entry)
        db.commit()
    
    map = db.query(Map).filter(Map.author == user_id).first()
    if map:
        restaurants = map.rest_ids.copy()
        if place_id not in restaurants:
            restaurants.append(place_id)
            setattr(map, "rest_ids", restaurants)
            db.commit()
            db.refresh(map)
    return collection_entry

def uncollect_restaurant(db: Session, user_id: int, place_id: str):
    collection_entry = db.query(UserRestCollect).filter(UserRestCollect.user_id == user_id, UserRestCollect.rest_id == place_id).first()
    if collection_entry:
        db.delete(collection_entry)
        db.commit()
    map = db.query(Map).filter(Map.author == user_id).first()
    if map:
        restaurants = map.rest_ids.copy()
        if place_id in restaurants:
            restaurants.remove(place_id)
            setattr(map, "rest_ids", restaurants)
            db.commit()
            db.refresh(map)

def like_restaurant(db: Session, user_id: int, place_id: str):
    existing_dislike = db.query(UserRestDislike).filter_by(user_id=user_id, rest_id=place_id).first()
    if existing_dislike:
        db.delete(existing_dislike)
    existing_like = db.query(UserRestLike).filter_by(user_id=user_id, rest_id=place_id).first()
    if not existing_like:
        like_entry = UserRestLike(user_id=user_id, rest_id=place_id)
        db.add(like_entry)
    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback in case of any error
        raise Exception(f"Failed to like the restaurant: {e}")
    return f"Restaurant {place_id} liked successfully!"


def unlike_restaurant(db: Session, user_id: int, place_id: str):
    like_entry = db.query(UserRestLike).filter(UserRestLike.user_id == user_id, UserRestLike.rest_id == place_id).first()
    if like_entry:
        db.delete(like_entry)
        db.commit()

def dislike_restaurant(db: Session, user_id: int, place_id: str):
    existing_like = db.query(UserRestLike).filter_by(user_id=user_id, rest_id=place_id).first()
    if existing_like:
        db.delete(existing_like)
    existing_dislike = db.query(UserRestDislike).filter_by(user_id=user_id, rest_id=place_id).first()
    if not existing_dislike:
        dislike_entry = UserRestDislike(user_id=user_id, rest_id=place_id)
        db.add(dislike_entry)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to dislike the restaurant: {e}")
    return f"Restaurant {place_id} disliked successfully!"

def undislike_restaurant(db: Session, user_id: int, place_id: str):
    dislike_entry = db.query(UserRestDislike).filter(UserRestDislike.user_id == user_id, UserRestDislike.rest_id == place_id).first()
    if dislike_entry:
        db.delete(dislike_entry)
        db.commit()
