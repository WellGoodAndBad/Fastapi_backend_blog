from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
import pydantic


class UserInPost(BaseModel):
    id: Optional[str]
    email: str = None

    @pydantic.validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or str(uuid.uuid4())

    @pydantic.validator("email", pre=True, always=True)
    def default_email(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    posts_blog_title: str = ''
    posts_blog_text_blog: str = ''


class PostList(BaseModel):
    posts_blog_id: int
    posts_blog_title: str
    posts_blog_date: Optional[datetime]
    user_email: str


class PostSingle(PostList):
    posts_blog_text_blog: str


class PostCreate(PostBase):
    pass

    class Config:
        orm_mode = True
