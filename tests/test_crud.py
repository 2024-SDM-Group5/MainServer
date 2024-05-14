import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, engine, SessionLocal
from app.crud import users, restaurants, maps, follow, diaries, collections, comments
from app.models.dbModel import *
from app.schemas.restaurants import FullCreateRestaurant
from app.schemas.diaries import DiaryCreate, DiaryUpdate
from app.schemas.comments import CommentCreate, CommentUpdate
from app.schemas.maps import MapCreate
from app.schemas.users import UserLoginInfo

class TestUser:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    @pytest.mark.parametrize(
        ("id"),
        [
            1,
            3,
            4
        ],
    )
    def test_get_user_by_id(self, id):
        user = users.get_user_by_id(self.session, id)
        assert user.user_id == id

    @pytest.mark.parametrize(
        ("email"),
        [
            "pohan.ho@gmail.com",
            "j8832266@gmail.com",
            "claire32246223@gmail.com"
        ],
    )
    def test_get_user_by_email(self, email):
        user = users.get_user_by_email(self.session, email)
        assert user.email == email
    
    @pytest.mark.parametrize(
        ("user"),
        [
            {
                "user_name": "John",
                "email": "john@email.com"
            }
        ],
    )
    def test_create_user(self, user):
        create_user = users.create_user(self.session, user)
        john = self.session.query(User).filter(User.user_name == user["user_name"]).first()
        assert john.user_name == user["user_name"]
        assert john.email != user["email"]
    
    @pytest.mark.parametrize(
        ("user"),
        [
            {
                "user_name": "John",
                "email": "john@email.com"
            }
        ],
    )
    def test_update_user(self, user):
        update = {
            "user_name": "JohnUpdate",
            "avatar_url": "image_url"
        }
        user_id = users.get_user_by_email(self.session, user["email"]).user_id
        update_user = users.update_user(self.session, user_id, update)
        update_john = self.session.query(User).filter(User.user_name == user["email"]).first()
        assert update_john.user_name == update["user_name"]
        assert update_john.avatar_url == update["avatar_url"]

    @pytest.mark.parametrize(
        ("user"),
        [
            {
                "user_name": "John",
                "email": "john@email.com"
            }
        ],
    )
    def test_delete_user(self, user):
        users.delete_user(self.session, users.get_user_by_email(self.session, user["email"]).user_id)
        john = self.session.query(User).filter(User.email == user["email"]).first()
        assert john is None
    @pytest.mark.parametrize(
        ("id"),
        [
            1,
            3,
            4
        ],
    )
    def test_get_user_diaries(self, id):
        diaries = users.get_user_diaries(self.session, id)
        for diary in diaries:
            assert diary.id == id

