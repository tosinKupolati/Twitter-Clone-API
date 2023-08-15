from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import posts, users, auth, likes
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TwitterCloneAPI")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(likes.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "welcome to my twitter-clone-api"}
