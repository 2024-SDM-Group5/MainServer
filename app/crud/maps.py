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

def update_map(db: Session, map_id: int, updates: dict) -> Map:
    map_obj = db.query(Map).filter(Map.map_id == map_id).first()
    if not map_obj:
        # 如果没有找到对象，抛出 HTTPException 或返回 None
        raise HTTPException(status_code=404, detail=f"Map with id {map_id} not found")
    
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
    if map_obj!=None:
        db.delete(map_obj)
        db.commit()
        return True
    return False

def get_maps_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Map]:
    return db.query(Map).filter(Map.author == user_id).offset(skip).limit(limit).all()
