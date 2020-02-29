from collections import Mapping


class Config(Mapping):
    def __init__(self, dict_config: dict, parent: 'Config' = None, name: str = None):
        if parent:
            self.__load_config(parent)
        if name:
            self.__name = name
        self.__load_config_dict(dict_config)

    def get_name(self):
        return self.__name

    def __load_config_dict(self, dict_config):
        for key, value in dict_config.items():
            value = self.__parse_value(value, key)
            if key[:2] == '__':
                setattr(self, f'_{type(self).__qualname__}__{key}', value)
            else:
                setattr(self, key, value)

    def __load_config(self, config):
        return self.__load_config_dict(config.__dict__)

    def __repr__(self):
        return f"Config: {self.__dict__}"

    def __getitem__(self, k):
        if isinstance(k, dict):
            return Config({name: self[key] for key, name in k.items()})
        elif not (isinstance(k, str)) and hasattr(k, '__iter__'):
            return Config({key: self[key] for key in k})

        return self.__dict__[k]

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter([key for key in self.__dict__ if key and key[0] != "_"])

    @classmethod
    def __parse_value(cls, value, name=None):
        if type(value) == dict:
            return Config(value, name=name)
        elif not (isinstance(value, str)) and hasattr(value, '__iter__'):
            return [cls.__parse_value(p) for p in value]
        return value
