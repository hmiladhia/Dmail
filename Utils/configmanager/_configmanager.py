import os
import json
import sys

from itertools import chain
from pathlib import Path

from Utils.configmanager import Config


class ConfigManager:
    @classmethod
    def import_config(cls, name, path=None):
        level = 0
        if name.startswith('.'):
            if not path:
                path = os.getcwd()
            for character in name:
                if character != '.':
                    break
                level += 1
        return cls.__config_import(name[level:], path, level)

    @classmethod
    def export_config_file(cls, obj, config_name=None, path=None, **kwargs):
        config_path = cls.__get_config_path(config_name if config_name else obj.__class__.__name__, path)
        config_dict = obj.to_dict()
        config_dict['__name'] = config_name
        with open(config_path, 'w') as config_file:
            json.dump(config_dict, config_file, indent=kwargs.get('indent', 2))

    @classmethod
    def __load_config(cls, config_name, path):
        config_dict = cls.__read_config_file(config_name, path)
        parent_config = cls.__load_parent_config(config_dict, path)
        return Config(config_dict, parent_config, config_name)

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
        return cls.import_config(parent_name, parent_path if parent_path else path) if parent_name else None

    @classmethod
    def __config_import(cls, name, path, level=0):
        base, _, name = name.rpartition('.')
        base = base.replace('.', '/')
        for path in chain([path], sys.path):
            try:
                if path:
                    cls.__sanity_check(name, path, level)
                    path = Path(path)
                    path = (path.parent if level == 2 else path) / base
                    return cls.__load_config(name, path)
            except FileNotFoundError:
                pass
        raise FileNotFoundError

    @staticmethod
    def __sanity_check(name, path, level):
        """Verify arguments are "sane"."""
        if not isinstance(name, str):
            raise TypeError('configuration name must be str, not {}'.format(type(name)))
        if level < 0:
            raise ValueError('level must be >= 0')
        if level > 0:
            if not isinstance(path, str):
                raise TypeError('path not set to a string')
            elif not path:
                raise ImportError('attempted relative import with no known path')
        if level > 2:
            raise ValueError('Invalid Path: level must be <= 2')
        if not name and level == 0:
            raise ValueError('Empty configuration name')

    @staticmethod
    def __get_config_path(config_name, path):
        return Path(path) / (config_name + '.json')