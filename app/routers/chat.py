from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.models import ConversationEntry
from app.dependencies.utils import create_chat_completion
from app.internal.prompt import Initial_prompt

router = APIRouter()


@router.post("/recieve_message")
async def recieve_msg(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    message = form_data.get("body", None)
    from_number = form_data.get("from", None)

    if not message or not from_number:
        return {"error": "Invalid request"}

    # Check if conversation exists
    conversation = (
        db.query(ConversationEntry).filter_by(phone_number=from_number).first()
    )

    if conversation:
        # Append the message to existing conversation
        conversation.messages.append({"role": "user", "content": message})
    else:
        # Create a new conversation
        initial_prompt = Initial_prompt()
        conversation = ConversationEntry(
            phone_number=from_number,
            messages=initial_prompt + [{"role": "user", "content": message}],
        )
        db.add(conversation)

    db.commit()

    # Generate the response from the bot
    response_dict = await create_chat_completion(conversation.messages)

    # Append the bot response to the conversation
    conversation.messages.append(response_dict)
    db.commit()

    return response_dict
