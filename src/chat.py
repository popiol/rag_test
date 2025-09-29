from dataclasses import dataclass
from functools import cached_property

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI


@dataclass
class Chat:
    model: str
    api_key: str
    conversations_path: str
    system_prompt: str
    user_prompt: str
    preparing_prompt: str

    @cached_property
    def prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt.replace("{", "{{").replace("}", "}}")),
                *[("user", message) for message in self.user_prompt.splitlines() if message],
            ]
        )

    @cached_property
    def preparing_prompt_langchain(self):
        return ChatPromptTemplate.from_messages(
            [
                *[("user", message) for message in self.preparing_prompt.splitlines() if message],
            ]
        )

    @cached_property
    def llm(self):
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
        )

    @cached_property
    def conversation(self):
        return self.prompt | self.llm
