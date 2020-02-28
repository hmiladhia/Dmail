from collections import Mapping


class Config(Mapping):
    def __init__(self, dict_config, parent=None, name=None):
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

    @staticmethod
    def __parse_value(value, name=None):
        if type(value) == dict:
            return Config(value, name=name)
        return value

    def __load_config(self, config):
        return self.__load_config_dict(config.__dict__)

    def __repr__(self):
        return f"Config: {self.__dict__}"

    def __getitem__(self, k):
        return self.__dict__[k]

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter([key for key in self.__dict__ if key and key[0] != "_"])