class TestRestaurant:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()
    
    @pytest.mark.parametrize(
        ("place_id"),
        [
            "ChIJycu5coupQjQRl9dmANfpHuw"
        ],
    )
    def test_get_restaurant(self, place_id):
        user_id = users.get_user_by_email(self.session, "pohan.ho@gmail.com").user_id
        restaurant = restaurants.get_restaurant(self.session, place_id, user_id)
        answer = self.session.query(Restaurant).filter(Restaurant.google_place_id == place_id).first()
        assert restaurant.address == answer.address
        assert restaurant.created == answer.created
        assert restaurant.google_place_id == answer.google_place_id
        assert restaurant.lat == answer.lat
        assert restaurant.lng == answer.lng
        assert restaurant.photo_url == answer.photo_url
        assert restaurant.rest_name == answer.rest_name
        assert restaurant.telephone == answer.telephone
        assert restaurant.rating == answer.rating
        assert restaurant.view_cnt == answer.view_cnt
    

    @pytest.mark.parametrize(
        ("restaurant", "update"),
        [
            (
                FullCreateRestaurant(
                name="test_restaurant",
                location={
                    "lat": 22.73,
                    "lng": 120.28
                },
                rating=3,
                place_id="test_restaurant_place_id",
                photo_url="test_restaurant_photo_url",
                address="test_restaurant_address",
                telephone="12345678"
                ),
                FullCreateRestaurant(
                name="test_restaurant_update",
                location={
                    "lat": 22.73,
                    "lng": 120.28
                },
                rating=3,
                place_id="test_restaurant_place_id",
                photo_url="test_restaurant_photo_url",
                address="test_restaurant_address",
                telephone="12345678"
                )
            )
        ],
    )
    def test_create_restaurant(self, restaurant, update):
        insert_restaurant = restaurants.create_update_restaurant(self.session, restaurant)
        answer = self.session.query(Restaurant).filter(Restaurant.google_place_id == restaurant.place_id).first()
        assert insert_restaurant.address == answer.address
        assert insert_restaurant.created == answer.created
        assert insert_restaurant.google_place_id == answer.google_place_id
        assert insert_restaurant.lat == answer.lat
        assert insert_restaurant.lng == answer.lng
        assert insert_restaurant.photo_url == answer.photo_url
        assert insert_restaurant.rest_name == answer.rest_name
        assert insert_restaurant.telephone == answer.telephone
        assert insert_restaurant.rating == answer.rating
        assert insert_restaurant.view_cnt == answer.view_cnt
        update_restaurant = restaurants.create_update_restaurant(self.session, update)
        answer = self.session.query(Restaurant).filter(Restaurant.google_place_id == restaurant.place_id).first()
        assert update_restaurant.rest_name == answer.rest_name
    
    @pytest.mark.parametrize(
        ("restaurant_id", "update"),
        [
            (
                "test_restaurant_place_id",
                {
                    "telephone": "87654321"
                }
            )
        ],
    ) 
    def test_update_restaurant(self, restaurant_id, update):
        update_restaurant = restaurants.update_restaurant(self.session, restaurant_id, update)
        answer = self.session.query(Restaurant).filter(Restaurant.google_place_id == restaurant_id).first()
        assert update_restaurant.telephone == answer.telephone

    @pytest.mark.parametrize(
        ("restaurant_id"),
        [
            "test_restaurant_place_id",
        ],
    )
    def test_delete_restaurant(self, restaurant_id):
        restaurants.delete_restaurant(self.session, restaurant_id)
        assert self.session.query(Restaurant).filter(Restaurant.google_place_id == restaurant_id).first() is None

    @pytest.mark.parametrize(
        ("user", "place_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_collect_restaurant(self, user, place_id):
        user_id = users.get_user_by_email(self.session, user)
        user_map = self.session.query(Map).filter(Map.author == user_id).first()
        collect = restaurants.collect_restaurant(self.session, user_id, place_id)
        assert self.session.query(UserRestCollect).filter(UserRestCollect.user_id == user_id, UserRestCollect.rest_id == place_id).first() is not None
        assert place_id in user_map.rest_ids

    @pytest.mark.parametrize(
        ("user", "place_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_uncollect_restaurant(self, user, place_id):
        user_id = users.get_user_by_email(self.session, user)
        user_map = self.session.query(Map).filter(Map.author == user_id).first()
        uncollect = restaurants.uncollect_restaurant(self.session, user_id, place_id)
        assert self.session.query(UserRestCollect).filter(UserRestCollect.user_id == user_id, UserRestCollect.rest_id == place_id).first() is None
        assert place_id not in user_map.rest_ids

    @pytest.mark.parametrize(
        ("user", "place_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_like_restaurant(self, user, place_id):
        user_id = users.get_user_by_email(self.session, user)
        like = restaurants.like_restaurant(self.session, user_id, place_id)
        assert self.session.query(UserRestLike).filter(UserRestLike.user_id == user_id, UserRestLike.rest_id == place_id).first() is not None
    
    @pytest.mark.parametrize(
        ("user", "place_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_unlike_restaurant(self, user, place_id):
        user_id = users.get_user_by_email(self.session, user)
        unlike = restaurants.unlike_restaurant(self.session, user_id, place_id)
        assert self.session.query(UserRestLike).filter(UserRestLike.user_id == user_id, UserRestLike.rest_id == place_id).first() is None

    @pytest.mark.parametrize(
        ("user", "place_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_dislike_restaurant(self, user, place_id):
        user_id = users.get_user_by_email(self.session, user)
        dislike = restaurants.dislike_restaurant(self.session, user_id, place_id)
        assert self.session.query(UserRestDislike).filter(UserRestDislike.user_id == user_id, UserRestDislike.rest_id == place_id).first() is not None

    @pytest.mark.parametrize(
        ("user", "place_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_undislike_restaurant(self, user, place_id):
        user_id = users.get_user_by_email(self.session, user)
        undislike = restaurants.undislike_restaurant(self.session, user_id, place_id)
        assert self.session.query(UserRestDislike).filter(UserRestDislike.user_id == user_id, UserRestDislike.rest_id == place_id).first() is None

class TestMap:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    @pytest.mark.parametrize(
        ("user", "map_id"),
        [
            ("pohan.ho@gmail.com", 1)
        ],
    )
    def test_get_map(self, user, map_id):
        user_id = users.get_user_by_email(self.session, user)
        test_map = maps.get_map(self.session, map_id, user_id)
        answer = self.session.query(Map).filter(Map.map_id == map_id).first()
        assert answer.author == test_map.author
        assert answer.description == test_map.description
        assert answer.icon_url == test_map.icon_url
        assert answer.lat == test_map.lat
        assert answer.lng == test_map.lng
        assert answer.map_name == test_map.map_name
        assert answer.tags == test_map.tags
        assert answer.rest_ids == test_map.rest_ids

    @pytest.mark.parametrize(
        ("user", "mapCreate"),
        [
            ("pohan.ho@gmail.com", 
             MapCreate(
                 description="test_description",
                 name="test_name",
                 iconUrl="test_url",
                 tags=[],
                 restaurants=[]
             ))
        ],
    )
    def test_create_map(self, user, mapCreate):
        user_id = users.get_user_by_email(self.session, user)
        userInfo = UserLoginInfo(userId=user_id, isNew=False)
        new_map = maps.create_map(self.session, mapCreate, userInfo)
        answer = self.session.query(Map).filter(Map.map_id == new_map).first()
        assert answer.description == mapCreate["description"]
        assert answer.map_name == mapCreate["name"]
        assert answer.icon_url == mapCreate["iconUrl"]
        assert answer.tags == mapCreate["tags"]
        assert answer.rest_ids == mapCreate["restaurants"]

    @pytest.mark.parametrize(
        ("user", "map_name"),
        [
            ("pohan.ho@gmail.com", "test_name")
        ],
    )
    def test_update_map(self, user, map_name):
        user_id = users.get_user_by_email(self.session, user)
        map_id = self.session.query(Map).filter(Map.author == user_id, Map.map_name == map_name).first().map_id
        update = {
            "description": "update_description",
            "tags": ["test_tags"]
        }
        update_map = maps.update_map(self.session, map_id, update, user_id)
        answer = self.session.query(Map).filter(Map.map_id == map_id).first()
        assert answer.description == update["description"]
        assert answer.tags == update["tags"]
    
    @pytest.mark.parametrize(
        ("user", "map_name"),
        [
            ("pohan.ho@gmail.com", "test_name")
        ],
    )
    def test_delete_map(self, user, map_name):
        user_id = users.get_user_by_email(self.session, user)
        map_id = self.session.query(Map).filter(Map.author == user_id, Map.map_name == map_name).first().map_id
        delete_map = maps.delete_map(self.session, map_id)
        assert self.session.query(Map).filter(Map.map_id == map_id).first() is None
    
    @pytest.mark.parametrize(
        ("user"),
        [
            "pohan.ho@gmail.com"
        ],
    )
    def test_get_map_by_user(self, user):
        user_id = users.get_user_by_email(self.session, user)
        map_list = maps.get_maps_by_user(self.session, user_id)
        for map in map_list:
            assert map.author == user_id

    @pytest.mark.parametrize(
        ("map_id", "query"),
        [
            (1,{
                "orderBy": "name",
                "q": None,
                "auth_user_id": 1
            })
        ],
    )
    def test_get_restaurants(self, map_id, query):
        count, rest_list = maps.get_restaurants(self.session, map_id, query)
        answer = self.session.query(Map).filter(Map.map_id == map_id).first().rest_ids
        assert count == len(rest_list)
        for rest in rest_list:
            rest_id = self.session.query(Restaurant).filter(Restaurant.rest_name == rest.name).first().google_place_id
            assert rest_id in answer
    
    @pytest.mark.parametrize(
        ("user", "map_id"),
        [
            ("pohan.ho@gmail.com", 2)
        ],
    )
    def test_collect_map(self, user, map_id):
        user_id = users.get_user_by_email(self.session, user)
        maps.collect_map(self.session, user_id, map_id)
        assert self.session.query(UserMapCollect).filter(UserMapCollect.map_id == map_id, UserMapCollect.user_id == user_id).first() is not None

    @pytest.mark.parametrize(
        ("user", "map_id"),
        [
            ("pohan.ho@gmail.com", 2)
        ],
    )
    def test_uncollect_map(self, user, map_id):
        user_id = users.get_user_by_email(self.session, user)
        maps.uncollect_map(self.session, user_id, map_id)
        assert self.session.query(UserMapCollect).filter(UserMapCollect.map_id == map_id, UserMapCollect.user_id == user_id).first() is None

class TestDiaryComment:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    @pytest.mark.parametrize(
        ("user", "diary"),
        [
            ("pohan.ho@gmail.com", 
             DiaryCreate(
                 restaurantId="ChIJycu5coupQjQRl9dmANfpHuw",
                 photos=["test_photo"],
                 content="test_content",
                 items=["test_items"]
             ))
        ],
    )
    def test_creste_diary(self, user, diary):
        user_id = users.get_user_by_email(self.session, user)
        test_diary = diaries.create_diary(self.session, diary, user_id)
        answer = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == diary["restaurantId"]).first()
        assert answer.photos == test_diary.photos
        assert answer.content == test_diary.content
        assert answer.items == test_diary.items
    
    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_get_diary(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        answer = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first()
        get_diary = diaries.get_diary(self.session, answer.diary_id, user_id)
        assert answer.diary_id == get_diary.id
        assert answer.user_id == get_diary.userId
        assert answer.rest_id == get_diary.restaurantId
        assert answer.content == get_diary.content
        assert answer.items == get_diary.items
        assert answer.photos == get_diary.photos
        assert get_diary.username == self.session.query(User).filter(User.user_id == get_diary.userId).first().user_name
        assert get_diary.restaurantName == self.session.query(Restaurant).filter(Restaurant.google_place_id == get_diary.restaurantId).first().rest_name
        assert get_diary.favCount == self.session.query(UserDiaryLike).filter(UserDiaryLike.diary_id == get_diary.id).count()
        assert get_diary.collectCount == self.session.query(UserDiaryCollect).filter(UserDiaryCollect.diary_id == get_diary.id).count()
    
    @pytest.mark.parametrize(
        ("user", "rest_id", "update"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw",
             DiaryUpdate(
                 photos=["update_photo"],
                 content="update_content",
                 items=["update_items"]
             ))
        ],
    )
    def test_update_diary(self, user, rest_id, update):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        update_diary = diaries.update_diary(self.session, diary_id, user_id, update)
        answer = self.session.query(Diary).filter(Diary.diary_id == diary_id).first()
        assert update_diary.content == answer.content
        assert update_diary.photos == answer.photos
        assert update_diary.items == answer.items
    
    @pytest.mark.parametrize(
        ("user", "rest_id", "content"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw", "test_comment")
        ],
    )
    def test_create_comment(self, user, rest_id, content):
        user_id = users.get_user_by_email(self.session, user)
        comment = CommentCreate(diaryId=self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id,
                                content=content)
        new_comment = comments.create_comment(self.session, user_id, comment)
        answer = self.session.query(Comment).filter(Comment.comment_id == new_comment.id).first()
        assert answer.diary_id == comment.diaryId
        assert answer.content == comment.content

    @pytest.mark.parametrize(
        ("user", "rest_id", "content"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw", "update_comment")
        ],
    )
    def test_update_comment(self, user, rest_id, content):
        user_id = users.get_user_by_email(self.session, user)
        comment = CommentUpdate(diaryId=self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id,
                                content=content)
        comment_id = self.session.query(Comment).filter(Comment.author == user_id, Comment.diary_id == CommentUpdate.diaryId).first().comment_id
        update_comment = comments.update_comment(self.session, user_id, comment_id, comment)
        answer = self.session.query(Comment).filter(Comment.comment_id == update_comment.id).first()
        assert answer.content == comment.content
    
    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_delete_comment(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        comment_id = self.session.query(Comment).filter(Comment.author == user_id, Comment.diary_id == diary_id).first().comment_id
        delete_comment = comments.delete_comment(self.session, user_id, comment_id)
        assert self.session.query(Comment).filter(Comment.comment_id == comment_id).first() is None
    
    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_collect_diary(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        collect = diaries.collect_diary(self.session, user_id, diary_id)
        assert self.session.query(UserDiaryCollect).filter(UserDiaryCollect.user_id == user_id, UserDiaryCollect.diary_id == diary_id).first() is not None

    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_uncollect_diary(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        uncollect = diaries.uncollect_diary(self.session, user_id, diary_id)
        assert self.session.query(UserDiaryCollect).filter(UserDiaryCollect.user_id == user_id, UserDiaryCollect.diary_id == diary_id).first() is None

    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_favorite_diary(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        favorite = diaries.favorite_diary(self.session, user_id, diary_id)
        assert self.session.query(UserDiaryLike).filter(UserDiaryLike.user_id == user_id, UserDiaryLike.diary_id == diary_id).first() is not None

    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_unfavorite_diary(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        unfavorite = diaries.unfavorite_diary(self.session, user_id, diary_id)
        assert self.session.query(UserDiaryLike).filter(UserDiaryLike.user_id == user_id, UserDiaryLike.diary_id == diary_id).first() is None

    @pytest.mark.parametrize(
        ("user", "rest_id"),
        [
            ("pohan.ho@gmail.com", "ChIJycu5coupQjQRl9dmANfpHuw")
        ],
    )
    def test_delete_diary(self, user, rest_id):
        user_id = users.get_user_by_email(self.session, user)
        diary_id = self.session.query(Diary).filter(Diary.user_id == user_id, Diary.rest_id == rest_id).first().diary_id
        diaries.delete_diary(self.session, diary_id)
        assert self.session.query(Diary).filter(Diary.diary_id == diary_id).first() is None 

class TestFollow:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    @pytest.mark.parametrize(
        ("follower", "followee"),
        [
            (1, 3),
            (3, 6),
            (4, 9),
        ],
    )
    def test_create_follow(self, follower, followee):
        following = follow.create_follow(self.session, follower=follower, followee=followee)
        answer = self.session.query(UserFollow).filter(UserFollow.follow == follower, UserFollow.be_followed == followee).first()
        assert answer is not None

    @pytest.mark.parametrize(
        ("follower", "followee"),
        [
            (1, 3),
            (3, 6),
            (4, 9),
        ],
    )
    def test_delete_follow(self, follower, followee):
        following = follow.delete_follow(self.session, follower=follower, followee=followee)
        answer = self.session.query(UserFollow).filter(UserFollow.follow == follower, UserFollow.be_followed == followee).first()
        assert answer is None

class TestCollection:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    @pytest.mark.parametrize(
        ("id"),
        [
            1,
            3,
            4
        ],
    )
    def test_get_user_map(self, id):
        map_list = collections.get_user_map(self.session, id, "created", 0, 10, "")
        if len(map_list) != 0:
            test_map = map_list[0]
            answer = maps.get_map(self.session, test_map.id, id)
            assert test_map.id == answer.map_id
            assert test_map.name == answer.map_name
            assert test_map.id == answer.map_id
            assert test_map.iconUrl == answer.icon_url or test_map.iconUrl == ""
            assert test_map.authorId == answer.author
            assert test_map.author == self.session.query(User).filter(User.user_id == answer.author).first().user_name
            assert test_map.viewCount == answer.view_cnt
            assert test_map.collectCount == self.session.query(UserMapCollect).filter(UserMapCollect.map_id == answer.map_id).count()
            assert test_map.hasCollected == True
            assert test_map.center == {"lat": answer.lat, "lng": answer.lng}
        else:
            assert map_list == []

    @pytest.mark.parametrize(
        ("id"),
        [
            1,
            3,
            4
        ],
    )
    def test_get_user_rest(self, id):
        rest_list = collections.get_user_rest(self.session, id, "created", 0, 10, "")
        if len(rest_list) != 0:
            test_rest = rest_list[0]
            answer = restaurants.get_restaurant(self.session, test_rest.placeId, id)
            assert test_rest.name == answer.rest_name
            assert test_rest.location == {"lat": answer.lat, "lng": answer.lng}
            assert test_rest.rating == answer.rating
            assert test_rest.placeId == answer.google_place_id
            assert test_rest.viewCount == answer.view_cnt
            assert test_rest.collectCount == self.session.query(UserRestCollect).filter(UserRestCollect.rest_id == answer.google_place_id).count()
            assert test_rest.likeCount == self.session.query(UserRestLike).filter(UserRestLike.rest_id == answer.google_place_id).count()
            assert test_rest.dislikeCount == self.session.query(UserRestDislike).filter(UserRestDislike.rest_id == answer.google_place_id).count()
            assert test_rest.hasCollected == True
            assert test_rest.hasLiked == self.session.query(UserRestLike).filter(UserRestLike.rest_id == answer.google_place_id).first() is not None
            assert test_rest.hasDisliked == self.session.query(UserRestDislike).filter(UserRestDislike.rest_id == answer.google_place_id).first() is not None
        else:
            assert rest_list == []

    @pytest.mark.parametrize(
        ("id"),
        [
            1,
            3,
            4
        ],
    )
    def test_get_user_diary(self, id):
        diary_list = collections.get_user_diary(self.session, id, 0, 10, "")
        if len(diary_list) != 0:
            test_diary = diary_list[0]
            answer = diaries.get_diary(self.session, test_diary.id, id)
            assert test_diary.id == answer.id
            assert test_diary.imageUrl == answer.photos[0]
            assert test_diary.restaurantName == answer.restaurantName
        else:
            assert diary_list == []


    

    