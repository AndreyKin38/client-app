from fastapi import FastAPI
from backend.handlers import router

app = FastAPI()

app.include_router(router=router)






