from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.routers.router import router

app = FastAPI(title="User service", version='1.0')

app.include_router(router)

origins = ["localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)