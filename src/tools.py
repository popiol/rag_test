from functools import cached_property

import yaml

from src.llm import LLM


class Tools:
    def __init__(self, config_path: str, secrets_path: str):
        self.config = self.load_yaml(config_path)
        self.secrets = self.load_yaml(secrets_path)

    def load_yaml(self, file_path: str):
        with open(file_path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @cached_property
    def llm(self):
        return LLM(**self.config["llm"], **self.secrets["llm"])
