from fastapi import APIRouter

from app.dependencies.utils import Chatbot

router = APIRouter()

chatbot = Chatbot()


@router.post("/start_chat")
async def start_chat(user_input: str):
    return await chatbot.create_chat_completion(user_input)
