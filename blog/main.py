from fastapi import FastAPI,Depends,HTTPException,status,Response
from blog import models,schemas,database
from sqlalchemy.orm import Session
# uvicorn main:app --reload
# pip install -r requirements.txt
# https://docs.sqlalchemy.org/en/20/orm/tutorial.html
# FastAPI use this orm https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-an-engine
app = FastAPI()

# for bind model to db 
models.Base.metadata.create_all(database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return "app running"

# add new blog 
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title=request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating blog {e}")

# for get all blogs
@app.get("/blog",status_code=status.HTTP_200_OK)
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",status_code=200)
def get_single_blog(id,response:Response,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':"Not Found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    return blog

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:schemas.Blog,db:Session = Depends(get_db)):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id)
        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog not found")
        blog.update({
            'title':request.title,
            'body':request.body
        })
        db.commit()
        return {'message':"blog updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating blog {e}")

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog not found")
    db.commit() 
    blog.delete(synchronize_session=False)
    db.commit()
    return {'message':f"blog delete successfully"}
    
