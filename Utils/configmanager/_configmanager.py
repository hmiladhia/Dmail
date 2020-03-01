import json

from pathlib import Path

from Utils.configmanager import Config
from Utils.configmanager import import_config


class ConfigManager:
    @classmethod
    def load_config(cls, config_name, path):
        config_dict = cls.__read_config_file(config_name, path)
        parent_config = cls.__load_parent_config(config_dict, path)
        return Config(config_dict, parent_config, config_name)

    @classmethod
    def export_config_file(cls, obj, config_name=None, path=None, **kwargs):
        config_path = cls.__get_config_path(config_name if config_name else obj.__class__.__name__, path)
        config_dict = obj.to_dict()
        config_dict['__name'] = config_name
        with open(config_path, 'w') as config_file:
            json.dump(config_dict, config_file, indent=kwargs.get('indent', 2))

    @classmethod
    def __read_config_file(cls, config_name, path):
        config_path = cls.__get_config_path(config_name, path)
        with open(config_path, 'r') as config_file:
            config_dict = json.load(config_file)
        return config_dict

    @classmethod
    def __load_parent_config(cls, config_dict, path):
        parent_name = config_dict.get('__parent', None)
        parent_path = config_dict.get('__parent_path', None)
        return import_config(parent_name, parent_path if parent_path else path) if parent_name else None

    @staticmethod
    def __get_config_path(config_name, path):
        return Path(path) / (config_name + '.json')
