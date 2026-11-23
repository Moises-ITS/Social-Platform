import random
from fastapi import (FastAPI,
                    Query,
                    Path,
                    Body,
                    Cookie,
                    Header,
                    Response,
                    HTTPException
)
from pydantic import BaseModel, Field, AfterValidator, EmailStr
from datetime import datetime, timezone, date
from typing import Annotated, Literal
from enum import StrEnum
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse, RedirectResponse

from app.database import check_database_connection
#Social Application Outline w/FastAPI

# Start Server ->
# uv run uvicorn app.main:app --reload

app = FastAPI(title="SocialAPI")

#model_config = {"extra": "forbid"}

#NOTE: JSON Only accepts strings as keys in a dictionary

#Filter Parameters
class Pagination(BaseModel):
    limit: int = Field(10, ge=1)
    offset: int = Field(0, ge=0)

class Filters(BaseModel):
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: set[str] = set()

#make each user have a dict of posts
#posts have list of comments + likes or dict
#ect.
class Post(BaseModel):
    post_id: int
    title: str
    description: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    hashed_password: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

fake_items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
fake_users = [{}]
fake_posts = [{}]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users")
def get_all_users(
    pagination: Annotated[Pagination, Query()],
    filters: Annotated[Filters, Query()],
    search: str | None = None,
):
    return fake_users[pagination.offset: pagination.offset + pagination.limit]

@app.get("/posts")
def get_all_posts(skip: Annotated[int, Query(min_length=1, max_length=len(fake_posts))] = 0, limit: Annotated[int, Query(min_length=1, max_length=len(fake_posts))] = 10):
    if skip >= limit:
        raise ValueError("Skip Cannot be greater than or equal to limit")
    return fake_posts[skip: skip + limit]

@app.get("/health/db")
def get_db_health():
    try:
        connected = check_database_connection
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database Unavailable")
    if not connected:
        raise HTTPException(status_code=503, detail="Detabase Check Failed")
    return {"database": "connected"}

#Examples
"""
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items[skip: skip + limit]

@app.post("items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
"""