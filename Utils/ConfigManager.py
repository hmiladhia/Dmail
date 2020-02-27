import os
import json

from pathlib import Path


class ConfigManager:
    def __init__(self, default_path=None):
        self.default_path = Path(default_path) if default_path else Path(os.getcwd())

    def load_config(self, config_name, path=None):
        config_path = self.__get_config_path(config_name, path)
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config

    def export_config(self, obj, config_name=None, path=None):
        config_path = self.__get_config_path(config_name if config_name else obj.__class__.__name__, path)
        with open(config_path, 'w') as config_file:
            json.dump(obj.__dict__, config_file)

    def __get_config_path(self, config_name, path):
        path = self.default_path if path is None else Path(path)
        return path / (config_name + '.json')


if __name__ == "__main__":
    cm = ConfigManager()
    # from config import GmailConfig
    #
    # gmailConfig = GmailConfig()
    # cm.export_config(gmailConfig)

    config = cm.load_config('GmailConfig')