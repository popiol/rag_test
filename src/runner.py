import argparse

from langchain_core.messages.utils import count_tokens_approximately

from src.tools import Tools


class Runner:
    def __init__(self, tools: Tools) -> None:
        self.tools = tools
        self.conversation = self.tools.chat.conversation

    def answer(self, question: str):
        response = self.tools.chat.llm.invoke(
            self.tools.chat.preparing_prompt_langchain.invoke(
                {
                    "current_timestamp": self.tools.documents.max_timestamp,
                    "question": question,
                }
            )
        )
        print(f"Timestamp retrieval token count: {response.usage_metadata['total_tokens']}")
        documents = self.tools.documents.find_closest(response.text())
        quotes = []
        timestamps = []
        for timestamp, document in documents:
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            timestamps.append(timestamp_str)
            with open(document) as f:
                data = f.read().replace("{", "{{").replace("}", "}}")
                quotes.append(f"{timestamp_str}: {data}")
        print("Using documents from timestamps:", ", ".join(str(ts) for ts in timestamps))
        inputs = {"quotes": "\n".join(quotes), "question": question}
        self.check_token_count(inputs)
        response = self.conversation.invoke(inputs)
        return f"used tokens: {response.usage_metadata}\n\n{response.text()}"

    def check_token_count(self, inputs: dict) -> None:
        n_tokens = sum(
            [count_tokens_approximately(p.invoke(inputs)) for p in self.conversation.get_prompts()]
        )
        print("Predicted token count:", n_tokens)
        if n_tokens > 1000_000:
            print("Too many tokens, aborting")
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
