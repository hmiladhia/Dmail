import json
import os

from pathlib import Path

from Utils.configmanager._config import Config


class ConfigManager:
    def __init__(self, default_path=None):
        self.default_path = Path(default_path) if default_path else Path(os.getcwd())

    def load_config(self, config_name, path=None):
        config_dict = self.__read_config_file(config_name, path)
        parent_config = self.__load_parent_config(config_dict)
        return Config(config_dict, parent_config, config_name)

    def export_config_file(self, obj, config_name=None, path=None):
        config_path = self.__get_config_path(config_name if config_name else obj.__class__.__name__, path)
        with open(config_path, 'w') as config_file:
            json.dump(obj.__dict__, config_file)

    def __read_config_file(self, config_name, path=None):
        config_path = self.__get_config_path(config_name, path)
        with open(config_path, 'r') as config_file:
            config_dict = json.load(config_file)
        return config_dict

    def __load_parent_config(self, config_dict, path=None):
        parent_name = config_dict.get('__parent', None)
        return self.load_config(parent_name, config_dict.get('__parent_path', None)) if parent_name else path

    def __get_config_path(self, config_name, path):
        path = self.default_path if path is None else Path(path)
        return path / (config_name + '.json')