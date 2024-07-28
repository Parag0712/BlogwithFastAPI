from fastapi import FastAPI,Depends,HTTPException
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

@app.post("/blog")
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