# Backend API

## BACKEND_URL
    
```
https://mainserver-fdhzgisj6a-de.a.run.app/
```

## Docker image

```
enip2473/fastapi-app
```

## Users


| API Name | Description | Endpoint | Method | 
|---|---|---|---|
| [Login / Register](###Login) | Logs in or registers a user using Google OAuth 2.0 | `/api/v1/users/login` | POST |
| [Update User Profile](###Update) | Updates a user's display name and avatar | `/api/v1/users/update` | PUT |
| [Upload Avatar](###Avatar_Upload) | Uploads a new avatar image for a user | `/api/v1/users/avatar` | POST |
| [Follow User](###Follow_User) | Allows a user to follow another user | `/api/v1/users/follow` | POST |
| [Unfollow User](###Unfollow_User) | Allows a user to unfollow another user | `/api/v1/users/unfollow` | POST |
| [Get User Detail](###User_Detail) | Retrieves detailed information about a user | `/api/v1/users/{id}` | GET |
| [Get My Detail](###My_Detail)| Retrieves detailed information about the logged-in user | `/api/v1/users/me` | GET |
| [Get User Diaries](###Diaries) | Retrieves a list of diaries written by a user | `/api/v1/users/{id}/diaries` | GET |

## Maps

| API Name | Description | Endpoint | Method | 
|---|---|---|---|
| [Get Maps](###Get_Maps) | Retrieves all maps | `/api/v1/maps` | GET |
| [Create Map](###Create_Map) | Creates a new map | `/api/v1/maps` | POST |
| [Single Map](###Single_Map) | Retrieves details of a specific map | `/api/v1/maps/{id}` | GET |
| [Restaurants in Map](###Restaurants_Map) | Retrieves restaurants of a specific map | `/api/v1/maps/{id}/restaurants` | GET |
| [Modify Map](###Modify_Map) | Updates an existing map | `/api/v1/maps/{id}` | PUT |
| [Delete Map](###Delete_Map) |  Deletes a map | `/api/v1/maps/{id}` | DELETE |
| [Favorite Map](###Favorite_Map) | Allows a user to favorite a map | `/api/v1/maps/{id}/favorites` | POST |
| [Unfavorite Map](###Unfavorite_Map) | Allows a user to unfavorite a map | `/api/v1/maps/{id}/favorites` | DELETE |


## Restaurants

| API Name | Description | Endpoint | Method | 
|---|---|---|---|
| [All Restaurants](###All_Restaurants) | Retrieves data of all restaurants | `/api/v1/restaurants` | GET |
| [Single Restaurant](###Single_Restaurant) | Retrieves details of a specific restaurant | `/api/v1/restaurants/{placeId}` | GET |

## Comments

| API Name | Description | Endpoint | Method | 
|---|---|---|---|
| [Create a comment](###Comment_Create) | Creates a new comment for a restaurant | `/api/v1/comments` | POST |
| [Comment Edit](###Comment_Edit) | Edits an existing comment | `/api/v1/comments/{id}` | PUT |
| [Comment Delete](###Comment_Delete) | Deletes a comment | `/api/v1/comments/{id}` | DELETE |

## Diaries

| API Name | Description | Endpoint | Method | 
|---|---|---|---|
| [Diaries](###Diaries_Get) | Retrieves a list of diaries | `/api/v1/diaries` | GET |
| [Diary Create](###Diary_Create) | Creates a new diary | `/api/v1/diaries` | POST |
| [Single Diary](###Single_Diary) | Retrieves a specific diary | `/api/v1/diaries/{id}` | GET |
| [Diary Update](###Diary_Update) | Updates an existing diary | `/api/v1/diaries/{id}` | PUT |
| [Diary Delete](###Diary_Delete) | Deletes a diary | `/api/v1/diaries/{id}` | DELETE |

## Collections

| API Name | Description | Endpoint | Method | 
|---|---|---|---|
| [Diary Collections](###Diary_Collections) | Retrive user favorite diaries | `/api/v1/collections/diary` | GET |
| [Map Collections](###Map_Collections) | Retrive user favorite maps | `/api/v1/collections/map` | GET |
| [Restaurant Collections](###Restaurant_Collections) | Retrive user favorite restaurants | `/api/v1/collections/restaurants` | GET |



    
## Users


### Login

- Route
    - /api/v1/users/login
- Method
    - POST
- Field
    - string
    - idToken
        - Token received through Google OAuth 2.0
- Example Query:

    ```jsx
    {
        idToken: "awejrlwejtkljwaklt"
    }
    ```

- Response
    - userId: number
        - The unique id of user. Auto generate one if the user is a new user.
    - isNew: boolean
        - True if the user is login first time
- Example Response

    ```jsx
    {
        userId: 11,
        isNew: false
    }
    ```

### Update
- Route
    - /api/v1/users/{id}
- Method
    - PUT
- Header
    - Authorization:
        - idToken: string
            - The author’s login token.
- Field
    - displayName: string
        - The name you want to display to others
    - avatarUrl: string
        - The url of the user avatar
- Example Query:

    ```jsx
    {
        "displayName": "enip",
        "avatarUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    ```

- Response
    - success: boolean
    - message: string
- Example Response

```jsx
{
    success: true,
    message: "User data updated successfully"
}
```

### Avatar_Upload
    
- Route
    - /api/v1/users/avatar
- Method
    - POST
- Field
    - avatar: File
        - The avatar you want to upload
- Return

```jsx
{
    "avatarUrl": "https://afdskjglas" 
}
```

### Follow_User
    
- Route
    ```
    /api/v1/users/follow
    ```
- Method
    - POST
- Header
    - Authorization:
        - idToken: string
            - The author’s login token.
- Field
    - userId: number
        - The ID of the user who wants to follow another user
    - followId: number
        - The ID of the user to be followed
- Response
    - success: boolean
    - message: string
- Example Response

```jsx
{
    success: true,
    message: "Followed successfully"
}
```

### Unfollow_User
    
- Route
    ```
    /api/v1/users/unfollow
    ```
- Method
    - POST
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Field
    - userId: number
        - The ID of the user who wants to unfollow another user
    - unfollowId: number
        - The ID of the user to be unfollowed

- Response
    - success: boolean
    - message: string
- Example Response

```jsx
{
    success: true,
    message: "Unfollowed successfully"
}
```


### User_Detail
    
- Route
    - /api/v1/users/{id}
- Method
    - GET
- Header (Optional)
    - Only needed when you need isFollowing
    - Authorization: Bearer ${idToken}
- Response Field
    - id: number
        - The unique id of the user.
    - displayName: string
        - The name you want to display to others
    - avatarUrl: string
        - The url of the user avatar
    - following: number
        - How many other users this user is following
    - followed: number
        - How many user is following this user
    - mapId: number
        - The id of map created by this user
    - postCount: number
        - The number of posts from the user
    - isFollowing: bool
        - If the current login user is following this user. If user is not logged in, it returns false.
- Example Response

```jsx
{
        "id": 1,
        "displayName": "John Doe",
        "avatarUrl": "https://example.com/avatar.jpg",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50
}
```


### My_Detail

- Route
    - /api/v1/users/me
- Method
    - GET
- Headers
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Field
    - id: number
        - The unique id of the user.
    - displayName: string
        - The name you want to display to others
    - avatarUrl: string
        - The url of the user avatar
    - following: number
        - How many other users this user is following
    - followed: number
        - How many user is following this user
    - mapId: number
        - The id of map created by this user
    - postCount: number
        - The number of posts from the user
- Example Response

```jsx
{
        "id": 1,
        "displayName": "John Doe",
        "avatarUrl": "https://example.com/avatar.jpg",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50
}
```

### Diaries

- Route
    - /api/v1/users/{id}/diaries
- Method
    - GET
- Path Parameter
    - id
        - The unique id of the user
- Status
    - 200
        - Success
    - 404
        - Not Found
        - The user with the specific id does not exist
    - 500
        - System Error
- Return Fields
    - diaries: object[]
        - Array of diary objects written by the user
        - A diary object includes:
            - id: number
                - The unique id of the diary
            - imageUrl: string
                - The url of the image in the diary
- Example Return

```jsx
[
    {
        "id": 1,
        "imageUrl": "<https://example-image-url1.com>"
    },
    {
        "id": 2,
        "imageUrl": "<https://example-image-url2.com>"
    }
]

```

### Collections

- Route: `/api/v1/users/collections`
- Method: GET
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Status Codes:
    * 200: Success
    * 404: Not Found (The user with the specific id does not exist)
    * 500: System Error
- Return Fields 
    * diaries: object[] 
        * Array of simplified diary objects collected by the user
        * A simplified diary object includes:
            * id: number 
                * The unique id of the diary
            * imageUrl: string
                *  The URL of a representative image in the diary (likely the first photo)
* Example Return

```jsx
[
  {
    "id": 5, 
    "imageUrl": "https://some-image-hosting-website.com/diaryImage5.jpg"
  },
  {
    "id": 22,
    "imageUrl": "https://some-image-hosting-website.com/anotherDiaryImage.png"
  }
]
```

    
## Map

### Get_Maps
        
- Route
    - /api/v1/maps
- Method
    - GET
- Query Parameter
    - orderBy
        - favCount: 收藏數
        - createTime: 建立日期
    - tags
        - 想要的 tag
        - tag 間用 or 的（可討論）
        - 若無此 field 則預設全部
    - offset
        - 從第幾個開始，用在 pagination。
        - 0-based
        - default: 0
    - limit
        - 最多回傳幾個 map
        - default:10
    - reverse
        - 是否反向 (ex. 預設高到低，reverse 就是低到高)
        - default: false
    - q
        - 搜尋關鍵字
- Query Example

    ```jsx
    GET 
    /api/v1/maps?tags=台北,飲料&orderBy=favCount&offset=10&limit=15&reverse=false
    ```

- Status
    - 200
        - Success
    - 500
        - System Error
- Return fields
    - total: map 總數
    - offset: 從第幾個開始
    - limit: 回傳幾個
    - maps: A list with simplified maps, return when status=200
        - id: number
            - The id of the map
        - name: string
            - The name of the map
        - iconUrl: string | null
            - The url of the icon, null if not exist
        - author: string
            - The name of the author
        - viewCount: number
            - how many time the map is viewed
        - favCount: number
            - how many user collect this map
- Example Return

```jsx!
{
    "total": 3
    "maps": [
        {
            "id": 12,
            "name": "飲料導覽",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 370,
            "favCount": 152
        },
        {
            "id": 13,
            "name": "夜市飲料攻略",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 295,
            "favCount": 117
        }
    ],
    "limit": 10,
    "offset": 1
}
```
            
### Create_Map
- Route
    - /api/v1/maps
- Method
    - POST
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token, will check.

        ```jsx
        {
            Authorization: Bearer ${idToken}
        }
        ```

- Field
    - name: string
        - The name of the new map
    - authorId: number
        - The author of the map
    - tags: string[]
        - The tags of the new map
    - restaurants: strings[]
        - A list of restaurants’ placeId.
        - placeId is identical to Google place API
        - How to get it?
- Example Request

    ```jsx
    POST /api/v1/maps

    {
        name: "台北飲料地圖",
        authorId: 123,
        tags: ["台北","飲料"]
        restaurants: [
            "asdjglsakjgka",
            "wewtwatqawt",
            "sdagasgasgsa"
        ]
    }
    ```

- Status
    - 201
        - Successfully created
    - 400
        - Bad Request, fields incorrect
        - check error message
    - 401
        - Unauthorized
        - idToken incorrect
    - 500
        - system error
- Return Fields
    - id: the Id of the newly created map
- Example Return

    ```jsx
    {
        id: 11
    }
    ```
            
### Single_Map

- Route
    - /api/v1/maps/{id}
- Method
    - GET
- Path Parameter
    - id
        - The unique id of the map
- Header (optional)
    - Authorization: Bearer ${idToken}
    - Only when you need hasFavorited
- Status
    - 200
        - Success
    - 404
        - Not Found
        - The map with the specific id does not exist
    - 500
        - System Error
- Return Fields
    - id: number
        - The id of the map
    - name: string
        - The name of the map
    - iconUrl: string | null
        - The url of the icon, null if not exist
    - center: object
        - Contains the latitude (lat) and longitude (lng) of the map
    - author: string
        - The name of the author
    - viewCount: number
        - How many times the map has been viewed
    - favCount: number
        - How many users have collected this map
        - Example Return
        
        ```jsx
        {
            "id": 11,
            "name": "台北飲料地圖",
            "iconUrl": "https://mypicture/11.png",
            "center": {
                "lat": 25.0329694,
                "lng": 121.5654118
             }
            "author": "enip",
            "viewCount": 441,
            "favCount": 189,
            "hasFavorited": false
        }
        ```
### Restaurants_Map

- Route
    - /api/v1/maps/{id}/restaurants
- Method
    - GET
- Path Parameter
    - id: The id of the map
- Query Parameter
    - orderBy
        - favCount: 收藏數
        - createTime: 建立日期
    - tags
        - 想要的 tag
        - tag 間用 or 的（可討論）
        - 若無此 field 則預設全部
    - offset
        - 從第幾個開始，用在 pagination。
        - 0-based
        - default: 0
    - limit
        - 最多回傳幾個 map
        - default:10
    - reverse
        - 是否反向 (ex. 預設高到低，reverse 就是低到高)
        - default: false
    - q
        - 搜尋關鍵字
    - sw
        - 搜尋的左下角，格式為 f"{lat},{lng}"
    - ne
        - 搜尋的右上角，格式為 f"{lat},{lng}"
- Return fields:
    - total: 餐廳總數
    - offset: 從第幾個開始
    - limit: 回傳幾個
    - restaurants: 餐廳陣列
        - placeId: string
        - The unique Google Place ID of the restaurant
    - name: string
        - The name of the restaurant
    - location: object
        - Contains the latitude (lat) and longitude (lng) of the restaurant
    - address: string
        - The address of the restaurant
    - telephone: string
        - The telephone number of the restaurant
    - rating: number
        - The rating of the restaurant
    - viewCount: number
        - How many times the restarant is viewed
    - favCount: number
        - How many times the restaurant is favorited

- Example Return
```json
{
    "total": 3,
    "restaurants": [
        {
            "name": "Restaurant 2",
            "address": "台北市大安區辛亥路二段170號",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "telephone": "02 1234 5554",
            "rating": 4.2,
            "placeId": "wewtwatqawt",
            "viewCount": 400,
            "favCount": 100
        },
        {
            "name": "Restaurant 3",
            "address": "台北市大安區辛亥路二段170號",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "telephone": "02 1234 5554",
            "rating": 4.2,
            "placeId": "wewtwatqawt",
            "viewCount": 400,
            "favCount": 100
        }
    ],
    "limit": 10,
    "offset": 1
}
```

        
### Modify_Map
        
- Route
    - /api/v1/maps/{id}
- Method
    - PUT
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.

    ```jsx
    {
    Authorization: Bearer ${token}
    }
    ```

- Field
    - name: string
        - The new name of the map
    - authorId: number
        - The author of the map
    - tags: string[]
        - The new tags of the map
    - restaurants: strings[]
        - The new list of restaurants’ placeId.
- Example Request

    ```jsx
    PUT /api/v1/maps/11

    {
        idToken: "afdasfsagasg",
        name: "台北飲料地圖",
        authorId: 123,
        tags: ["台北、飲料"]
        restaurants: [
            "asdjglsakjgka",
            "wewtwatqawt",
            "sdagasgasgsa"
        ]
    }
    ```

- Status
    - 200
        - Successfully updated
    - 400
        - Bad Request, fields incorrect
        - check error message
    - 401
        - Unauthorized
        - idToken incorrect
    - 404
        - Not Found
        - The map with the specific id does not exist
    - 500
        - system error
- Return Fields
    - id: the Id of the updated map
- Example Return

    ```jsx
    {
        id: 11
    }
    ```
            
### Delete_Map
        
- Route
    - /api/v1/maps/{id}
- Method
    - DELETE
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Path Parameter
    - id
        - The unique id of the map
- Status
    - 200
        - Success
    - 404
        - Not Found
        - The map with the specific id does not exist
    - 500
        - System Error
- Example Request

    ```jsx
    DELETE /api/v1/maps/11
    ```
- Return Fields
    - id: the Id of the deleted map
- Example Return

    ```jsx
    {
        id: 11
    }
    ```



### Favorite_Map
        
- Route
    - /api/v1/maps/{id}/favorites
- Method
    - POST
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Path Parameter
    - id
        - The unique id of the map
- Field
    - userId: number
        - The userId of the user
- Status
    - 200
        - Success
    - 401
        - Unauthorized
        - The user failed to login
    - 404
        - Not Found
        - The map with the specific id does not exist
    - 500
        - System Error
- Return Fields
    - id: the Id of the favorited map
- Example Return

    ```jsx
    {
        id: 11
    }
    ```

    
### Unfavorite_Map

- Route
    - /api/v1/maps/{id}/favorites
- Method
    - DELETE
- Path Parameter
    - id
        - The unique id of the map
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Field
    - userId: number
        - The userId of the user
- Status
    - 200
        - Success
    - 401
        - Unauthorized
        - The user failed to login
    - 404
        - Not Found
        - The map with the specific id does not exist
    - 500
        - System Error
- Return Fields
    - id: the Id of the unfavorited map
- Example Return

    ```jsx
    {
        id: 11
    }
    ```



## Restaurants

## All_Restaurants

- Route
    - /api/v1/restaurants
- Method
    - GET
- Query Parameter
    - orderBy
        - favCount: 收藏數
        - createTime: 建立日期
    - tags
        - 想要的 tag
        - tag 間用 or 的（可討論）
        - 若無此 field 則預設全部
    - offset
        - 從第幾個開始，用在 pagination。
        - 0-based
        - default: 0
    - limit
        - 最多回傳幾個 map
        - default:10
    - reverse
        - 是否反向 (ex. 預設高到低，reverse 就是低到高)
        - default: false
    - q
        - 搜尋關鍵字
- Return fields:
    - total: 餐廳總數
    - offset: 從第幾個開始
    - limit: 回傳幾個
    - restaurants: 餐廳陣列
        - placeId: string
        - The unique Google Place ID of the restaurant
    - name: string
        - The name of the restaurant
    - location: object
        - Contains the latitude (lat) and longitude (lng) of the restaurant
    - address: string
        - The address of the restaurant
    - telephone: string
        - The telephone number of the restaurant
    - rating: number
        - The rating of the restaurant
    - viewCount: number
        - How many times the restarant is viewed
    - favCount: number
        - How many times the restaurant is favorited

- Example Return
```json
{
    "total": 3,
    "restaurants": [
        {
            "name": "Restaurant 2",
            "address": "台北市大安區辛亥路二段170號",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "telephone": "02 1234 5554",
            "rating": 4.2,
            "placeId": "wewtwatqawt",
            "viewCount": 400,
            "favCount": 100
        },
        {
            "name": "Restaurant 3",
            "address": "台北市大安區辛亥路二段170號",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "telephone": "02 1234 5554",
            "rating": 4.2,
            "placeId": "wewtwatqawt",
            "viewCount": 400,
            "favCount": 100
        }
    ],
    "limit": 10,
    "offset": 1
}
```


### Single_Restaurant
        
- Route
    - /api/v1/restaurants/{placeId}
- Method
    - GET
- Path Parameter
    - placeId (string)
        - The unique placeId of the restaurant
- Status
    - 200
        - Success
    - 404
        - Not Found
        - The restaurant with the specific id does not exist
    - 500
        - System Error
- Return Fields
    - placeId: string
        - The unique Google Place ID of the restaurant
    - name: string
        - The name of the restaurant
    - location: object
        - Contains the latitude (lat) and longitude (lng) of the restaurant
    - address: string
        - The address of the restaurant
    - telephone: string
        - The telephone number of the restaurant
    - rating: number
        - The rating of the restaurant
    - viewCount: number
        - How many times the restarant is viewed
    - favCount: number
        - How many times the restaurant is favorited
    - diaries: Diary[]
        - The diaries from the users
        - The diary includes:
            - id: int
                - The id of the diary
            - imageUrl: HttpUrl = Field(None)
                - The image of the diary
- Example Return

    ```jsx
    {
        "name": "Restaurant 1",
        "location": {
            "lat": 25.0329694,
            "lng": 121.5654177
        },
        "address": "台北市大安區辛亥路二段 170 號"
        "telephone": "02 3366 1234"
        "rating": 4.5,
        "placeId": "asdjglsakjgka",
        "viewCount": 100,
        "favCount": 100
        "diaries": [
            {"id": 1, "imageUrl": "https://aaaa.png"},
            {"id": 2, "imageUrl": "https://bbbb.png"}
        ]
    }
    ```
            
## Comments
    
### Comment_Create
- Route
    - /api/v1/comments
- Method
    - POST
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Field
    - diaryId: int
        - The id of the diary
    - content: string
        - The content of the comment
        
- Example Request

```jsx
POST /api/v1/comments

{
    "diaryId": 1,
    "content": "食物很好吃",
}
```

- Status
    - 201
        - Successfully created
    - 400
        - Bad Request, fields incorrect
    - 500
        - system error
- Return Fields
    - id: the Id of the newly created comment
- Example Return

```jsx
{
    id: 1
}
```
        
### Comment_Edit
- Route
    - /api/v1/comments/{id}
- Method
    - PUT
- Path Parameter
    - id
        - The unique id of the comment
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Field
    - diaryId: int
        - The id of the diary
    - content: string
        - The new content of the comment

- Example Request

```jsx
PUT /api/v1/comments/1

{
    "diaryId": 1,
    "content": "食物很美味"
}

```

- Status
    - 200
        - Successfully updated
    - 400
        - Bad Request, fields incorrect
    - 500
        - system error
- Return Fields
    - id: the Id of the updated comment
- Example Return

```jsx
{
    id: 1
}

```
        
### Comment_Delete

- Route
    - /api/v1/comments/{id}
- Method
    - DELETE
- Path Parameter
    - id
        - The unique id of the comment
- Header
    - Authorization: Bearer ${idToken}
        - idToken: string
            - The author’s login token.
- Status
    - 200
        - Success
    - 404
        - Not Found
        - The comment with the specific id does not exist
    - 500
        - System Error
- Example Request

```jsx
DELETE /api/v1/comments/1
```
        
## Diary
    
### Diaries_Get

- Route
    - /api/v1/diaries
- Query parameter
    - offset: where to start
    - limit: the number request
- Method
    - GET
- Return: Diary[], where diary consist
    - username: string
        - Username of the diary owner
    - avatarUrl: string
        - The url of the user's avatar
    - photos: string[]
        - Url of photos in the dairy
    - content: string
        - The content of the diary
    - replies: reply[]
        - Reply contains:
            - id: int
                - The id of the reply
            - username: string
                - the username of reply
            - avatarUrl: string
            - content: string
            - createdAt: number
    - favCount: number
        - How many people like this diary
    - createdAt: number
        - The created time of the diary
    - rating: number
        - The rating you give to the restaurant

- Example Response

```jsx
[
  {
    "id": 1,
    "username": "foodieJane",
    "avatarUrl": "https://myavatar.jpg"
    "photos": ["https://myphotos.com/diarypic1.jpg", "https://myphotos.com/diarypic2.jpg"],
    "content": "Tried this amazing boba place today!",
    "replies": [
      { 
        "username": "bobaLover",     
        "avatarUrl": "https://myavatar.jpg",
        "content": "Looks delicious!"
        "createdAt": 1711987663
      }
    ],
    "favCount": 25,
    "createdAt": 1711987662
  }
]
```

### Diary_Create
- Route: `/api/v1/diaries`
- Method: POST
- Header: 
    - Authorization: Bearer ${idToken}
- Fields:
    - restaurantId: string (The placeId of the restaurant)
    - photos: string[] (Array of Photo URLs)
    - content: string 
- Status Codes:
    - 201: Successfully created
    - 400: Bad Request 
    - 401: Unauthorized
    - 500: System Error
- Return:
    - id: number (ID of the new diary)
- Example Request

```jsx
POST /api/v1/diaries
{
  "restaurantId": 1,
  "photos": ["https://myphotos.com/diarypic1.jpg"],
  "content": "Best ramen ever!"
}
```

### Single_Diary
- Route: `/api/v1/diaries/{id}`
- Method: GET
- Path Parameter:
    - id: number (Diary ID)
- Header (Optional)
    - Only needed when you need hasFavorited
    - Authorization: Bearer ${idToken}
- Status Codes:
    - 200: Success
    - 404: Not Found
    - 500: System Error
- Return
    - username: string
        - Username of the diary owner
    - avatarUrl: string
        - The url of the user's avatar
    - restaurantName: string
        - The name of the restaurant
    - restaurantId: string
        - The placeId of the restaurant
    - photos: string[]
        - Url of photos in the dairy
    - content: string
        - The content of the diary
    - replies: reply[]
        - Reply contains:
            - id: int
                - the id of the reply
            - authorId: int
                - the id of the author
            - username: string
                - the username of reply
            - avatarUrl: string
                - The url of the user's avatar
            - content: string
            - createdAt: number
                - The created time of the diary
    - favCount: number
        - How many people like this diary
    - createdAt: number
        - The created time of the diary
    - hasFavorited: boolean
        - If the user has liked this diary
- Example Response

```jsx
{
    "id": 1,
    "username": "foodieJane",
    "avatarUrl": "https://myavatar.jpg",
    "restaurantName": "寶林茶室",
    "restaurantId": "ChIJIRh87uyrQjQR9oV3eqzxFJs",
    "photos": ["https://myphotos.com/diarypic1.jpg", "https://myphotos.com/diarypic2.jpg"],
    "content": "Tried this amazing boba place today!",
    "replies": [
      { 
        "id": 1,
        "authorId": 1,
        "username": "bobaLover",     
        "avatarUrl": "https://myavatar.jpg",
        "content": "Looks delicious!"
        "createdAt": 1711987663
      }
    ],
    "favCount": 25,
    "createdAt": 1711987662
}
```



### Diary_Update
- Route: `/api/v1/diaries/{id}`
- Method: PUT
- Path Parameter:
    - id: number (Diary ID)
- Header: 
    - Authorization: Bearer ${idToken}
- Fields
    - photos: string[]
        - Url of photos in the dairy
    - content: string
        - The content of the diary
- Status Codes:
    - 200: Successfully updated
    - 400: Bad Request 
    - 401: Unauthorized
    - 404: Not Found
    - 500: System Error
- Return:
    - id: number (ID of the updated diary)

### Diary_Delete

- Route: `/api/v1/diaries/{id}`
- Method: DELETE
- Path Parameter:
    - id: number (Diary ID)
- Header: 
    - Authorization: Bearer ${idToken}
- Status Codes:
    - 200: Success
    - 401: Unauthorized
    - 404: Not Found
    - 500: System Error

## Collections

### Diary_Collections

- Route: `/api/v1/collections/diary`
- Method: GET
- Header: 
    - Authorization: Bearer ${idToken}
- Return:
    - All diary collected by current user. 
    - A diary contains:
        - id: the id of the diary
        - imageUrl: The url of the first image of the diary
- Example:

```javascript
[
    {
        "id": 1,
        "imageUrl": "https://picsum.photos/200"
    },
    {
        "id": 2,
        "imageUrl": "https://picsum.photos/200"
    },
    {
        "id": 3,
        "imageUrl": "https://picsum.photos/200"
    }
]
```


### Map_Collections

- Route: `/api/v1/collections/map`
- Method: GET
- Header: 
  - Authorization: Bearer ${idToken}
- Return:
  - All map collections created or saved by the current user. Each map contains:
    - `id`: The unique identifier of the map.
    - `name`: The name of the map.
    - `iconUrl`: The URL of the icon representing the map.
    - `author`: The creator of the map.
    - `viewCount`: The number of times the map has been viewed.
    - `favCount`: The number of times the map has been marked as favorite.
- Example:

```javascript
[
    {
        "id": 11,
        "name": "台北飲料地圖",
        "iconUrl": "https://picsum.photos/200",
        "author": "enip",
        "viewCount": 441,
        "favCount": 189
    },
    {
        "id": 12,
        "name": "飲料導覽",
        "iconUrl": "https://picsum.photos/200",
        "author": "enip",
        "viewCount": 370,
        "favCount": 152
    },
    {
        "id": 13,
        "name": "夜市飲料攻略",
        "iconUrl": "https://picsum.photos/200",
        "author": "enip",
        "viewCount": 295,
        "favCount": 117
    }
]
```

### Restaurant_Collections

- Route: `/api/v1/collections/restaurant`
- Method: GET
- Header: 
  - Authorization: Bearer ${idToken}
- Return:
  - All restaurant collections favorited or saved by the current user. Each entry includes:
    - `name`: The name of the restaurant.
    - `location`: A JSON object containing latitude (`lat`) and longitude (`lng`).
    - `address`: The street address of the restaurant.
    - `telephone`: The telephone number of the restaurant.
    - `rating`: The average rating of the restaurant out of 5.
    - `placeId`: A unique identifier for the restaurant, potentially used for integrating with external services like Google Maps.
    - `viewCount`: The number of times the restaurant's details have been viewed.
    - `favCount`: The number of times the restaurant has been marked as favorite.
- Example:

```javascript
[
    {
        "name": "Restaurant 1",
        "location": {"lat": 25.0329694, "lng": 121.5654177},
        "address": "台北市大安區辛亥路二段170號",
        "telephone": "02 1234 5554",
        "rating": 4.5,
        "placeId": "asdjglsakjgka",
        "viewCount": 400,
        "favCount": 100
    },
    {
        "name": "Restaurant 2",
        "location": {"lat": 25.0329694, "lng": 121.5654177},
        "address": "台北市大安區辛亥路二段170號",
        "telephone": "02 1234 5554",
        "rating": 4.2,
        "placeId": "wewtwatqawt",
        "viewCount": 400,
        "favCount": 100
    },
    {
        "name": "Restaurant 3",
        "location": {"lat": 25.0329694, "lng": 121.5654177},
        "address": "台北市大安區辛亥路二段170號",
        "telephone": "02 1234 5554",
        "rating": 4.2,
        "placeId": "wewtwatqawt",
        "viewCount": 400,
        "favCount": 100
    }
]
```