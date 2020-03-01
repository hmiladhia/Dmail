import re
import warnings

from os import environ
from collections import MutableMapping


class Config(MutableMapping):
    def __init__(self, config_dict: dict, parent: 'Config' = None, name: str = None):
        self.__config_dict = dict()
        self.__parent = parent
        self.__load_config_dict(config_dict)
        if name:
            self.set_value('__name', name)

    def get_name(self):
        return self.__name

    def to_dict(self):
        d = {self.__reverse_parse_key(k): self.__reverse_parse_value(v) for k, v in self.__config_dict.items()}
        if self.__parent:
            d['__parent'] = self.__parent.get_name()
        return d

    def set_value(self, key, value):
        key = self.__parse_key(key)
        value = self.__parse_value(value, key)
        self.__config_dict[key] = value

    def format_string(self, text, regex=None):
        if regex is None:
            regex = r"{(.*?)}"
        matches = re.finditer(regex, text, re.MULTILINE | re.DOTALL)

        for matchNum, match in enumerate(matches):
            for groupNum in range(0, len(match.groups())):
                try:
                    value = self[match.group(1)]
                except KeyError:
                    value = match.group(0)
                text = re.sub(match.group(0), value, text)
        return text

    def __load_config_dict(self, dict_config):
        for key, value in dict_config.items():
            self.set_value(key, value)

    def __repr__(self):
        return f"Config: {self.to_dict()}"

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        if not key.startswith(self.__private_prefix):
            self.set_value(key, value)
        else:
            return super(Config, self).__setattr__(key, value)

    def __getitem__(self, k):
        if isinstance(k, dict):
            return Config({name: self[key] for key, name in k.items()})
        elif not (isinstance(k, str)) and hasattr(k, '__iter__'):
            return Config({key: self[key] for key in k})

        try:
            return self.__get_single_item(k)
        except KeyError:
            if self.__parent:
                return self.__parent.__get_single_item(k)
            raise KeyError

    def __get_single_item(self, sub_attributes):
        value = self.__get_raw_single_item(sub_attributes)
        if isinstance(value, str):
            try:
                value = self.format_string(value).format(os_environ=environ)
            except RecursionError:
                warnings.warn('Two config entries are calling each other: the raw value was used')
            except KeyError:
                warnings.warn('Key not found: the raw value was used')
        return value

    def __get_raw_single_item(self, sub_attributes):
        if isinstance(sub_attributes, str):
            sub_attributes = sub_attributes.split('.')
        if not sub_attributes:
            raise ValueError
        if len(sub_attributes) > 1:
            return self.__config_dict[sub_attributes[0]].__get_single_item(sub_attributes[1:])
        else:
            return self.__config_dict[sub_attributes[0]]

    def __setitem__(self, k, v) -> None:
        self.set_value(k, v)

    def __delitem__(self, v) -> None:
        del self.__config_dict[v]

    def __len__(self):
        return len(self.__config_dict)

    def __iter__(self):
        keys = {key for key in self.__config_dict if key and not key.startswith(self.__private_prefix)}
        if self.__parent:
            keys.update(self.__parent)
        return iter(keys)

    __private_prefix = f'_{__qualname__}'

    @classmethod
    def __parse_value(cls, value, name=None):
        if type(value) == dict:
            return Config(value, name=name)
        elif not (isinstance(value, str)) and hasattr(value, '__iter__'):
            return [cls.__parse_value(p) for p in value]
        return value

    @classmethod
    def __reverse_parse_value(cls, value):
        if type(value) == Config:
            return value.to_dict()
        elif not (isinstance(value, str)) and hasattr(value, '__iter__'):
            return [cls.__reverse_parse_value(p) for p in value]
        return value

    @classmethod
    def __parse_key(cls, key):
        return f'{cls.__private_prefix}{key}' if key[:2] == '__' else key

    @classmethod
    def __reverse_parse_key(cls, key):
        n = len(cls.__private_prefix)
        return key[n:] if key[:n] == cls.__private_prefix else key

