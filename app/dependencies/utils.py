import os

import openai
from dotenv import load_dotenv

from app.internal.prompt import Initial_prompt

load_dotenv()
openai.api_key = os.environ.get(
    "OPENAI_API_KEY"
)  # supply your API key however you choose


class Chatbot:
    def __init__(self):
        self.messages = Initial_prompt()

    async def update_chat(self, role, user_message):
        self.messages.append({"role": role, "content": user_message})

    async def create_chat_completion(self, user_message):
        await self.update_chat("user", user_message)

        chat_completion_resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo-16k", temperature=0.1, messages=self.messages
        )

        message_content = chat_completion_resp["choices"][0]["message"][
            "content"
        ]  # noqa
        role = chat_completion_resp["choices"][0]["message"]["role"]

        await self.update_chat(role, message_content)

        response_dict = {"role": role, "content": message_content}

        return response_dict
