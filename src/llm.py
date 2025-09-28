from dataclasses import dataclass
from functools import cached_property

from langchain_google_genai import ChatGoogleGenerativeAI


@dataclass
class LLM:
    api_key: str
    model: str
    type: str

    @cached_property
    def langchain_llm(self):
        if self.type == "ChatGoogleGenerativeAI":
            return ChatGoogleGenerativeAI(
                model=self.model,
                google_api_key=self.api_key,
            )
        else:
            raise ValueError(f"Unsupported LLM type: {self.type}")
