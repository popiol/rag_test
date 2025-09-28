import argparse
from datetime import datetime

from langchain_core.messages.utils import count_tokens_approximately
from langchain_core.runnables.config import RunnableConfig

from src.tools import Tools


class Runner:
    def __init__(self, tools: Tools) -> None:
        self.tools = tools
        self.conversation = self.tools.chat.conversation

    def answer(self, question: str) -> str:
        response = self.tools.chat.llm.invoke(
            self.tools.chat.preparing_prompt_langchain.invoke(
                {
                    "current_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": question,
                }
            )
        )
        print(response)
        exit()
        with open(
            "../crypto_alerts/data/quotes/year=2025/month=08/day=21/20250821220006.json"
        ) as f:
            quotes = f.read().replace("{", "{{").replace("}", "}}")
        inputs = {"quotes": quotes, "question": question}
        config = RunnableConfig({"configurable": {"session_id": "session1"}})
        response = self.conversation.invoke(inputs, config=config)
        return response

    def check_token_count(self, inputs: dict, config: RunnableConfig) -> None:
        n_tokens = sum(
            [
                count_tokens_approximately(p.invoke({**inputs, "history": []}))
                for p in self.conversation.get_prompts(config=config)
            ]
        )
        if n_tokens > 100_000:
            print(f"Too many tokens: {n_tokens}")
            exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yml")
    parser.add_argument("--secrets", default="secrets.yml")
    parser.add_argument("--question")
    args = parser.parse_args()
    tools = Tools(args.config, args.secrets)
    runner = Runner(tools)
    print(runner.answer(args.question))


if __name__ == "__main__":
    main()
