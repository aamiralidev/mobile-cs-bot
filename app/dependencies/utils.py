import asyncio
import logging
import os
import time

import openai
from dotenv import load_dotenv

from app.internal.prompt import Initial_prompt

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


# flake8:noqa
class Chatbot:
    def __init__(self):
        self.messages = Initial_prompt()

    def clear_prompt(self):
        self.messages = Initial_prompt()

    async def update_chat(self, role, user_message):
        self.messages.append({"role": role, "content": user_message})

    async def create_chat_completion(self, user_message):
        await self.update_chat("user", user_message)

        retry_attempts = 4  # Changed to 4 retries
        retry_delay = 4  # Delay in seconds

        # Sleep for 1 second
        await asyncio.sleep(1)

        chat_completion_resp = None  # Initialize variable

        for attempt in range(retry_attempts):
            try:
                chat_completion_resp = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=self.messages,
                    temperature=0,  # noqa
                )
                # If request is successful, break out of loop
                break
            except Exception as e:
                logging.info(
                    f"Attempt {attempt + 1} failed due to openai server. Error: {str(e)}"
                )  # Log every exception
                if attempt + 1 == retry_attempts:
                    return {
                        "role": "assistant",
                        "content": "I'm sorry, I'm just having network issues. I'll get back to you soon.",
                    }
                await asyncio.sleep(retry_delay)  # Wait before retrying

        if chat_completion_resp is None:  # Check for uninitialized variable
            return {
                "role": "assistant",
                "content": "I'm sorry, I'm just having network issues. I'll get back to you soon.",
            }

        message_content = chat_completion_resp["choices"][0]["message"][
            "content"
        ]  # noqa
        role = chat_completion_resp["choices"][0]["message"]["role"]

        await self.update_chat(role, message_content)

        response_dict = {"role": role, "content": message_content}

        return response_dict


# Rate limit reached for 10KTPM-200RPM in organization org-OwEF47WmIVbizPha2QqABD0g on tokens per min.
# Limit: 10000 / min. Please try again in 6ms. Contact us through our help center at help.openai.com if you continue to have issues.
