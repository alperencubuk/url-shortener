# URL Shortener

URL Shortener API with FastAPI, Postgres, Sqlalchemy, Pydantic v2, Docker.

### Requirements:

```
docker
```

### Run:

```
cp config/.env.example config/.env
docker compose up --build
```

### Test (11/11):

```
docker exec api pytest
```

### Coverage (%96):

```
docker exec api coverage run -m pytest
docker exec api coverage report
```

### Docs:

```
OpenAPI: http://localhost:8000/docs
Postman: postman_collection.json in the project root.
```

### Endpoints:

```http request
POST   /urls          # url add
GET    /urls          # url list
GET    /urls/{url}    # url redirect or get
DELETE /urls/{url}    # url delete

GET    /              # health check
```

### Example Requests/Responses:

#### Request:
```http request
POST /urls

Body:
{
    "url": "https://alperencubuk.com"
}
```

#### Response:
```json
{
    "id": 1,
    "url": "https://alperencubuk.com/",
    "shortened_url": "http://localhost:8000/urls/76cc90e2-1bfe-40b8-a66c-a977307def03",
    "times_clicked": 0,
    "create_date": "2023-11-13T21:30:27.860036"
}
```

#### Request:
```http request
GET /urls/{short_url_path}
```

#### Response:
```
Redirect to URL
(times_clicked increases)
```

#### Request:
```http request
GET /urls/{short_url_path}?redirect=False

Query:
redirect: bool = Redirect or get json (defaul=True)
```

#### Response:
```json
{
    "id": 1,
    "url": "https://alperencubuk.com/",
    "shortened_url": "http://localhost:8000/urls/4c4decb9-d570-460c-a9db-eaa2c4968e13",
    "times_clicked": 1,
    "create_date": "2023-11-13T21:35:28.145748"
}
```

#### Request:
```http request
GET /urls?page=1&size=2

Query:
page: int = Page number (optional) (defaul=1)
size: int = Items per page (optional) (defaul=50)
sort: str = id or times_clicked (optional) (defaul=id)
order: str = asc or desc (optional) (defaul=asc)
```

#### Response:
```json
{
    "page": 1,
    "size": 2,
    "total": 3,
    "pages": 2,
    "urls": [
        {
            "id": 1,
            "url": "https://alperencubuk.com/",
            "shortened_url": "http://localhost:8000/urls/eb43ec8e-98d6-4f96-808a-9317c5ec9a06",
            "times_clicked": 2,
            "create_date": "2023-11-13T20:59:00.225971"
        },
        {
            "id": 2,
            "url": "https://github.com/",
            "shortened_url": "http://localhost:8000/urls/ced99896-97fb-482a-87ce-bbb5ce0f6204",
            "times_clicked": 0,
            "create_date": "2023-11-13T20:50:23.506770"
        }
    ]
}
```

### Database Tables:

```json
{
  "Base (Abstract)": {
    "id": "int",
    "create_date": "datetime"
  },
  "Urls": {
    "url": "str",
    "shortened_url": "uuid",
    "times_clicked": "int"
  }
}
```

### Migration:

```
docker exec api alembic revision --autogenerate -m "description"
docker exec api alembic upgrade head
```
