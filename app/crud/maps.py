from sqlalchemy.orm import Session
from app.models.dbModel import Map
from app.schemas.maps import (
    MapCreate, 
    SimplifiedMap, 
    CompleteMap, 
)
from sqlalchemy import func, select, and_, literal, distinct, exists, any_
from sqlalchemy.orm import Session, aliased
from app.models.dbModel import User, Restaurant, UserRestCollect, UserRestLike, UserRestDislike, UserMapCollect
from app.schemas.restaurants import SimplifiedRestaurant
from app.schemas.users import UserLoginInfo
from fastapi.exceptions import HTTPException

def query_sql(map_id = None, auth_user_id: int = -1, name_match: str = None, order_by: str = None):
    Collect = aliased(UserMapCollect)
    stmt = select(
        Map.map_id.label('id'),
        Map.map_name.label('name'),
        Map.icon_url.label('iconUrl'),
        User.user_name.label('author'),
        Map.author.label('authorId'),
        Map.view_cnt.label('viewCount'),
        Map.description,
        func.count(distinct(Collect.user_id)).label('collectCount'),
        exists(
            select(1).where(
                UserMapCollect.user_id == auth_user_id, UserMapCollect.map_id == Map.map_id
            )
        ).label('hasCollected'),
        func.json_build_object('lat', func.avg(Restaurant.lat), 'lng', func.avg(Restaurant.lng)).label('center')
    ).outerjoin(User, Map.author == User.user_id) \
    .outerjoin(Collect, Collect.map_id == Map.map_id) \
    .outerjoin(Restaurant, Restaurant.google_place_id == any_(Map.rest_ids))

    if map_id:
        stmt = stmt.where(Map.map_id == map_id)

    if name_match:
        stmt = stmt.where(User.user_name.like(f"%{name_match}%"))
    
    stmt = stmt.group_by(Map.map_id, User.user_name)
    if order_by:
        if order_by == "collectCount":
            stmt = stmt.order_by(func.count(distinct(Collect.user_id)).desc())
        elif order_by == "createTime":
            stmt = stmt.order_by(Map.created.desc())
    return stmt


def get_map(db: Session, map_id: int, auth_user_id: int) -> Map:
    stmt = query_sql(map_id=map_id, auth_user_id=auth_user_id)
    result = db.execute(stmt).first()
    restaurant = CompleteMap(
        **{k: v for k, v in result._asdict().items() 
            if k != 'iconUrl' or v is not None
        }
    )
    return restaurant

def get_maps(db: Session, query: dict) -> list[Map]:
    stmt = query_sql(auth_user_id=query["auth_user_id"], name_match=query["q"], order_by=query["orderBy"]).limit(query["limit"]).offset(query["offset"])
    result = db.execute(stmt).all()
    return [
        SimplifiedMap(
            **{k: v for k, v in map_._asdict().items() 
                if k != 'iconUrl' or v is not None
            }
        ) 
        for map_ in result
    ]

def create_map(db: Session, map_data: MapCreate, user: UserLoginInfo) -> Map:
    db_map = Map(
        map_name=map_data.name,
        icon_url=map_data.iconUrl,
        author=user.userId,  
        tags=map_data.tags,
        rest_ids=map_data.restaurants 
    )
    try:
        db.add(db_map)
        db.commit()
        db.refresh(db_map)
        return db_map.map_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create map{e}")

def update_map(db: Session, map_id: int, updates: dict, user_id: int) -> Map:
    map_obj = db.query(Map).filter(Map.map_id == map_id).first()
    if not map_obj:
        raise HTTPException(status_code=404, detail=f"Map with id {map_id} not found")
    if map_obj.author != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this map")
    for key, value in updates.items():
        if hasattr(map_obj, key):
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

def base_query(auth_user_id: int, map_id: int, order_by: str = None):
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
    
    if order_by:
        if order_by == "rating":
            stmt = stmt.order_by(Restaurant.rating.desc())
        elif order_by == "name":
            stmt = stmt.order_by(Restaurant.rest_name)
        elif order_by == "collectCount":
            stmt = stmt.order_by(func.count(distinct(Collects.user_id)).desc())

    
    return stmt

def get_restaurants(db: Session, map_id: int, query_params: dict):
    order_by = query_params.get("orderBy")
    q = query_params.get("q")
    auth_user_id = query_params.get("auth_user_id", -1)
    stmt = base_query(auth_user_id, map_id, order_by)

    if q:
        stmt = stmt.where(Restaurant.rest_name.like(f"%{q}%"))

    results = db.execute(stmt).all()
    count = len(results)
    restaurants = [SimplifiedRestaurant(**result._asdict()) for result in results]
    return count, restaurants

def collect_map(db: Session, user_id: int, map_id: int):
    collection_entry = UserMapCollect(user_id=user_id, map_id=map_id)
    db.add(collection_entry)
    db.commit()

def uncollect_map(db: Session, user_id: int, map_id: str):
    collection_entry = db.query(UserMapCollect).filter(UserMapCollect.user_id == user_id, UserMapCollect.map_id == map_id).first()
    if collection_entry:
        db.delete(collection_entry)
        db.commit()
