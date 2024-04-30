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
from app.schemas.users import UserLoginInfo

def get_map(db: Session, map_id: int) -> Map:
    return db.query(Map).filter(Map.map_id == map_id).first()

def get_maps(db: Session, skip: int = 0, limit: int = 100) -> list[Map]:
    return db.query(Map).offset(skip).limit(limit).all()

def create_map(db: Session, map_data: MapCreate, user: UserLoginInfo) -> Map:
    db_map = Map(
        map_name=map_data.map_name,
        lat=map_data.lat,
        lng=map_data.lng,
        icon_url=map_data.icon_url,
        author=user.userId,  
        tags=map_data.tags,
        rest_ids=map_data.rest_ids 
    )
    try:
        db.add(db_map)
        db.commit()
        db.refresh(db_map)
        return db_map.map_id
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create map")

def update_map(db: Session, map_id: int, updates: dict) -> Map:
    map_obj = db.query(Map).filter(Map.map_id == map_id).first()
    if map_obj:
        for key, value in updates.items():
            setattr(map_obj, key, value)
        db.commit()
        db.refresh(map_obj)
    return map_obj

def delete_map(db: Session, map_id: int):
    map_obj = db.query(Map).filter(Map.map_id == map_id).first()
    if map_obj:
        db.delete(map_obj)
        db.commit()

def get_maps_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Map]:
    return db.query(Map).filter(Map.author == user_id).offset(skip).limit(limit).all()
