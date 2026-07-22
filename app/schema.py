from pydantic import BaseModel , EmailStr #seperates the content of the body automaticaly,and can check if it is their or not and it's type
from datetime import datetime

class Postbase(BaseModel):
    title: str
    content: str
    published: bool = True #seting default

class Postcreate(Postbase):
    pass

class Post(Postbase):
    id: int
    created_at : datetime
    class config:
        orm_mode =True


class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id = int
    email : EmailStr
    created_at : datetime

    class config:
        orm_mode =True