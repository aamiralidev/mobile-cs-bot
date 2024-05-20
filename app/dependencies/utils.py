import asyncio
import logging

import openai

from app.internal.prompt import Initial_prompt


async def create_chat_completion(user_message):
    messages = Initial_prompt()

    messages.append({"role": "user", "content": user_message})

    retry_attempts = 2  # Number of retries
    retry_delay = 2  # Delay in seconds for each retry

    await asyncio.sleep(8)  # Initial sleep of 7 second

    chat_completion_resp = None  # Initialize the response variable

    total_wait_time = 0  # Initialize the total waiting time

    for attempt in range(retry_attempts):
        try:
            chat_completion_resp = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                temperature=0,  # noqa
            )
            # If the request is successful, break out of the loop
            break
        except Exception as e:
            logging.info(
                f"""Attempt {attempt + 1} failed due to OpenAI server error:
                {str(e)}"""
            )
            print(str(e))
            await asyncio.sleep(
                retry_delay
            )  # Wait for 'retry_delay' seconds before the next attempt
            total_wait_time += retry_delay  # Update the total waiting time

    # If all retry attempts fail, return an error message
    if chat_completion_resp is None and total_wait_time >= (
        retry_attempts * retry_delay
    ):
        return {
            "role": "assistant",
            "content": """I'm sorry, I'm having network issues.
            I'll get back to you soon.""",
        }

    message_content = chat_completion_resp["choices"][0]["message"]["content"]
    role = chat_completion_resp["choices"][0]["message"]["role"]

    response_dict = {"role": role, "content": message_content}

    return response_dict
