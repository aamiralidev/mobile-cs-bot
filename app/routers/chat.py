import json
import logging
import os

import psycopg2
from fastapi import APIRouter, Request

from app.dependencies.utils import create_chat_completion
from app.internal.prompt import Initial_prompt

router = APIRouter()


# Environment variables
DB_NAME = os.getenv("DB_USER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def connect_to_db():
    """Create and return a database connection and cursor."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,  # noqa
    )
    cur = conn.cursor()
    return conn, cur


@router.post("/recieve_message")
async def recieve_msg(request: Request):
    form_data = await request.form()

    message = form_data.get("body", None)
    from_number = form_data.get("from", None)

    if not message or not from_number:
        return {"error": "Invalid request"}

    conn, cur = connect_to_db()

    try:
        # Check if conversation exists
        cur.execute(
            "SELECT messages FROM conversation_entries WHERE phone_number = %s",  # noqa
            (from_number,),
        )
        result = cur.fetchone()

        if result:
            # Append the message to existing conversation
            conversation_messages = result[0]
            conversation_messages.append({"role": "user", "content": message})
            cur.execute(
                "UPDATE conversation_entries SET messages = %s WHERE phone_number = %s",  # noqa
                (json.dumps(conversation_messages), from_number),
            )
        else:
            # Create a new conversation
            initial_prompt = Initial_prompt()
            conversation_messages = initial_prompt + [
                {"role": "user", "content": message}
            ]
            cur.execute(
                "INSERT INTO conversation_entries (phone_number, messages) VALUES (%s, %s)",  # noqa
                (from_number, json.dumps(conversation_messages)),
            )

        conn.commit()

        # Generate the response from the bot
        response_dict = await create_chat_completion(conversation_messages)

        # Append the bot response to the conversation
        conversation_messages.append(response_dict)
        cur.execute(
            "UPDATE conversation_entries SET messages = %s WHERE phone_number = %s",  # noqa
            (json.dumps(conversation_messages), from_number),
        )

        conn.commit()

        return response_dict

    except Exception as e:
        conn.rollback()
        logging.error(f"Error: {e}")
        return {"error": "An error occurred while processing the message"}

    finally:
        cur.close()
        conn.close()
