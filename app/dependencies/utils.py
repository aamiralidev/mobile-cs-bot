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

        retry_attempts = 5  # Number of retries
        retry_delay = 4  # Delay in seconds for each retry

        await asyncio.sleep(1.5)  # Initial sleep of 1 second

        chat_completion_resp = None  # Initialize the response variable

        total_wait_time = 0  # Initialize the total waiting time

        for attempt in range(retry_attempts):
            try:
                chat_completion_resp = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=self.messages,
                    temperature=0,  # noqa
                )
                # If the request is successful, break out of the loop
                break
            except Exception as e:
                logging.info(
                    f"Attempt {attempt + 1} failed due to OpenAI server error: {str(e)}"
                )
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
                "content": "I'm sorry, I'm having network issues. I'll get back to you soon.",
            }

        message_content = chat_completion_resp["choices"][0]["message"]["content"]
        role = chat_completion_resp["choices"][0]["message"]["role"]

        await self.update_chat(role, message_content)

        response_dict = {"role": role, "content": message_content}

        return response_dict


# Rate limit reached for 10KTPM-200RPM in organization org-OwEF47WmIVbizPha2QqABD0g on tokens per min.
# Limit: 10000 / min. Please try again in 6ms. Contact us through our help center at help.openai.com if you continue to have issues.
