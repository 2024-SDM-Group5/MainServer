from sqlalchemy.orm import Session
from app.models.dbModel import Map
from app.schemas.maps import (
    MapCreate, 
    MapUpdate, 
    CompleteMap, 
    PostResponse,
    PutResponse, 
    PaginatedMapResponse,
    SimplifiedMaps_Ex,
    CompleteMap_Ex
)
from sqlalchemy import func, select, and_, literal, distinct, exists, any_
from sqlalchemy.orm import Session, aliased
from app.models.dbModel import Restaurant, UserRestCollect, UserRestLike, UserRestDislike
from app.schemas.restaurants import CreateRestaurant, SimplifiedRestaurant, FullCreateRestaurant, Restaurant as ClientRestaurant
from app.schemas.users import UserLoginInfo
from fastapi.exceptions import HTTPException

def get_map(db: Session, map_id: int) -> Map:
    return db.query(Map).filter(Map.map_id == map_id).first()

def get_maps(db: Session, skip: int = 0, limit: int = 100) -> list[Map]:
    return db.query(Map).offset(skip).limit(limit).all()

def create_map(db: Session, map_data: MapCreate, user: UserLoginInfo) -> Map:
    db_map = Map(
        map_name=map_data.map_name,
        lat=map_data.lat,
        lng=map_data.lng,
        icon_url=str(map_data.icon_url),
        author=user.userId,  
        tags=map_data.tags,
        rest_ids=map_data.rest_ids 
    )
    try:
        db.add(db_map)
        db.commit()
        db.refresh(db_map)
        return db_map.map_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create map{e}")

def update_map(db: Session, map_id: int, updates: dict, user_id: int) -> Map:
    map_obj = db.query(Map).filter(Map.map_id == map_id).first()
    if not map_obj:
        raise HTTPException(status_code=404, detail=f"Map with id {map_id} not found")
    if map_obj.author != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this map")
    for key, value in updates.items():
        if hasattr(map_obj, key):
            if key == "icon_url":
                setattr(map_obj, key, str(value))
            else:
                setattr(map_obj, key, value)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid key {key}")
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update Map due to: {str(e)}")
        
    db.refresh(map_obj)

    return map_obj

def delete_map(db: Session, map_id: int):
    map_obj = db.query(Map).filter(Map.map_id == map_id).first()
    if map_obj != None:
        db.delete(map_obj)
        db.commit()
        return True
    return False

def get_maps_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Map]:
    return db.query(Map).filter(Map.author == user_id).offset(skip).limit(limit).all()

def base_query(auth_user_id: int, map_id: int):
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
    ).select_from(
        Restaurant
    ).join(
        Map, Map.map_id == map_id
    ).where(
        Restaurant.google_place_id == any_(Map.rest_ids)  # Using the ANY function to filter by rest_ids array
    ).outerjoin(Collects, Collects.rest_id == Restaurant.google_place_id) \
     .outerjoin(Likes, Likes.rest_id == Restaurant.google_place_id) \
     .outerjoin(Dislikes, Dislikes.rest_id == Restaurant.google_place_id) \
     .group_by(Restaurant.google_place_id)
    
    return stmt

def get_restaurants(db: Session, map_id: int, query_params: dict):
    order_by = query_params.get("orderBy")
    offset = query_params.get("offset", 0)
    limit = query_params.get("limit", 10)
    q = query_params.get("q")
    auth_user_id = query_params.get("auth_user_id", -1)
    stmt = base_query(auth_user_id, map_id)

    if q:
        stmt = stmt.where(Restaurant.rest_name.like(f"%{q}%"))
    # Ordering
    if order_by:
        if order_by == "rating":
            stmt = stmt.order_by(Restaurant.rating.desc())
        elif order_by == "name":
            stmt = stmt.order_by(Restaurant.rest_name)

    stmt = stmt.offset(offset).limit(limit)
    results = db.execute(stmt).all()
    count = len(results)
    restaurants = [SimplifiedRestaurant(**result._asdict()) for result in results]
    return count, restaurants
