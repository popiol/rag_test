import argparse

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.tools import Tools


class Runner:
    def __init__(self, tools: Tools, secrets_path: str) -> None:
        self.tools = tools
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.tools.llm.api_key,
        )

    def answer(self, question: str) -> str:
        response = self.llm.invoke([HumanMessage(content=question)])
        return response.text()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yml")
    parser.add_argument("--secrets", default="secrets.yml")
    parser.add_argument("--question")
    args = parser.parse_args()
    tools = Tools(args.config, args.secrets)
    runner = Runner(tools, args.secrets)
    print(runner.answer(args.question))


if __name__ == "__main__":
    main()
