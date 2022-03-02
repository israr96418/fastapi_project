from fastapi import FastAPI
from . import models, database
# this create all our model
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, authenticaion,Vote

# we have no need of Longer of this command after Alembic

# this commad told to the sqlalchemy to run the create_all commad to create table
# means this one line of code convert all the sqlAlchemy model into tables

# models.Base.metadata.create_all(bind=database.engine)

origins = ["*"]
app = FastAPI()

app.add_middleware(
    # CORSMiddleware running before any request
    # allow_origin means ke ham ne kon kon se origin ko allow karna he ta ke o mere backend se communication kar sake
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authenticaion.router)
app.include_router(Vote.router)


@app.get("/")
def generic():
    return {"message":"helllo worldLLLLLL"}
