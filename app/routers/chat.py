from fastapi import APIRouter, Request

from app.dependencies.utils import create_chat_completion

router = APIRouter()


@router.post("/recieve_message")
async def recieve_msg(request: Request):
    form_data = await request.form()

    message = form_data.get("Body", None)

    print("Received message: ", message)
    return await create_chat_completion(message)
