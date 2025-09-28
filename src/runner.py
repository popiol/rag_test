import argparse

from langchain_community.chat_message_histories.file import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.tools import Tools

desc = """
    "a": ["ask_price", "ask_whole_lot_volume", "ask_lot_volume"],
    "b": ["bid_price", "bid_whole_lot_volume", "bid_lot_volume"],
    "c": ["closing_price", "closing_lot_volume"],
    "v": ["volume_today", "volume_24h"],
    "p": ["volume_weighted_price_today", "volume_weighted_price_24h"],
    "t": ["n_trades_today", "n_trades_24h"],
    "l": ["low_today", "low_24h"],
    "h": ["high_today", "high_24h"],
    "o": ["opening_price"],
"""


class Runner:
    def __init__(self, tools: Tools) -> None:
        self.tools = tools
        with open(
            "../crypto_alerts/data/quotes/year=2025/month=08/day=21/20250821220006.json"
        ) as f:
            quotes = f.read().replace("{", "{{").replace("}", "}}")
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                I will show you a JSON document with order price and volume info for crypto currencies.
                The document format is {{"currency_pair": {{
                "a": [<ask_price>, <ask_whole_lot_volume>, <ask_lot_volume>],
                "b": [<bid_price>, <bid_whole_lot_volume>, <bid_lot_volume>],
                "c": [<closing_price>, <closing_lot_volume>],
                "v": [<volume_today>, <volume_24h>],
                "p": [<volume_weighted_price_today>, <volume_weighted_price_24h>],
                "t": [<n_trades_today>, <n_trades_24h>],
                "l": [<low_today>, <low_24h>],
                "h": [<high_today>, <high_24h>],
                "o": <opening_price>
                }}, ... }}. 
            """
                    + "This is the document: "
                    + quotes,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("user", "{question}"),
            ]
        )

        def get_history(session_id: str) -> BaseChatMessageHistory:
            return FileChatMessageHistory(
                file_path=f"data/conversations/{session_id}.json"
            )

        self.conversation = RunnableWithMessageHistory(
            self.prompt_template | self.tools.llm.langchain_llm,
            get_history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def answer(self, question: str) -> str:
        # response = self.llm.invoke([HumanMessage(content=question)])
        response = self.conversation.invoke(
            {"question": "Which currency has the highest relative price amplitude?"},
            config={"configurable": {"session_id": "session1"}},
        )
        return response.text()


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
