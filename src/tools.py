from functools import cached_property

import yaml

from src.chat import Chat
from src.documents import Documents


class Tools:
    def __init__(self, config_path: str, secrets_path: str):
        self.config = self.load_yaml(config_path)
        self.secrets = self.load_yaml(secrets_path)

    def load_yaml(self, file_path: str):
        with open(file_path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @cached_property
    def chat(self):
        return Chat(**self.config["chat"], **self.secrets["chat"])

    @cached_property
    def documents(self):
        return Documents(**self.config["documents"])
