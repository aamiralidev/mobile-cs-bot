import logging
import os
from contextlib import asynccontextmanager

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app.dependencies import database

from .routers import chat, webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Database connection has started successfully")

    # Initialize database connection
    await database.init_db()

    yield  # This point is where the FastAPI application runs

    # Close database connection
    await database.close_db_connection()

    logging.info("Database connection closed successfully")


load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
print("key = ", str(os.environ.get("OPENAI_API_KEY")))


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(webhook.router)


templates = Jinja2Templates(directory="app/templates")


@app.get("/chat_interface")
async def chat_interface(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})  # noqa


@app.get("/")
async def root():
    return "Dan Chatbot api"
