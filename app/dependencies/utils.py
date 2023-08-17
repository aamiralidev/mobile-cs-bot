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

        retry_attempts = 3
        retry_delay = 5  # delay in seconds

        for attempt in range(retry_attempts):
            try:
                chat_completion_resp = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=self.messages,
                    temperature=0,  # noqa
                )
                # if request is successful, break out of loop
                break
            except:  # noqa
                if attempt + 1 == retry_attempts:
                    logging.info("Attempt failed due to openai server")
                    return {
                        "role": "assistant",
                        "content": "I'm sorry i'm just having network issue I'll get back to you soon",
                    }
                time.sleep(retry_delay)  # wait before retrying

        message_content = chat_completion_resp["choices"][0]["message"][
            "content"
        ]  # noqa
        role = chat_completion_resp["choices"][0]["message"]["role"]

        await self.update_chat(role, message_content)

        response_dict = {"role": role, "content": message_content}

        return response_dict
