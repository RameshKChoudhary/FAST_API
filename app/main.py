from fastapi import FastAPI, Response , status , HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel #seperates the content of the body automaticaly,and can check if it is their or not and it's type
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine ,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True #seting default
    rating: Optional[int] = None #optional field


while True:
    
    try:
        conn = psycopg2.connect(host="ep-delicate-dawn-ad9x94q3-pooler.c-2.us-east-1.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_6bIRx5Jgwryd",
        port=5432,
        sslmode="require",
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected")
        break

    except Exception as error:
        print("failed to connect")
        print("ERROR :",error)
        time.sleep(10)

my_posts=[
    {"title":"title...","content":"content...","id":1},
    {"title":"title2..","content":"content2..","id":2}
    ]


def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World !!"}



@app.get("/sqla")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}



@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM "new-schema"."posts" """)
    posts= cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create(post: Post):
    # # print(post)
    # # print(post.dict()) #converting to dict
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # return {"new post": post_dict}
    cursor.execute("""INSERT INTO "new-schema"."posts" (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new post": new_post}

@app.get("/posts/{id}")
def get_post(id:int): #converts to int
# def get_post(id:int , response:Response):

    cursor.execute("""SELECT * FROM "new-schema"."posts" WHERE id = %s """,(str(id)))
    post = cursor.fetchone()
    # post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with if: {id} was not found")
        # # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg":f"post with if: {id} was not found"}
    return {"post details":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):

    cursor.execute("""DELETE FROM "new-schema"."posts" WHERE id = %s RETURNING * """,(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id : int , post : Post):
    cursor.execute("""UPDATE "new-schema"."posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
 
    return {"updated data":updated_post}