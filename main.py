from fastapi import FastAPI
from backend.handlers import app_router, user_router, auth_router

app = FastAPI()

app.include_router(router=app_router)
app.include_router(router=user_router)
app.include_router(router=auth_router)









