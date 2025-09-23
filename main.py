from fastapi import FastAPI
from backend import routers

app = FastAPI()

for router in routers:
    app.include_router(router=router)


