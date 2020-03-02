import os
import sys

from itertools import chain
from pathlib import Path

from Utils.configmanager._configmanager import ConfigManager


def import_config(name, path=None):
    level = 0
    if name.startswith('.'):
        if not path:
            path = os.getcwd()
        for character in name:
            if character != '.':
                break
            level += 1
    return _config_import(name[level:], path, level)


def _sanity_check(name, path, level):
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


def _config_import(name, path, level=0):
    base, _, name = name.rpartition('.')
    base = base.replace('.', '/')
    for path in chain([path], sys.path):
        try:
            if path:
                _sanity_check(name, path, level)
                path = Path(path)
                path = (path.parent if level == 2 else path) / base
                return ConfigManager.load_config(name, path)
        except FileNotFoundError:
            pass
    raise FileNotFoundError


ConfigManager.import_config = import_config
