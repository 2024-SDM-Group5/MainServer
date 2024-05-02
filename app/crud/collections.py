from sqlalchemy.orm import Session
from operator import itemgetter
import statistics
from app.models.dbModel import User, Map, Restaurant, Diary, UserMapCollect, UserRestCollect, UserRestLike, UserRestDislike, UserRestRate, UserDiaryCollect
from app.schemas.maps import SimplifiedMap
from app.schemas.diaries import SimplifiedDiary
from app.schemas.restaurants import SimplifiedRestaurant

def get_user_map(db:Session, user_id:int, orderBy:str, offset:int, limit:int, q: str) -> list[SimplifiedMap]:
    maps = db.query(UserMapCollect).filter(UserMapCollect.user_id == user_id).all()
    map_ids = list(map(lambda x: x.map_id, maps))
    query = db.query(Map).filter(Map.map_id.in_(map_ids))
    if q != "":
        query = query.filter(Map.map_name.ilike(f"%{q}%"))
    if orderBy == "created":
        query = query.order_by(Map.created.desc())
    query = query.offset(offset).limit(limit)
    map_collections = query.all()
    simplified_maps = [
        SimplifiedMap(
            id=map_instance.map_id,
            name=map_instance.map_name,
            iconUrl=map_instance.icon_url,
            author=db.query(User).filter(User.user_id == map_instance.author).first().user_name,
            authorId=map_instance.author,
            viewCount=map_instance.view_cnt,
            collectCount=db.query(UserMapCollect).filter(UserMapCollect.map_id == map_instance.map_id).count(),
            hasCollected=True,
            center={"lat": map_instance.lat, "lng": map_instance.lng}
        )
        for map_instance in map_collections
    ]
    if orderBy == "collect_cnt":
        simplified_maps = sorted(simplified_maps, key=itemgetter('collectCount'), reverse=True)
    
    return simplified_maps

def get_user_rest(db:Session, user_id:int, orderBy:str, offset:int, limit:int, q: str) -> list[SimplifiedRestaurant]:
    rests = db.query(UserRestCollect).filter(UserRestCollect.user_id == user_id).all()
    rest_ids = list(map(lambda x: x.rest_id, rests))
    query = db.query(Restaurant).filter(Restaurant.google_place_id.in_(rest_ids))
    if q != "":
        query = query.filter(Restaurant.rest_name.ilike(f"%{q}%"))
    if orderBy == "created":
        query = query.order_by(Restaurant.created.desc())
    query = query.offset(offset).limit(limit)
    rest_collections = query.all()
    simplified_rests = [
        SimplifiedRestaurant(
            name=rest_instance.rest_name,
            address=rest_instance.address,
            location={"lat": rest_instance.lat, "lng": rest_instance.lng},
            telephone=rest_instance.telephone,
            rating=rest_instance.rating,
            placeId=rest_instance.google_place_id,
            viewCount=rest_instance.view_cnt,
            collectCount=db.query(UserRestCollect).filter(UserRestCollect.rest_id == rest_instance.google_place_id).count(),
            likeCount=db.query(UserRestLike).filter(UserRestLike.rest_id == rest_instance.google_place_id).count(),
            dislikeCount=db.query(UserRestDislike).filter(UserRestDislike.rest_id == rest_instance.google_place_id).count(),
            hasCollected=True,
            hasLiked=db.query(UserRestLike).filter(UserRestLike.user_id == user_id).first() is not None,
            hasDisliked=db.query(UserRestDislike).filter(UserRestDislike.user_id == user_id).first() is not None,
        )
        for rest_instance in rest_collections
    ]
    if orderBy == "collect_cnt":
        simplified_rests = sorted(simplified_rests, key=itemgetter('collectCount'), reverse=True)
    
    return simplified_rests

def get_user_diary(db:Session, user_id:int, offset:int, limit:int, q: str) -> list[SimplifiedDiary]:
    diaries = db.query(UserDiaryCollect).filter(UserDiaryCollect.user_id == user_id).all()
    diary_ids = list(map(lambda x: x.diary_id, diaries))
    query = db.query(Diary).filter(Diary.diary_id.in_(diary_ids))
    if q != "":
        query = query.filter(Diary.title.ilike(f"%{q}%"))
    query = query.order_by(Diary.created.desc())
    query = query.offset(offset).limit(limit)
    diary_collections = query.all()
    simplified_diaries = [
        SimplifiedDiary(
            id=diary_instance.diary_id,
            imageUrl=diary_instance.avatar_url,
            restaurantName=db.query(Restaurant).filter(Restaurant.google_place_id == diary_instance.rest_id).first().rest_name
        )
        for diary_instance in diary_collections
    ]
    
    return simplified_diaries

