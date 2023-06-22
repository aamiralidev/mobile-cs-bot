from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import chat

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.include_router(chat.router)


@app.get("/")
async def root():
    return "8*8 Work-api"
