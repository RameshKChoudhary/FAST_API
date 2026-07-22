from fastapi import FastAPI, Response , status , HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel #seperates the content of the body automaticaly,and can check if it is their or not and it's type
from typing import Optional , List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models , schema
from .database import engine ,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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




@app.get("/posts", response_model=List[schema.Post])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "new-schema"."posts" """)
    # all_posts= cursor.fetchall()
    # print(all_posts)
    all_posts = db.query(models.Post).all()
    return  all_posts

@app.post("/posts" , status_code=status.HTTP_201_CREATED , response_model=schema.Post)
def create(post: schema.Postcreate , db: Session = Depends(get_db)):

    # # print(post)
    # # print(post.dict()) #converting to dict
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # return {"new post": post_dict}

    # cursor.execute("""INSERT INTO "new-schema"."posts" (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()


    # new_post = models.Post(title = post.title,content = post.content, published = post.published)
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}" , response_model=schema.Post)
def get_post(id:int , db: Session = Depends(get_db)): #converts to int

    # cursor.execute("""SELECT * FROM "new-schema"."posts" WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    # # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with if: {id} was not found")

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM "new-schema"."posts" WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)


    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}" ,  response_model=schema.Post)
def update_post(id : int , post : schema.Postcreate , db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE "new-schema"."posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
 
    return post_query.first()



@app.post("/users" , status_code=status.HTTP_201_CREATED , response_model=schema.UserOut)
def create_user(user : schema.UserCreate , db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user