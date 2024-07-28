from fastapi import FastAPI,Depends,HTTPException,status,Response
from blog import models,schemas,database
from sqlalchemy.orm import Session
from typing import List
# uvicorn main:app --reload
# pip install -r requirements.txt
# https://docs.sqlalchemy.org/en/20/orm/tutorial.html
# FastAPI use this orm https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-an-engine
app = FastAPI()

# for bind model to db 
models.Base.metadata.create_all(database.engine)

# get connection
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# for home route
@app.get("/")
def index():
    return "app running"

# add new blog 
# for db session we use Depends
# for get data from user we use schemas request:Blog
# for exeception we send HTTPExeception
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        # here query for add data 
        # sqlalchemy orm used by fastAPI
        # we send data
        new_blog = models.Blog(title=request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating blog {e}")

# for get all blogs
@app.get("/blog",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])    
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# for custom response we use response
# for short cut we use 404
# using response model we can specify which type of response data we send
@app.get("/blog/{id}",status_code=200,response_model=schemas.ShowBlog)
def get_single_blog(id,response:Response,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':"Not Found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    return blog

# for update we use put request 
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:schemas.Blog,db:Session = Depends(get_db)):
    try:
        # here query for find data
        blog = db.query(models.Blog).filter(models.Blog.id == id)
        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog not found")
        # update data
        blog.update({
            'title':request.title,
            'body':request.body
        })
        # commit
        db.commit()
        return {'message':"blog updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating blog {e}")

# for status we use status
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog not found")
    db.commit() 
    blog.delete(synchronize_session=False) 
    db.commit()
    return {'message':f"blog delete successfully"}
    
