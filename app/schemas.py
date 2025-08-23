from datetime import datetime
import email
from typing import Optional,Literal
from pydantic import BaseModel, EmailStr
from xmlrpc.client import boolean

from sqlalchemy import literal


class PostBase(BaseModel):
    title:str
    content:str
    published:boolean=True


class PostCreate(PostBase):
    pass

class User_Response(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        # orm_mode=True
        from_attributes=True

class PostResponse(PostBase):
    id:int
    created_at:datetime
    user_id:int
    user:User_Response

    class Config:
        #  orm_mode=True
         from_attributes=True


class PostOut(BaseModel):
    Post:PostResponse
    votes:int

    class Config:
        #  orm_mode=True
         from_attributes=True

class User_Create(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class vote(BaseModel):
    post_id:int
    dir:Literal[0,1]