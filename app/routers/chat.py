from fastapi import APIRouter, Request

from app.dependencies.utils import create_chat_completion

router = APIRouter()


@router.post("/recieve_message")
async def recieve_msg(request: Request):
    form_data = await request.form()

    message = form_data.get("body", None)

    from_number = form_data.get("from", None)

    print("Received message: ", f"{message} AND {from_number}")
    return await create_chat_completion(message)
