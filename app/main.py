from fastapi import FastAPI

from app import models
from app.database import engine
from .routers import posts, user, auth, vote

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()




app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)