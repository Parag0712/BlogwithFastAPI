from fastapi import FastAPI
from schemas import Blog

# uvicorn main:app --reload
# pip install -r requirements.txt
# https://docs.sqlalchemy.org/en/20/orm/tutorial.html
app = FastAPI()

@app.get("/")
def index():
    return "app running"

@app.post("/blog")
def addblog(blog:Blog):
    return blog

