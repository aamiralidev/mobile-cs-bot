from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app.routers.chat import chatbot_ob

from .routers import chat, webhook

app = FastAPI()

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
    chatbot_ob.clear_prompt()
    return templates.TemplateResponse("chat.html", {"request": request})  # noqa


@app.get("/")
async def root():
    return "8*8 Work-api"
