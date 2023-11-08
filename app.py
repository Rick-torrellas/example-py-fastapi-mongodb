from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="Example Python Fastapi Pymongo",
    version="v0.3.0"
)

app.include_router(user)