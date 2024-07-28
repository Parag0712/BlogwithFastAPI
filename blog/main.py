from fastapi import FastAPI
from blog import models,schemas,database

# uvicorn main:app --reload
# pip install -r requirements.txt
# https://docs.sqlalchemy.org/en/20/orm/tutorial.html
app = FastAPI()

models.Base.metadata.create_all(database.engine)
@app.get("/")
def index(req:schemas.Blog):
    return "app running"
