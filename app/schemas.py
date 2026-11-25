#How data enters and leaves API
#Pydantic schemas allow user to control which fields clients receive(different from models)
from datetime import datetime

from pydantic import BaseModel, PositiveInt, SecretStr

class User(BaseModel):
    id: int
    name: str = "John Doe"
    username: str
    email: str
    password: SecretStr
    signup_ts = datetime

class Comment(BaseModel):
    id: int
    description: str
    user: User
    likes: int
    posted_ts: datetime

class Post(BaseModel):
    id: int
    title: str
    description: str
    comments: list[Comment]
    likes: int
    upload_ts: datetime 