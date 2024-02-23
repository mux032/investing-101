import os
import yaml
from typing import Type
from pydantic import BaseModel


class ConfigModel(BaseModel):
    website_url: str
    webdriver_path: str
    funds_list_file_path: str
    output_file_path: str

    def __str__(self):
        return str(self.dict())


class Config(ConfigModel):
    def __init__(self, **data):
        super().__init__(**data)

    @classmethod
    def load_config(cls: Type['Config'], config_path: str) -> 'Config':
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file is missing, check the path '{config_path}'")
        else:
            with open(config_path) as file:
                config_data = yaml.load(file, Loader=yaml.FullLoader)
                return cls.parse_obj(config_data)
