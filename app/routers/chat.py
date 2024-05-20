from fastapi import APIRouter
from pydantic import BaseModel

from app.dependencies.utils import create_chat_completion

router = APIRouter()


class ChatInput(BaseModel):
    user_input: str


@router.post("/start_chat")
async def start_chat(chat_input: ChatInput):
    return await create_chat_completion(chat_input.user_input)
