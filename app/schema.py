from pydantic import BaseModel #seperates the content of the body automaticaly,and can check if it is their or not and it's type


class Postbase(BaseModel):
    title: str
    content: str
    published: bool = True #seting default

class Postcreate(Postbase):
    pass