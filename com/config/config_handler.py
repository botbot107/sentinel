import json

from com.config.singleton import Singleton
from com.model.config import Config
from definitions import CONF_PATH

@Singleton
class ConfigHandler:
    __config: Config

    def __init__(self):
        with open(CONF_PATH) as f:
            self.__config = Config.from_dict(json.loads(f.read()))

    def get(self) -> Config:
        return self.__config